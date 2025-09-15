import pulsar
import os
from pulsar.schema import *
from alpespartners.modulos.tracking.infraestructura.schema.v1.comandos import ComandoRegistrarImpresion, ComandoRegistrarConversion
from alpespartners.modulos.tracking.infraestructura.schema.v1.eventos import EventoImpresionRegistrada, EventoConversionRegistrada
from alpespartners.modulos.tracking.infraestructura.repositorios import RepositorioImpresionesInMemory, RepositorioConversionesInMemory
from alpespartners.modulos.tracking.infraestructura.event_store import EventStore, EventStoreRepository
from alpespartners.modulos.tracking.infraestructura.projections import ProjectionManager
from alpespartners.modulos.tracking.aplicacion.handlers import RegistrarImpresionHandler, RegistrarConversionHandler
from alpespartners.modulos.tracking.aplicacion.comandos.registrar_impresion import RegistrarImpresion
from alpespartners.modulos.tracking.aplicacion.comandos.registrar_conversion import RegistrarConversion
from alpespartners.seedwork.infraestructura.utils import millis_a_datetime
from datetime import datetime
import json


class ConsumidorComandos:
    def __init__(self):
        self.broker_host = os.getenv('BROKER_HOST', 'localhost')
        self.pulsar_client = pulsar.Client(f'pulsar://{self.broker_host}:6650')
        self.repo_impresiones = RepositorioImpresionesInMemory()
        self.repo_conversiones = RepositorioConversionesInMemory()
        
        # Nueva topología híbrida
        self.event_store = EventStore()
        self.event_store_repo = EventStoreRepository(self.event_store)
        self.projection_manager = ProjectionManager()

    def suscribirse_a_comandos_impresion(self):
        consumer = self.pulsar_client.subscribe(
            'comando-registrar-impresion',
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name='tracking-impresion-sub',
            schema=AvroSchema(ComandoRegistrarImpresion)
        )

        while True:
            mensaje = consumer.receive()
            comando_data = mensaje.value()
            
            # Convertir a comando de aplicación
            comando = RegistrarImpresion(
                id=comando_data.id,
                campaña_id=comando_data.campaña_id,
                influencer_id=comando_data.influencer_id,
                usuario_id=comando_data.usuario_id,
                tipo_evento=comando_data.tipo_evento,
                user_agent=comando_data.user_agent,
                ip_address=comando_data.ip_address,
                referrer=comando_data.referrer,
                timestamp=comando_data.timestamp
            )

            # Procesar comando
            handler = RegistrarImpresionHandler()
            impresion = handler.handle(comando)
            
            # Persistir en repositorio tradicional (para compatibilidad)
            self.repo_impresiones.agregar(impresion)
            
            # Nueva topología: Guardar en Event Store
            evento = handler.eventos[0]
            self.event_store_repo.save_impresion(impresion.id, evento)
            
            # Ejecutar proyecciones para actualizar read models
            self.projection_manager.handle_event(evento)
            
            # Publicar evento
            self._publicar_evento_impresion(evento)
            
            consumer.acknowledge(mensaje)

    def suscribirse_a_comandos_conversion(self):
        consumer = self.pulsar_client.subscribe(
            'comando-registrar-conversion',
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name='tracking-conversion-sub',
            schema=AvroSchema(ComandoRegistrarConversion)
        )

        while True:
            mensaje = consumer.receive()
            comando_data = mensaje.value()
            
            # Convertir a comando de aplicación
            comando = RegistrarConversion(
                id=comando_data.id,
                campaña_id=comando_data.campaña_id,
                influencer_id=comando_data.influencer_id,
                usuario_id=comando_data.usuario_id,
                tipo_conversion=comando_data.tipo_conversion,
                valor=comando_data.valor,
                moneda=comando_data.moneda,
                user_agent=comando_data.user_agent,
                ip_address=comando_data.ip_address,
                referrer=comando_data.referrer,
                timestamp=comando_data.timestamp
            )

            # Procesar comando
            handler = RegistrarConversionHandler()
            conversion = handler.handle(comando)
            
            # Persistir en repositorio tradicional (para compatibilidad)
            self.repo_conversiones.agregar(conversion)
            
            # Nueva topología: Guardar en Event Store
            evento = handler.eventos[0]
            self.event_store_repo.save_conversion(conversion.id, evento)
            
            # Ejecutar proyecciones para actualizar read models
            self.projection_manager.handle_event(evento)
            
            # Publicar evento
            self._publicar_evento_conversion(evento)
            
            consumer.acknowledge(mensaje)

    def _publicar_evento_impresion(self, evento):
        producer = self.pulsar_client.create_producer(
            'evento-impresion-registrada',
            schema=AvroSchema(EventoImpresionRegistrada)
        )
        
        evento_data = EventoImpresionRegistrada(
            id=evento.id,
            campaña_id=evento.campaña_id,
            influencer_id=evento.influencer_id,
            usuario_id=evento.usuario_id,
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
            influencer_id=evento.influencer_id,
            usuario_id=evento.usuario_id,
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
