from abc import ABC, abstractmethod
from alpespartners.modulos.pagos.dominio.entidades import Pago, Comision
from typing import List, Optional

class RepositorioPagos(ABC):
    @abstractmethod
    def obtener_por_id(self, pago_id: str) -> Optional[Pago]:
        pass

    @abstractmethod
    def obtener_por_usuario(self, usuario_id: str) -> List[Pago]:
        pass

    @abstractmethod
    def agregar(self, pago: Pago):
        pass

    @abstractmethod
    def actualizar(self, pago: Pago):
        pass

class RepositorioComisiones(ABC):
    @abstractmethod
    def obtener_por_id(self, pago_id: str) -> Optional[Comision]:
        pass

    @abstractmethod
    def obtener_por_usuario(self, usuario_id: str) -> List[Comision]:
        pass

    @abstractmethod
    def agregar(self, comision: Comision):
        pass

    @abstractmethod
    def actualizar(self, comision: Comision):
        pass
