"""
API de consultas para el módulo de tracking
Implementa CQRS con read models optimizados para consultas
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime

from alpespartners.modulos.tracking.infraestructura.read_models import (
    ImpresionReadModelRepository, ConversionReadModelRepository, CampañaStatsReadModelRepository
)


router = APIRouter(prefix="/tracking/queries", tags=["tracking-queries"])


@router.get("/health")
async def health_check():
    return {"message": "Tracking Queries API is healthy"}


@router.get("/impresiones/{impresion_id}")
async def obtener_impresion(impresion_id: str):
    """Obtiene una impresión por ID usando read model"""
    try:
        repo = ImpresionReadModelRepository()
        impresion = repo.get_impresion(impresion_id)
        
        if not impresion:
            raise HTTPException(status_code=404, detail="Impresión no encontrada")
        
        return {
            "id": impresion.id,
            "campaña_id": impresion.campaña_id,
            "influencer_id": impresion.influencer_id,
            "usuario_id": impresion.usuario_id,
            "tipo_evento": impresion.tipo_evento,
            "user_agent": impresion.user_agent,
            "ip_address": impresion.ip_address,
            "referrer": impresion.referrer,
            "timestamp": impresion.timestamp.isoformat(),
            "created_at": impresion.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversiones/{conversion_id}")
async def obtener_conversion(conversion_id: str):
    """Obtiene una conversión por ID usando read model"""
    try:
        repo = ConversionReadModelRepository()
        conversion = repo.get_conversion(conversion_id)
        
        if not conversion:
            raise HTTPException(status_code=404, detail="Conversión no encontrada")
        
        return {
            "id": conversion.id,
            "campaña_id": conversion.campaña_id,
            "influencer_id": conversion.influencer_id,
            "usuario_id": conversion.usuario_id,
            "tipo_conversion": conversion.tipo_conversion,
            "valor": conversion.valor,
            "moneda": conversion.moneda,
            "user_agent": conversion.user_agent,
            "ip_address": conversion.ip_address,
            "referrer": conversion.referrer,
            "timestamp": conversion.timestamp.isoformat(),
            "created_at": conversion.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campañas/{campaña_id}/impresiones")
async def obtener_impresiones_campaña(campaña_id: str, limit: int = 100):
    """Obtiene impresiones por campaña usando read model"""
    try:
        repo = ImpresionReadModelRepository()
        impresiones = repo.get_impresiones_by_campaña(campaña_id)[:limit]
        
        return {
            "campaña_id": campaña_id,
            "total": len(impresiones),
            "impresiones": [
                {
                    "id": imp.id,
                    "influencer_id": imp.influencer_id,
                    "usuario_id": imp.usuario_id,
                    "tipo_evento": imp.tipo_evento,
                    "timestamp": imp.timestamp.isoformat()
                }
                for imp in impresiones
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campañas/{campaña_id}/conversiones")
async def obtener_conversiones_campaña(campaña_id: str, limit: int = 100):
    """Obtiene conversiones por campaña usando read model"""
    try:
        repo = ConversionReadModelRepository()
        conversiones = repo.get_conversiones_by_campaña(campaña_id)[:limit]
        
        return {
            "campaña_id": campaña_id,
            "total": len(conversiones),
            "conversiones": [
                {
                    "id": conv.id,
                    "influencer_id": conv.influencer_id,
                    "usuario_id": conv.usuario_id,
                    "tipo_conversion": conv.tipo_conversion,
                    "valor": conv.valor,
                    "moneda": conv.moneda,
                    "timestamp": conv.timestamp.isoformat()
                }
                for conv in conversiones
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campañas/{campaña_id}/estadisticas")
async def obtener_estadisticas_campaña(campaña_id: str):
    """Obtiene estadísticas de una campaña usando read model"""
    try:
        repo = CampañaStatsReadModelRepository()
        stats = repo.get_stats(campaña_id)
        
        if not stats:
            return {
                "campaña_id": campaña_id,
                "total_impresiones": 0,
                "total_conversiones": 0,
                "valor_total_conversiones": 0.0,
                "tasa_conversion": 0.0,
                "ultima_actualizacion": None
            }
        
        return {
            "campaña_id": stats.campaña_id,
            "total_impresiones": stats.total_impresiones,
            "total_conversiones": stats.total_conversiones,
            "valor_total_conversiones": stats.valor_total_conversiones,
            "tasa_conversion": stats.tasa_conversion,
            "ultima_actualizacion": stats.ultima_actualizacion.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/influencers/{influencer_id}/impresiones")
async def obtener_impresiones_influencer(influencer_id: str, limit: int = 100):
    """Obtiene impresiones por influencer usando read model"""
    try:
        repo = ImpresionReadModelRepository()
        impresiones = repo.get_impresiones_by_influencer(influencer_id)[:limit]
        
        return {
            "influencer_id": influencer_id,
            "total": len(impresiones),
            "impresiones": [
                {
                    "id": imp.id,
                    "campaña_id": imp.campaña_id,
                    "tipo_evento": imp.tipo_evento,
                    "timestamp": imp.timestamp.isoformat()
                }
                for imp in impresiones
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/influencers/{influencer_id}/conversiones")
async def obtener_conversiones_influencer(influencer_id: str, limit: int = 100):
    """Obtiene conversiones por influencer usando read model"""
    try:
        repo = ConversionReadModelRepository()
        conversiones = repo.get_conversiones_by_influencer(influencer_id)[:limit]
        
        return {
            "influencer_id": influencer_id,
            "total": len(conversiones),
            "conversiones": [
                {
                    "id": conv.id,
                    "campaña_id": conv.campaña_id,
                    "tipo_conversion": conv.tipo_conversion,
                    "valor": conv.valor,
                    "moneda": conv.moneda,
                    "timestamp": conv.timestamp.isoformat()
                }
                for conv in conversiones
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
