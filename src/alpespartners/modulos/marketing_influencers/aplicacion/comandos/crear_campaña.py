from dataclasses import dataclass, field
from alpespartners.modulos.marketing_influencers.aplicacion.dto import CampañaDTO
from alpespartners.seedwork.aplicacion.comandos import Comando
from .base import CrearReservaBaseHandler
from alpespartners.seedwork.aplicacion.comandos import ejecutar_comando as comando
from alpespartners.modulos.marketing_influencers.infraestructura.repositorios import RepositorioCampañasDB


@dataclass
class CrearCampaña(Comando):
    id: str
    nombre: str
    producto: str
    presupuesto: float
    moneda: str
    marca: str
    influencers_ids: list[str] = field(default_factory=list)
    conversiones: list = field(default_factory=list)


class CrearCampañaHandler(CrearReservaBaseHandler):
    def handle(self, comando: CrearCampaña):
        campaña_dto = CampañaDTO(
            id=comando.id,
            nombre=comando.nombre,
            producto=comando.producto,
            presupuesto=comando.presupuesto,
            moneda=comando.moneda,
            marca=comando.marca,
            influencers_ids=comando.influencers_ids,
            conversiones=comando.conversiones
        )

        repositorio = RepositorioCampañasDB()
        repositorio.agregar(campaña_dto)


@comando.register(CrearCampaña)
def ejecutar_comando_crear_campaña(comando: CrearCampaña):
    handler = CrearCampañaHandler()
    handler.handle(comando)
