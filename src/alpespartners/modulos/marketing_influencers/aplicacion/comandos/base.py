from alpespartners.seedwork.aplicacion.comandos import ComandoHandler
from alpespartners.modulos.marketing_influencers.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.marketing_influencers.dominio.fabricas import FabricaMarketingDeInfluencers

class CrearReservaBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_campañas: FabricaMarketingDeInfluencers = FabricaMarketingDeInfluencers()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_campañas(self):
        return self._fabrica_campañas