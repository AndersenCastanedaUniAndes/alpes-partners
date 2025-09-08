from abc import ABC
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


@dataclass(frozen=True)
class ObjetoValor:
    ...


@dataclass(frozen=True)
class Codigo(ABC, ObjetoValor):
    codigo: str


@dataclass(frozen=True)
class Pais(ObjetoValor):
    codigo: Codigo
    nombre: str


@dataclass(frozen=True)
class Ciudad(ObjetoValor):
    pais: Pais
    codigo: Codigo
    nombre: str


class EstadoPago(Enum):
    PENDIENTE = "PENDIENTE"
    PROCESANDO = "PROCESANDO"
    COMPLETADO = "COMPLETADO"
    FALLIDO = "FALLIDO"


class Moneda(Enum):
    COP = "COP"
    USD = "USD"
    EUR = "EUR"

@dataclass(frozen=True)
class Monto:
    valor: Decimal
    moneda: Moneda

