from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class TipoPago(ObjetoValor):
    tipo: str

@dataclass(frozen=True)
class ValorPago(ObjetoValor):
    monto: float
    moneda: str

@dataclass(frozen=True)
class MetadatosPago(ObjetoValor):
    nombre: str
    email: str
    timestamp: str

class EstadoPago(Enum):
    PENDIENTE = "PENDIENTE"
    PROGRAMADO = "PROGRAMADO"
    REALIZADO = "REALIZADO"
