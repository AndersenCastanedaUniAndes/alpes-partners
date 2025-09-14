from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.comandos import Comando
from typing import Optional

@dataclass
class ProgramarPago(Comando):
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
