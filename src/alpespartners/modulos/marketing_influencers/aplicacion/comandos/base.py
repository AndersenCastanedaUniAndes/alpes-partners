from alpespartners.seedwork.aplicacion.comandos import ComandoHandler

class CrearReservaBaseHandler(ComandoHandler):
    def __init__(self):
        self.fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()