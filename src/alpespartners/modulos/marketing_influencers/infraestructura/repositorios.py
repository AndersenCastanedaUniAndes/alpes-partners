from alpespartners.config.db import db
from alpespartners.modulos.marketing_influencers.dominio.fabricas import FabricaCampañas
from alpespartners.modulos.marketing_influencers.dominio.repositorios import RepositorioCampañas
from .mapeadores import MapeadorCampaña

class RepositorioCampañasDB(RepositorioCampañas):

    def __init__(self):
        self._fabrica_campaña: FabricaCampaña = FabricaCampaña()

    @property
    def fabrica_campaña(self):
        return self._fabrica_campaña

    def obtener_por_id(self, id: UUID) -> Campaña:
        reserva_dto = db.session.query(CampañaDTO).filter_by(id=str(id)).one()
        return self.fabrica_campaña.crear_objeto(reserva_dto, MapeadorCampaña())

    def obtener_todos(self) -> list[Campaña]:
        # TODO
        raise NotImplementedError

    def agregar(self, reserva: Campaña):
        campaña_dto = self.fabrica_campaña.crear_objeto(reserva, MapeadorCampaña())
        db.session.add(campaña_dto)

    def actualizar(self, reserva: Campaña):
        # TODO
        raise NotImplementedError

    def eliminar(self, reserva_id: UUID):
        # TODO
        raise NotImplementedError