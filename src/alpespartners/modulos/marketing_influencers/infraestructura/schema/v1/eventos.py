from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class CampañaCreadaPayload(Record):
    id = String()


class EventoCampañaCreada(EventoIntegracion):
    data = CampañaCreadaPayload()
