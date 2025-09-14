import json
import pulsar
import os
from pulsar.schema import *
from alpespartners.modulos.pagos.infraestructura.schema.v1.comandos import EsquemaComandoProgramarPago, EsquemaComandoCalcularComision
from alpespartners.modulos.pagos.infraestructura.schema.v1.eventos import EsquemaEventoPagoRealizado, EsquemaEventoComisionCalculada

class DespachadorPagos:
    def __init__(self, broker_url=None):
        self.broker_url = broker_url or "pulsar://localhost:6650"
        self.broker_host = os.getenv('BROKER_HOST', 'localhost')
        self.pulsar_client = pulsar.Client(f'pulsar://{self.broker_host}:6650')

    def despachar(self, evento):
        # Simulación de envío de evento al broker
        print(f"🚚 Despachando evento de pagos al broker {self.broker_url}...")
        print(f"Evento: {json.dumps(evento.__dict__, default=str, ensure_ascii=False)}")
        # Aquí iría la lógica real de integración con Pulsar o el broker
        # Por ejemplo, publicar en un tópico específico
        # ...
        print("✅ Evento despachado!")

    def publicar_comando(self, comando, topico):
        if isinstance(comando, EsquemaComandoProgramarPago):
            self._publicar_comando_programar_pago(comando, topico)
        elif isinstance(comando, EsquemaComandoCalcularComision):
            self._publicar_comando_calcular_comision(comando, topico)

    def publicar_evento(self, evento, topico):
        if isinstance(evento, EsquemaEventoPagoRealizado):
            self._publicar_evento_pago_realizado(evento, topico)
        elif isinstance(evento, EsquemaEventoComisionCalculada):
            self._publicar_evento_comision_calculada(evento, topico)

    def _publicar_comando_programar_pago(self, comando, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(EsquemaComandoProgramarPago)
        )
        producer.send(comando)
        producer.close()

    def _publicar_comando_calcular_comision(self, comando, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(EsquemaComandoCalcularComision)
        )
        producer.send(comando)
        producer.close()

    def _publicar_evento_pago_realizado(self, evento, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(EsquemaEventoPagoRealizado)
        )
        producer.send(evento)
        producer.close()

    def _publicar_evento_comision_calculada(self, evento, topico):
        producer = self.pulsar_client.create_producer(
            topico,
            schema=AvroSchema(EsquemaEventoComisionCalculada)
        )
        producer.send(evento)
        producer.close()

    def cerrar(self):
        self.pulsar_client.close()
