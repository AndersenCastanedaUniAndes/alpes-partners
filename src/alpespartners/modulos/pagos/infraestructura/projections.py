from datetime import datetime
from alpespartners.modulos.pagos.dominio.eventos import PagoRealizado, ComisionCalculada
from alpespartners.modulos.pagos.infraestructura.read_models import (
    PagoReadModel, ComisionReadModel,
    PagoReadModelRepository, ComisionReadModelRepository
)

class PagoProjection:
    def __init__(self):
        self.pago_repo = PagoReadModelRepository()

    def handle_pago_realizado(self, event: PagoRealizado):
        pago_read_model = PagoReadModel(
            pago_id=event.pago_id,
            usuario_id=event.usuario_id,
            monto_pagado=event.monto_pagado,
            moneda=event.moneda,
            fecha_realizacion=event.fecha_realizacion,
            timestamp=event.timestamp or datetime.now()
        )
        self.pago_repo.save_pago(pago_read_model)

class ComisionProjection:
    def __init__(self):
        self.comision_repo = ComisionReadModelRepository()

    def handle_comision_calculada(self, event: ComisionCalculada):
        comision_read_model = ComisionReadModel(
            pago_id=event.pago_id,
            monto_comision=event.monto_comision,
            moneda=event.moneda,
            timestamp=event.timestamp or datetime.now()
        )
        self.comision_repo.save_comision(comision_read_model)

class ProjectionManagerPagos:
    def __init__(self):
        self.pago_projection = PagoProjection()
        self.comision_projection = ComisionProjection()

    def handle_event(self, event):
        if isinstance(event, PagoRealizado):
            self.pago_projection.handle_pago_realizado(event)
        elif isinstance(event, ComisionCalculada):
            self.comision_projection.handle_comision_calculada(event)

    def rebuild_all_projections(self):
        # Reconstruye los modelos de lectura desde el event store
        pass

class ProyeccionPagos:
    def actualizar(self, evento):
        # Actualiza modelos de lectura según eventos
        pass
