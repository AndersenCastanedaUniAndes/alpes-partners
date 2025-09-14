"""
Proyecciones para mantener read models actualizados
Implementa el patrón Projection para CQRS
"""
from datetime import datetime
from typing import List
from alpespartners.modulos.tracking.dominio.eventos import ImpresionRegistrada, ConversionRegistrada
from alpespartners.modulos.tracking.infraestructura.read_models import (
    ImpresionReadModel, ConversionReadModel, CampañaStatsReadModel,
    ImpresionReadModelRepository, ConversionReadModelRepository, CampañaStatsReadModelRepository
)


class ImpresionProjection:
    """Proyección para mantener el read model de impresiones actualizado"""
    
    def __init__(self):
        self.impresion_repo = ImpresionReadModelRepository()
        self.stats_repo = CampañaStatsReadModelRepository()

    def handle_impresion_registrada(self, event: ImpresionRegistrada):
        """Maneja el evento ImpresionRegistrada"""
        # Crear read model
        impresion_read_model = ImpresionReadModel(
            id=event.id,
            campaña_id=event.campaña_id,
            influencer_id=event.influencer_id,
            usuario_id=event.usuario_id,
            tipo_evento=event.tipo_evento,
            user_agent=event.metadatos.user_agent.valor,
            ip_address=event.metadatos.ip_address.direccion,
            referrer=event.metadatos.referrer.url,
            timestamp=event.timestamp,
            created_at=datetime.now()
        )
        
        # Guardar en read model
        self.impresion_repo.save_impresion(impresion_read_model)
        
        # Actualizar estadísticas de campaña
        self._update_campaña_stats(event.campaña_id)

    def _update_campaña_stats(self, campaña_id: str):
        """Actualiza las estadísticas de una campaña"""
        # Obtener impresiones de la campaña
        impresiones = self.impresion_repo.get_impresiones_by_campaña(campaña_id)
        total_impresiones = len(impresiones)
        
        # Obtener conversiones de la campaña
        conversion_repo = ConversionReadModelRepository()
        conversiones = conversion_repo.get_conversiones_by_campaña(campaña_id)
        total_conversiones = len(conversiones)
        
        # Calcular valor total de conversiones
        valor_total = sum(conv.valor for conv in conversiones)
        
        # Actualizar estadísticas
        self.stats_repo.update_stats(campaña_id, total_impresiones, total_conversiones, valor_total)


class ConversionProjection:
    """Proyección para mantener el read model de conversiones actualizado"""
    
    def __init__(self):
        self.conversion_repo = ConversionReadModelRepository()
        self.stats_repo = CampañaStatsReadModelRepository()

    def handle_conversion_registrada(self, event: ConversionRegistrada):
        """Maneja el evento ConversionRegistrada"""
        # Crear read model
        conversion_read_model = ConversionReadModel(
            id=event.id,
            campaña_id=event.campaña_id,
            influencer_id=event.influencer_id,
            usuario_id=event.usuario_id,
            tipo_conversion=event.tipo_conversion.value,
            valor=event.valor.valor,
            moneda=event.valor.moneda,
            user_agent=event.metadatos.user_agent.valor,
            ip_address=event.metadatos.ip_address.direccion,
            referrer=event.metadatos.referrer.url,
            timestamp=event.timestamp,
            created_at=datetime.now()
        )
        
        # Guardar en read model
        self.conversion_repo.save_conversion(conversion_read_model)
        
        # Actualizar estadísticas de campaña
        self._update_campaña_stats(event.campaña_id)

    def _update_campaña_stats(self, campaña_id: str):
        """Actualiza las estadísticas de una campaña"""
        # Obtener conversiones de la campaña
        conversiones = self.conversion_repo.get_conversiones_by_campaña(campaña_id)
        total_conversiones = len(conversiones)
        valor_total = sum(conv.valor for conv in conversiones)
        
        # Obtener impresiones de la campaña
        impresion_repo = ImpresionReadModelRepository()
        impresiones = impresion_repo.get_impresiones_by_campaña(campaña_id)
        total_impresiones = len(impresiones)
        
        # Actualizar estadísticas
        self.stats_repo.update_stats(campaña_id, total_impresiones, total_conversiones, valor_total)


class ProjectionManager:
    """Gestor de proyecciones que coordina todas las proyecciones"""
    
    def __init__(self):
        self.impresion_projection = ImpresionProjection()
        self.conversion_projection = ConversionProjection()

    def handle_event(self, event):
        """Maneja un evento y ejecuta las proyecciones correspondientes"""
        if isinstance(event, ImpresionRegistrada):
            self.impresion_projection.handle_impresion_registrada(event)
        elif isinstance(event, ConversionRegistrada):
            self.conversion_projection.handle_conversion_registrada(event)

    def rebuild_all_projections(self):
        """Reconstruye todas las proyecciones desde el event store"""
        # Esta función se implementaría para reconstruir read models
        # desde el event store en caso de corrupción de datos
        pass
