from uuid import UUID
import pulsar,_pulsar  
from pulsar.schema import *
import logging
import traceback

from alpespartners.modulos.marketing_influencers.infraestructura.schema.v1.eventos import EventoCampañaCreada, CampañaCreadaPayload
from alpespartners.modulos.marketing_influencers.infraestructura.schema.v1.comandos import ComandoCrearCampaña, ComandoCrearCampañaPayload
from alpespartners.modulos.marketing_influencers.aplicacion.comandos.crear_campaña import CrearCampaña
from alpespartners.seedwork.aplicacion.comandos import ejecutar_comando
from alpespartners.seedwork.infraestructura import utils
from alpespartners.modulos.marketing_influencers.infraestructura.despachadores import Despachador
from pulsar import Consumer

def suscribirse_a_eventos():
    cliente: Consumer = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-campana', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='aeroalpes-sub-eventos', schema=AvroSchema(EventoCampañaCreada))

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
        consumidor = cliente.subscribe('comandos-campana', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearCampaña))

        while True:
            mensaje = consumidor.receive()

            try:
                data: ComandoCrearCampañaPayload = mensaje.value().data

                comando = CrearCampaña(
                    id=str(data.id),
                    nombre=data.nombre,
                    producto=data.producto,
                    presupuesto=data.presupuesto,
                    moneda=data.moneda,
                    marca=data.marca,
                    influencers_ids=[str(UUID(influencer_id)) for influencer_id in data.influencers_ids] if data.influencers_ids else [],
                    conversiones=data.conversiones if data.conversiones else []
                )

                ejecutar_comando(comando)
            except Exception:
                logging.error('ERROR: Publicando evento a campana-creada')
                traceback.print_exc()

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
