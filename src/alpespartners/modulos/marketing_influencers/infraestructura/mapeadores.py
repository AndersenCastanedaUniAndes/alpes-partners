from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.marketing_influencers.dominio.entidades import Campaña
from .dto import CampañaDTO

class MapeadorCampaña(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Campaña.__class__

    def entidad_a_dto(self, entidad: Campaña) -> CampañaDTO:
        return None

    def dto_a_entidad(self, dto: CampañaDTO) -> Campaña:
        return None