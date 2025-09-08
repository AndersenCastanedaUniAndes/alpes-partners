from alpespartners.seedwork.dominio.excepciones import ExcepcionFabrica


class TipoObjetoNoExisteEnDominioMarketingDeInfluencersExcepcion(ExcepcionFabrica):
    def __init__(self, mensaje='No existe una fábrica para el tipo solicitado en el módulo de Marketing de Influencers'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)
