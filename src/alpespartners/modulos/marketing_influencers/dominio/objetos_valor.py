from alpespartners.seedwork.dominio.objetos_valor import ObjetoValor, Ciudad
from dataclasses import dataclass


@dataclass(frozen=True)
class Nombre(ObjetoValor):
    nombres: str
    apellidos: str


@dataclass(frozen=True)
class Email(ObjetoValor):
    address: str
    dominio: str
    es_empresarial: bool


@dataclass(frozen=True)
class Cedula(ObjetoValor):
    numero: int
    ciudad: Ciudad


class MetodosPago(ObjetoValor):
    # TODO
    ...


@dataclass(frozen=True)
class Plataforma(ObjetoValor):
    nombre: str
    url: str