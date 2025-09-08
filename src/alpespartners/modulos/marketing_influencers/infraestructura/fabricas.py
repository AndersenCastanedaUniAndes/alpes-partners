from dataclasses import dataclass
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.seedwork.dominio.repositorios import Repositorio
from alpespartners.seedwork.dominio.excepciones import ExcepcionFabrica
from alpespartners.modulos.marketing_influencers.dominio.repositorios import RepositorioCampañas
from .repositorios import RepositorioCampañasDB


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioCampañas.__class__:
            return RepositorioCampañasDB()
        # elif obj == RepositorioProveedores.__class__:
        #     return RepositorioProveedoresSQLite()
        else:
            raise ExcepcionFabrica()
