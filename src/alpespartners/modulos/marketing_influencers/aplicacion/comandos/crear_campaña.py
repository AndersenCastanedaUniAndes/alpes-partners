from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.marketing_influencers.dominio.entidades import Campaña
from .base import CrearReservaBaseHandler
from alpespartners.seedwork.aplicacion.comandos import ejecutar_comando as comando
from alpespartners.modulos.marketing_influencers.aplicacion.mapeadores import MapeadorCampaña


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
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def handle(self, comando: CrearCampaña):
        campaña_dto = Campaña(
            id=comando.id,
            nombre=comando.nombre,
            producto=comando.producto,
            presupuesto=comando.presupuesto,
            moneda=comando.moneda,
            marca=comando.marca
        )

        campaña: Campaña = self.fabrica_campañas.crear_objeto(campaña_dto, MapeadorCampaña())


@comando.register(CrearCampaña)
def ejecutar_comando_crear_campaña(comando: CrearCampaña):
    handler = CrearCampañaHandler()
    handler.handle(comando)
