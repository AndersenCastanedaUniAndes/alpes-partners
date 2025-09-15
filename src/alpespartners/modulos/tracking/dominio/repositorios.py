from abc import ABC, abstractmethod
from alpespartners.modulos.tracking.dominio.entidades import Impresion, Conversion
from typing import List, Optional


class RepositorioImpresiones(ABC):
    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Impresion]:
        pass

    @abstractmethod
    def obtener_por_campaña(self, campaña_id: str) -> List[Impresion]:
        pass

    @abstractmethod
    def agregar(self, impresion: Impresion):
        pass

    @abstractmethod
    def actualizar(self, impresion: Impresion):
        pass


class RepositorioConversiones(ABC):
    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Conversion]:
        pass

    @abstractmethod
    def obtener_por_campaña(self, campaña_id: str) -> List[Conversion]:
        pass

    @abstractmethod
    def obtener_por_influencer(self, influencer_id: str) -> List[Conversion]:
        pass

    @abstractmethod
    def agregar(self, conversion: Conversion):
        pass

    @abstractmethod
    def actualizar(self, conversion: Conversion):
        pass
