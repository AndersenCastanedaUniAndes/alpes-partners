from pulsar.schema import *
from alpespartners.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion


class EventoImpresionRegistrada(EventoIntegracion):
    id = String()
    campaña_id = String()
    influencer_id = String()
    usuario_id = String()
    tipo_evento = String()
    user_agent = String()
    ip_address = String()
    referrer = String()
    timestamp = String()


class EventoConversionRegistrada(EventoIntegracion):
    id = String()
    campaña_id = String()
    influencer_id = String()
    usuario_id = String()
    tipo_conversion = String()
    valor = Float()
    moneda = String()
    user_agent = String()
    ip_address = String()
    referrer = String()
    timestamp = String()
