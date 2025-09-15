import pulsar,_pulsar  
from pulsar.schema import *
import logging
import traceback

from alpespartners.modulos.marketing_influencers.infraestructura.schema.v1.eventos import EventoCampañaCreada, CampañaCreadaPayload
from alpespartners.modulos.marketing_influencers.infraestructura.schema.v1.comandos import ComandoCrearCampaña
from alpespartners.seedwork.infraestructura import utils
from pulsar import Consumer
from alpespartners.modulos.marketing_influencers.infraestructura.despachadores import Despachador

def suscribirse_a_eventos():
    cliente: Consumer = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-campaña', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoCampañaCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-campaña', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearCampaña))

        while True:
            mensaje = consumidor.receive()
            data = mensaje.value().data
            print(f'Comando recibido: {data}')

            # Publicar evento simple a "eventos-campaña" tras recibir el comando
            class _Evento:
                def __init__(self, id: str):
                    self.id = id

            try:
                campañaCreada = EventoCampañaCreada()
                campañaCreada.data = CampañaCreadaPayload()
                campañaCreada.data.id = data.id
                Despachador().publicar_evento(campañaCreada, 'campaña-creada')
                print(f'Evento enviado a campaña-creada: {{"id": "{data.id}"}}')
            except Exception:
                logging.error('ERROR: Publicando evento a campaña-creada')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
