from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class TipoEvento(ObjetoValor):
    tipo: str


@dataclass(frozen=True)
class UserAgent(ObjetoValor):
    valor: str


@dataclass(frozen=True)
class IPAddress(ObjetoValor):
    direccion: str


@dataclass(frozen=True)
class Referrer(ObjetoValor):
    url: str


class TipoConversion(Enum):
    VENTA = "VENTA"
    REGISTRO = "REGISTRO"
    SUSCRIPCION = "SUSCRIPCION"
    DESCARGAR = "DESCARGAR"
    CLICK = "CLICK"


@dataclass(frozen=True)
class ValorConversion(ObjetoValor):
    valor: float
    moneda: str


@dataclass(frozen=True)
class Metadatos(ObjetoValor):
    user_agent: UserAgent
    ip_address: IPAddress
    referrer: Referrer
    timestamp: str
