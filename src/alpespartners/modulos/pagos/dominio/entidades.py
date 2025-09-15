from alpespartners.seedwork.dominio.entidades import Entidad
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Pago(Entidad):
    pago_id: str
    usuario_id: Optional[str]
    nombre: Optional[str]
    email: Optional[str]
    monto: float
    moneda: str
    fecha_programada: Optional[str]
    estado: str = 'pendiente'
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Comision(Entidad):
    pago_id: str
    monto_comision: float
    moneda: str
    timestamp: datetime = field(default_factory=datetime.now)

    def calcular_comision(self, porcentaje: float) -> float:
        """Calcula la comisión basada en el monto del pago"""
        return self.monto_comision * (porcentaje / 100)
