from alpespartners.modulos.pagos.dominio.repositorios import RepositorioPagos, RepositorioComisiones
from alpespartners.modulos.pagos.dominio.entidades import Pago, Comision
from typing import List, Optional

class RepositorioPagosInMemory(RepositorioPagos):
    def __init__(self):
        self._pagos: dict = {}

    def obtener_por_id(self, pago_id: str) -> Optional[Pago]:
        return self._pagos.get(pago_id)

    def obtener_por_usuario(self, usuario_id: str) -> List[Pago]:
        return [p for p in self._pagos.values() if p.usuario_id == usuario_id]

    def agregar(self, pago: Pago):
        self._pagos[pago.pago_id] = pago

    def actualizar(self, pago: Pago):
        self._pagos[pago.pago_id] = pago

class RepositorioComisionesInMemory(RepositorioComisiones):
    def __init__(self):
        self._comisiones: dict = {}

    def obtener_por_id(self, pago_id: str) -> Optional[Comision]:
        return self._comisiones.get(pago_id)

    def obtener_por_usuario(self, usuario_id: str) -> List[Comision]:
        return [c for c in self._comisiones.values() if c.pago_id in self._pagos_by_usuario(usuario_id)]

    def agregar(self, comision: Comision):
        self._comisiones[comision.pago_id] = comision

    def actualizar(self, comision: Comision):
        self._comisiones[comision.pago_id] = comision

    def _pagos_by_usuario(self, usuario_id: str) -> List[str]:
        # Simula obtener los pagos por usuario (debería integrarse con RepositorioPagos)
        return [pago_id for pago_id, com in self._comisiones.items() if com.usuario_id == usuario_id]
