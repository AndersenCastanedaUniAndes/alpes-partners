from alpespartners.seedwork.dominio.entidades import Entidad
from alpespartners.seedwork.dominio.objetos_valor import Monto
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .objetos_valor import TipoConversion, ValorConversion, Metadatos


@dataclass
class Impresion(Entidad):
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_evento: str
    metadatos: Metadatos
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Conversion(Entidad):
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_conversion: TipoConversion
    valor: ValorConversion
    metadatos: Metadatos
    timestamp: datetime = field(default_factory=datetime.now)
    
    def calcular_comision(self, porcentaje: float) -> float:
        """Calcula la comisión basada en el valor de la conversión"""
        return self.valor.valor * (porcentaje / 100)
