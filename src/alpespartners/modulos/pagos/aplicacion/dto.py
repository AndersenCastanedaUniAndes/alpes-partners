from dataclasses import dataclass
from typing import Optional

@dataclass
class PagoDTO:
    pago_id: str
    usuario_id: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    monto: float = 0.0
    moneda: str = "COP"
    numero_tarjeta: Optional[str] = None
    expiracion: Optional[str] = None
    cvv: Optional[str] = None
    fecha_programada: Optional[str] = None

@dataclass
class ComisionDTO:
    pago_id: str
    monto_comision: float = 0.0
    moneda: str = "COP"
