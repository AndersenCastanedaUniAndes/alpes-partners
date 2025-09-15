from alpespartners.seedwork.aplicacion.comandos import ComandoHandler
from alpespartners.modulos.marketing_influencers.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.marketing_influencers.dominio.fabricas import FabricaMarketingDeInfluencers

class CrearReservaBaseHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_repositorio = FabricaRepositorio()
        self.fabrica_campañas = FabricaMarketingDeInfluencers()

    @property
    def fabrica_repositorio(self):
        return self.fabrica_repositorio

    @property
    def fabrica_campaña(self):
        return self.fabrica_campañas