from fastapi import APIRouter, Depends, Response
import json
from datetime import datetime

from alpespartners.config.db import get_session
from alpespartners.modulos.tracking.aplicacion.comandos.registrar_impresion import RegistrarImpresion
from alpespartners.modulos.tracking.aplicacion.comandos.registrar_conversion import RegistrarConversion
from alpespartners.modulos.tracking.aplicacion.mapeadores import MapeadorImpresionDTOJson, MapeadorConversionDTOJson
from alpespartners.modulos.tracking.infraestructura.despachadores import Despachador
from alpespartners.modulos.tracking.infraestructura.schema.v1.comandos import ComandoRegistrarImpresion, ComandoRegistrarConversion
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio


router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.get("/health")
async def health_check():
    return {"message": "Tracking API is healthy"}


@router.post("/impresiones")
async def registrar_impresion(impresion_dict: dict, session=Depends(get_session)):
    try:
        map_impresion = MapeadorImpresionDTOJson()
        impresion_dto = map_impresion.externo_a_dto(impresion_dict)

        comando = RegistrarImpresion(
            id=impresion_dto.id,
            campaña_id=impresion_dto.campaña_id,
            influencer_id=impresion_dto.influencer_id,
            usuario_id=impresion_dto.usuario_id,
            tipo_evento=impresion_dto.tipo_evento,
            user_agent=impresion_dto.user_agent,
            ip_address=impresion_dto.ip_address,
            referrer=impresion_dto.referrer,
            timestamp=impresion_dto.timestamp
        )

        # Crear comando para Pulsar
        comando_pulsar = ComandoRegistrarImpresion(
            id=comando.id,
            campaña_id=comando.campaña_id,
            influencer_id=comando.influencer_id or "",
            usuario_id=comando.usuario_id or "",
            tipo_evento=comando.tipo_evento,
            user_agent=comando.user_agent,
            ip_address=comando.ip_address,
            referrer=comando.referrer,
            timestamp=comando.timestamp
        )

        despachador = Despachador()
        despachador.publicar_comando(comando_pulsar, "comando-registrar-impresion")

        return Response(json.dumps({'status': 'EN_QUEUED'}), status_code=202, media_type='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps({'error': str(e)}), status_code=400, media_type='application/json')


@router.post("/conversiones")
async def registrar_conversion(conversion_dict: dict, session=Depends(get_session)):
    try:
        map_conversion = MapeadorConversionDTOJson()
        conversion_dto = map_conversion.externo_a_dto(conversion_dict)

        comando = RegistrarConversion(
            id=conversion_dto.id,
            campaña_id=conversion_dto.campaña_id,
            influencer_id=conversion_dto.influencer_id,
            usuario_id=conversion_dto.usuario_id,
            tipo_conversion=conversion_dto.tipo_conversion,
            valor=conversion_dto.valor,
            moneda=conversion_dto.moneda,
            user_agent=conversion_dto.user_agent,
            ip_address=conversion_dto.ip_address,
            referrer=conversion_dto.referrer,
            timestamp=conversion_dto.timestamp
        )

        # Crear comando para Pulsar
        comando_pulsar = ComandoRegistrarConversion(
            id=comando.id,
            campaña_id=comando.campaña_id,
            influencer_id=comando.influencer_id or "",
            usuario_id=comando.usuario_id or "",
            tipo_conversion=comando.tipo_conversion,
            valor=comando.valor,
            moneda=comando.moneda,
            user_agent=comando.user_agent,
            ip_address=comando.ip_address,
            referrer=comando.referrer,
            timestamp=comando.timestamp
        )

        despachador = Despachador()
        despachador.publicar_comando(comando_pulsar, "comando-registrar-conversion")

        return Response(json.dumps({'status': 'EN_QUEUED'}), status_code=202, media_type='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps({'error': str(e)}), status_code=400, media_type='application/json')


@router.get("/impresiones/{impresion_id}")
async def obtener_impresion(impresion_id: str):
    # TODO: Implementar consulta de impresión
    return {"message": "Impresión obtenida", "impresion_id": impresion_id}


@router.get("/conversiones/{conversion_id}")
async def obtener_conversion(conversion_id: str):
    # TODO: Implementar consulta de conversión
    return {"message": "Conversión obtenida", "conversion_id": conversion_id}


@router.get("/campañas/{campaña_id}/impresiones")
async def obtener_impresiones_campaña(campaña_id: str):
    # TODO: Implementar consulta de impresiones por campaña
    return {"message": "Impresiones de campaña obtenidas", "campaña_id": campaña_id}


@router.get("/campañas/{campaña_id}/conversiones")
async def obtener_conversiones_campaña(campaña_id: str):
    # TODO: Implementar consulta de conversiones por campaña
    return {"message": "Conversiones de campaña obtenidas", "campaña_id": campaña_id}
