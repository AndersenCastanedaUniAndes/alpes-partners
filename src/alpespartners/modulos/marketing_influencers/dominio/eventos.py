from dataclasses import dataclass
from alpespartners.seedwork.dominio.eventos import EventoDominio

@dataclass
class CampañaCreada(EventoDominio):
    id_campaña: str
    id_cliente: str
    estado: str
    fecha_creacion: str


@dataclass
class ReservaCancelada(EventoDominio):
    id_reserva: str
    fecha_actualizacion: str


@dataclass
class ReservaAprobada(EventoDominio):
    id_reserva: str
    fecha_actualizacion: str
