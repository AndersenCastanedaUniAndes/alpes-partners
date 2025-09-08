from abc import ABC
from alpespartners.seedwork.dominio.repositorios import Repositorio


class RepositorioCampañas(Repositorio, ABC):
    ...


class RepositorioInfluencer(Repositorio, ABC):
    ...
