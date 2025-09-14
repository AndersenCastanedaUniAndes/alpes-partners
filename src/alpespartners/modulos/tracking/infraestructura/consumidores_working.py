"""
Consumidores funcionales para el módulo de tracking
Versión simplificada que funciona correctamente
"""
import pulsar
import os
from pulsar.schema import *
from alpespartners.modulos.tracking.infraestructura.schema.v1.comandos import ComandoRegistrarImpresion, ComandoRegistrarConversion
from alpespartners.modulos.tracking.infraestructura.schema.v1.eventos import EventoImpresionRegistrada, EventoConversionRegistrada
from alpespartners.modulos.tracking.infraestructura.repositorios import RepositorioImpresionesInMemory, RepositorioConversionesInMemory
from datetime import datetime
import json


class ConsumidorComandosWorking:
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
                
                # Crear entidad de dominio simplificada
                from alpespartners.modulos.tracking.dominio.entidades import Impresion
                from alpespartners.modulos.tracking.dominio.objetos_valor import Metadatos, UserAgent, IPAddress, Referrer, TipoEvento
                
                metadatos = Metadatos(
                    user_agent=UserAgent(comando_data.user_agent),
                    ip_address=IPAddress(comando_data.ip_address),
                    referrer=Referrer(comando_data.referrer),
                    timestamp=comando_data.timestamp
                )

                impresion = Impresion(
                    id=comando_data.id,
                    campaña_id=comando_data.campaña_id,
                    influencer_id=comando_data.influencer_id if comando_data.influencer_id else None,
                    usuario_id=comando_data.usuario_id if comando_data.usuario_id else None,
                    tipo_evento=TipoEvento(comando_data.tipo_evento),
                    metadatos=metadatos,
                    timestamp=datetime.fromisoformat(comando_data.timestamp) if comando_data.timestamp else datetime.now()
                )

                # Persistir
                self.repo_impresiones.agregar(impresion)
                
                # Publicar evento
                self._publicar_evento_impresion(comando_data)
                
                consumer.acknowledge(mensaje)
                print(f"✅ Impresión {comando_data.id} procesada exitosamente")
                
            except Exception as e:
                print(f"❌ Error procesando impresión: {e}")
                import traceback
                traceback.print_exc()
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
                
                # Crear entidad de dominio simplificada
                from alpespartners.modulos.tracking.dominio.entidades import Conversion
                from alpespartners.modulos.tracking.dominio.objetos_valor import Metadatos, UserAgent, IPAddress, Referrer, TipoConversion, ValorConversion
                
                metadatos = Metadatos(
                    user_agent=UserAgent(comando_data.user_agent),
                    ip_address=IPAddress(comando_data.ip_address),
                    referrer=Referrer(comando_data.referrer),
                    timestamp=comando_data.timestamp
                )

                valor = ValorConversion(comando_data.valor, comando_data.moneda)

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
                
                # Publicar evento
                self._publicar_evento_conversion(comando_data)
                
                consumer.acknowledge(mensaje)
                print(f"✅ Conversión {comando_data.id} procesada exitosamente")
                
            except Exception as e:
                print(f"❌ Error procesando conversión: {e}")
                import traceback
                traceback.print_exc()
                consumer.negative_acknowledge(mensaje)

    def _publicar_evento_impresion(self, comando_data):
        producer = self.pulsar_client.create_producer(
            'evento-impresion-registrada',
            schema=AvroSchema(EventoImpresionRegistrada)
        )
        
        evento_data = EventoImpresionRegistrada(
            id=comando_data.id,
            campaña_id=comando_data.campaña_id,
            influencer_id=comando_data.influencer_id or "",
            usuario_id=comando_data.usuario_id or "",
            tipo_evento=comando_data.tipo_evento,
            user_agent=comando_data.user_agent,
            ip_address=comando_data.ip_address,
            referrer=comando_data.referrer,
            timestamp=comando_data.timestamp
        )
        
        producer.send(evento_data)
        producer.close()

    def _publicar_evento_conversion(self, comando_data):
        producer = self.pulsar_client.create_producer(
            'evento-conversion-registrada',
            schema=AvroSchema(EventoConversionRegistrada)
        )
        
        evento_data = EventoConversionRegistrada(
            id=comando_data.id,
            campaña_id=comando_data.campaña_id,
            influencer_id=comando_data.influencer_id or "",
            usuario_id=comando_data.usuario_id or "",
            tipo_conversion=comando_data.tipo_conversion,
            valor=comando_data.valor,
            moneda=comando_data.moneda,
            user_agent=comando_data.user_agent,
            ip_address=comando_data.ip_address,
            referrer=comando_data.referrer,
            timestamp=comando_data.timestamp
        )
        
        producer.send(evento_data)
        producer.close()

    def cerrar(self):
        self.pulsar_client.close()


def main():
    consumidor = ConsumidorComandosWorking()
    
    print("🚀 Iniciando consumidores de tracking (versión funcional)...")
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
