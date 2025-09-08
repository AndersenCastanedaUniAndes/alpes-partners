from dataclasses import dataclass
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.seedwork.dominio.entidades import Entidad
from alpespartners.seedwork.dominio.reglas import ReglaSiempreValida
from .entidades import Campaña
from .excepciones import TipoObjetoNoExisteEnDominioMarketingDeInfluencersExcepcion


@dataclass
class _FabricaCampañas(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            campaña: Campaña = mapeador.dto_a_entidad(obj)

            self.validar_regla(ReglaSiempreValida)

            return campaña


@dataclass
class FabricaMarketingDeInfluencers(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Campaña.__class__:
            fabrica_reserva = _FabricaCampañas()
            return fabrica_reserva.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioMarketingDeInfluencersExcepcion()
