"""
Consumidores corregidos para el módulo de tracking
Versión funcional sin Event Store
"""
import pulsar
import os
from pulsar.schema import *
from alpespartners.modulos.tracking.infraestructura.schema.v1.comandos import ComandoRegistrarImpresion, ComandoRegistrarConversion
from alpespartners.modulos.tracking.infraestructura.schema.v1.eventos import EventoImpresionRegistrada, EventoConversionRegistrada
from alpespartners.modulos.tracking.infraestructura.repositorios import RepositorioImpresionesInMemory, RepositorioConversionesInMemory
from alpespartners.modulos.tracking.dominio.objetos_valor import Metadatos, UserAgent, IPAddress, Referrer, TipoConversion, ValorConversion
from alpespartners.modulos.tracking.dominio.entidades import Impresion, Conversion
from alpespartners.modulos.tracking.dominio.eventos import ImpresionRegistrada, ConversionRegistrada
from datetime import datetime
import json


class ConsumidorComandosFixed:
    def __init__(self):
        self.broker_host = os.getenv('BROKER_HOST', 'localhost')
        self.pulsar_client = pulsar.Client(f'pulsar://{self.broker_host}:6650')
        self.repo_impresiones = RepositorioImpresionesInMemory()
        self.repo_conversiones = RepositorioConversionesInMemory()

    def suscribirse_a_comandos_impresion(self):
        consumer = self.pulsar_client.subscribe(
            'comando-registrar-impresion',
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name='tracking-impresion-sub',
            schema=AvroSchema(ComandoRegistrarImpresion)
        )

        print("🔄 Consumidor de impresiones iniciado...")
        while True:
            try:
                mensaje = consumer.receive()
                comando_data = mensaje.value()
                
                print(f"📊 Procesando impresión: {comando_data.id}")
                
                # Crear metadatos
                metadatos = Metadatos(
                    user_agent=UserAgent(comando_data.user_agent),
                    ip_address=IPAddress(comando_data.ip_address),
                    referrer=Referrer(comando_data.referrer),
                    timestamp=comando_data.timestamp
                )

                # Crear entidad de dominio
                impresion = Impresion(
                    id=comando_data.id,
                    campaña_id=comando_data.campaña_id,
                    influencer_id=comando_data.influencer_id if comando_data.influencer_id else None,
                    usuario_id=comando_data.usuario_id if comando_data.usuario_id else None,
                    tipo_evento=comando_data.tipo_evento,
                    metadatos=metadatos,
                    timestamp=datetime.fromisoformat(comando_data.timestamp) if comando_data.timestamp else datetime.now()
                )

                # Persistir
                self.repo_impresiones.agregar(impresion)
                
                # Crear evento de dominio
                evento = ImpresionRegistrada(
                    id=impresion.id,
                    campaña_id=impresion.campaña_id,
                    influencer_id=impresion.influencer_id,
                    usuario_id=impresion.usuario_id,
                    tipo_evento=impresion.tipo_evento,
                    metadatos=impresion.metadatos,
                    timestamp=impresion.timestamp
                )
                
                # Publicar evento
                self._publicar_evento_impresion(evento)
                
                consumer.acknowledge(mensaje)
                print(f"✅ Impresión {comando_data.id} procesada exitosamente")
                
            except Exception as e:
                print(f"❌ Error procesando impresión: {e}")
                consumer.negative_acknowledge(mensaje)

    def suscribirse_a_comandos_conversion(self):
        consumer = self.pulsar_client.subscribe(
            'comando-registrar-conversion',
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name='tracking-conversion-sub',
            schema=AvroSchema(ComandoRegistrarConversion)
        )

        print("🔄 Consumidor de conversiones iniciado...")
        while True:
            try:
                mensaje = consumer.receive()
                comando_data = mensaje.value()
                
                print(f"💰 Procesando conversión: {comando_data.id}")
                
                # Crear metadatos
                metadatos = Metadatos(
                    user_agent=UserAgent(comando_data.user_agent),
                    ip_address=IPAddress(comando_data.ip_address),
                    referrer=Referrer(comando_data.referrer),
                    timestamp=comando_data.timestamp
                )

                # Crear valor de conversión
                valor = ValorConversion(comando_data.valor, comando_data.moneda)

                # Crear entidad de dominio
                conversion = Conversion(
                    id=comando_data.id,
                    campaña_id=comando_data.campaña_id,
                    influencer_id=comando_data.influencer_id if comando_data.influencer_id else None,
                    usuario_id=comando_data.usuario_id if comando_data.usuario_id else None,
                    tipo_conversion=TipoConversion(comando_data.tipo_conversion),
                    valor=valor,
                    metadatos=metadatos,
                    timestamp=datetime.fromisoformat(comando_data.timestamp) if comando_data.timestamp else datetime.now()
                )

                # Persistir
                self.repo_conversiones.agregar(conversion)
                
                # Crear evento de dominio
                evento = ConversionRegistrada(
                    id=conversion.id,
                    campaña_id=conversion.campaña_id,
                    influencer_id=conversion.influencer_id,
                    usuario_id=conversion.usuario_id,
                    tipo_conversion=conversion.tipo_conversion,
                    valor=conversion.valor,
                    metadatos=conversion.metadatos,
                    timestamp=conversion.timestamp
                )
                
                # Publicar evento
                self._publicar_evento_conversion(evento)
                
                consumer.acknowledge(mensaje)
                print(f"✅ Conversión {comando_data.id} procesada exitosamente")
                
            except Exception as e:
                print(f"❌ Error procesando conversión: {e}")
                consumer.negative_acknowledge(mensaje)

    def _publicar_evento_impresion(self, evento):
        producer = self.pulsar_client.create_producer(
            'evento-impresion-registrada',
            schema=AvroSchema(EventoImpresionRegistrada)
        )
        
        evento_data = EventoImpresionRegistrada(
            id=evento.id,
            campaña_id=evento.campaña_id,
            influencer_id=evento.influencer_id or "",
            usuario_id=evento.usuario_id or "",
            tipo_evento=evento.tipo_evento,
            user_agent=evento.metadatos.user_agent.valor,
            ip_address=evento.metadatos.ip_address.direccion,
            referrer=evento.metadatos.referrer.url,
            timestamp=evento.timestamp.isoformat()
        )
        
        producer.send(evento_data)
        producer.close()

    def _publicar_evento_conversion(self, evento):
        producer = self.pulsar_client.create_producer(
            'evento-conversion-registrada',
            schema=AvroSchema(EventoConversionRegistrada)
        )
        
        evento_data = EventoConversionRegistrada(
            id=evento.id,
            campaña_id=evento.campaña_id,
            influencer_id=evento.influencer_id or "",
            usuario_id=evento.usuario_id or "",
            tipo_conversion=evento.tipo_conversion.value,
            valor=evento.valor.valor,
            moneda=evento.valor.moneda,
            user_agent=evento.metadatos.user_agent.valor,
            ip_address=evento.metadatos.ip_address.direccion,
            referrer=evento.metadatos.referrer.url,
            timestamp=evento.timestamp.isoformat()
        )
        
        producer.send(evento_data)
        producer.close()

    def cerrar(self):
        self.pulsar_client.close()


def main():
    consumidor = ConsumidorComandosFixed()
    
    print("🚀 Iniciando consumidores de tracking (versión corregida)...")
    print("=" * 60)
    
    try:
        # Ejecutar consumidores en hilos separados
        import threading
        
        thread_impresiones = threading.Thread(
            target=consumidor.suscribirse_a_comandos_impresion
        )
        thread_conversiones = threading.Thread(
            target=consumidor.suscribirse_a_comandos_conversion
        )
        
        thread_impresiones.start()
        thread_conversiones.start()
        
        thread_impresiones.join()
        thread_conversiones.join()
        
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo consumidores...")
        consumidor.cerrar()


if __name__ == "__main__":
    main()
