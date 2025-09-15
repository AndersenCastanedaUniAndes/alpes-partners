from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.comandos import Comando
from typing import Optional

@dataclass
class CalcularComision(Comando):
    pago_id: str
    usuario_id: Optional[str] = None
    monto: float = 0.0
    moneda: str = "COP"
    fecha_programada: Optional[str] = None
