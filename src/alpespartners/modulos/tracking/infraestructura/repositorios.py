from alpespartners.modulos.tracking.dominio.repositorios import RepositorioImpresiones, RepositorioConversiones
from alpespartners.modulos.tracking.dominio.entidades import Impresion, Conversion
from typing import List, Optional
import json


class RepositorioImpresionesInMemory(RepositorioImpresiones):
    def __init__(self):
        self._impresiones: dict = {}

    def obtener_por_id(self, id: str) -> Optional[Impresion]:
        return self._impresiones.get(id)

    def obtener_por_campaña(self, campaña_id: str) -> List[Impresion]:
        return [imp for imp in self._impresiones.values() if imp.campaña_id == campaña_id]

    def agregar(self, impresion: Impresion):
        self._impresiones[impresion.id] = impresion

    def actualizar(self, impresion: Impresion):
        self._impresiones[impresion.id] = impresion


class RepositorioConversionesInMemory(RepositorioConversiones):
    def __init__(self):
        self._conversiones: dict = {}

    def obtener_por_id(self, id: str) -> Optional[Conversion]:
        return self._conversiones.get(id)

    def obtener_por_campaña(self, campaña_id: str) -> List[Conversion]:
        return [conv for conv in self._conversiones.values() if conv.campaña_id == campaña_id]

    def obtener_por_influencer(self, influencer_id: str) -> List[Conversion]:
        return [conv for conv in self._conversiones.values() if conv.influencer_id == influencer_id]

    def agregar(self, conversion: Conversion):
        self._conversiones[conversion.id] = conversion

    def actualizar(self, conversion: Conversion):
        self._conversiones[conversion.id] = conversion
