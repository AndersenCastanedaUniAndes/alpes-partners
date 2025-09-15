from fastapi import APIRouter, Depends, Response
import json

from alpespartners.config.db import get_session
from alpespartners.modulos.marketing_influencers.aplicacion.mapeadores import MapeadorCampañaDTOJson
from alpespartners.modulos.marketing_influencers.infraestructura.despachadores import Despachador
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio


router = APIRouter(prefix="/marketing-influencers", tags=["marketing-influencers"])


@router.get("/health")
async def health_check():
    return {"message": "Marketing Influencers API is healthy"}


@router.post("/campañas")
async def crear_campaña(campaña_dict: dict):
    print(f'Recibido para creación: {campaña_dict}')
    try:
        map_campaña = MapeadorCampañaDTOJson()
        campaña_dto = map_campaña.externo_a_dto(campaña_dict)

        # Publicar en el tópico de comandos para que lo consuma el microservicio
        despachador = Despachador()
        # Enviamos el DTO directamente como "comando" (el despachador extrae los campos necesarios)
        despachador.publicar_comando(campaña_dto, 'comandos-campaña')

        return Response(json.dumps({'status': 'EN_QUEUED'}), status_code=202, media_type='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps({'error': str(e)}), status_code=400, media_type='application/json')



@router.get("/campañas/{campaña_id}")
async def obtener_campaña(campaña_id: str):
    # TODO: Lógica para obtener una campaña por su ID
    return {"message": "Campaña obtenida", "campaña_id": campaña_id}


@router.post("/conversiones")
async def registrar_conversion(conversion_dict: dict):
    # TODO: Lógica para registrar una conversión
    return {"message": "Conversión registrada", "conversión": conversion_dict}

