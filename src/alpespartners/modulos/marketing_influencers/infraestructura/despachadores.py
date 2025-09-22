import pulsar
from pulsar.schema import *
from datetime import datetime

from alpespartners.modulos.marketing_influencers.infraestructura.schema.v1.eventos import EventoCampañaCreada, CampañaCreadaPayload
from alpespartners.modulos.marketing_influencers.infraestructura.schema.v1.comandos import ComandoCrearCampaña, ComandoCrearCampañaPayload
from alpespartners.seedwork.infraestructura import utils


epoch = datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()


    def publicar_evento(self, evento, topico):
        print(f'Publicando evento a {topico}: {evento}')
        payload = self.to_payload(CampañaCreadaPayload, evento)

        evento_integracion = EventoCampañaCreada(
            id=str(utils.time_millis()),
            time=int(utils.time_millis()),
            specversion="1.0",
            type="campaña-creada",
            datacontenttype="avro/binary",
            service_name=utils.service_name(),
            data=payload,
        )

        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoCampañaCreada))


    def publicar_comando(self, dto, topico):
        payload = self.to_payload(ComandoCrearCampañaPayload, dto, extra={
            'fecha_creacion': int(unix_time_millis(datetime.now()))
        })

        comando = ComandoCrearCampaña(
            id=str(utils.time_millis()),
            time=int(utils.time_millis()),
            specversion="1.0",
            type="crear-campaña",
            datacontenttype="avro/binary",
            service_name=utils.service_name(),
            data=payload,
        )

        self._publicar_mensaje(comando, topico, AvroSchema(ComandoCrearCampaña))


    def to_payload(self, payload_cls, source_obj, extra: dict = None):
        data = {}
        for field in payload_cls.__dict__.keys():
            if hasattr(source_obj, field):
                data[field] = getattr(source_obj, field)
        if extra:
            data.update(extra)

        return payload_cls(**data)

