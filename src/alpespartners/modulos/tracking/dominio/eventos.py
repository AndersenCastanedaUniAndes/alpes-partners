from alpespartners.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .objetos_valor import TipoConversion, ValorConversion, Metadatos


@dataclass
class ImpresionRegistrada(EventoDominio):
    id: str
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_evento: str
    metadatos: Metadatos
    timestamp: datetime

    def __post_init__(self):
        super().__post_init__()


@dataclass
class ConversionRegistrada(EventoDominio):
    id: str
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_conversion: TipoConversion
    valor: ValorConversion
    metadatos: Metadatos
    timestamp: datetime

    def __post_init__(self):
        super().__post_init__()
