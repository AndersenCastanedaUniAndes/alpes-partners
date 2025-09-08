from alpespartners.seedwork.dominio.entidades import Entidad
from alpespartners.seedwork.dominio.objetos_valor import Monto, EstadoPago
from dataclasses import dataclass, field
from datetime import datetime

from .objetos_valor import Nombre, Email, Cedula


@dataclass
class Conversion(Entidad):
    campaña_id: str
    influencer_id: str
    monto: Monto


@dataclass
class Influencer(Entidad):
    nombre: Nombre
    email: Email
    cedula: Cedula
    plataforma: str
    audiencia: int
    activo: bool = True
    fecha_nacimiento: datetime = field(default_factory=datetime)

    def desactivar(self):
        self.activo = False
        self.fecha_actualizacion = datetime.now()


@dataclass
class Campaña(Entidad):
    nombre: str
    producto: str
    presupuesto: Monto
    marca: str
    influencers_ids: list[str]
    conversiones: list


@dataclass
class Pago(Entidad):
    influencer_id: str
    campaña_id: str
    monto: Monto
    estado: EstadoPago = EstadoPago.PENDIENTE

