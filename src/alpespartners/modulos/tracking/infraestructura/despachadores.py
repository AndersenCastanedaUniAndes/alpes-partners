import pulsar
import os
from pulsar.schema import *
from alpespartners.modulos.tracking.infraestructura.schema.v1.comandos import ComandoRegistrarImpresion, ComandoRegistrarConversion
from alpespartners.modulos.tracking.infraestructura.schema.v1.eventos import EventoImpresionRegistrada, EventoConversionRegistrada
from alpespartners.seedwork.infraestructura.utils import time_millis
from datetime import datetime
import uuid


class Despachador:
    def __init__(self):
        self.broker_host = os.getenv('BROKER_HOST', 'localhost')
        self.pulsar_client = pulsar.Client(f'pulsar://{self.broker_host}:6650')

    def publicar_comando(self, comando, topico):
        if isinstance(comando, ComandoRegistrarImpresion):
            self._publicar_comando_impresion(comando, topico)
        elif isinstance(comando, ComandoRegistrarConversion):
            self._publicar_comando_conversion(comando, topico)

    def publicar_evento(self, evento, topico):
        if isinstance(evento, EventoImpresionRegistrada):
            self._publicar_evento_impresion(evento, topico)
        elif isinstance(evento, EventoConversionRegistrada):
            self._publicar_evento_conversion(evento, topico)

    def _publicar_comando_impresion(self, comando, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(ComandoRegistrarImpresion)
        )
        producer.send(comando)
        producer.close()

    def _publicar_comando_conversion(self, comando, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(ComandoRegistrarConversion)
        )
        producer.send(comando)
        producer.close()

    def _publicar_evento_impresion(self, evento, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(EventoImpresionRegistrada)
        )
        producer.send(evento)
        producer.close()

    def _publicar_evento_conversion(self, evento, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(EventoConversionRegistrada)
        )
        producer.send(evento)
        producer.close()

    def cerrar(self):
        self.pulsar_client.close()
