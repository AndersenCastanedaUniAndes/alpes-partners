from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ImpresionDTO:
    id: str
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_evento: str
    user_agent: str
    ip_address: str
    referrer: str
    timestamp: str


@dataclass
class ConversionDTO:
    id: str
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_conversion: str
    valor: float
    moneda: str
    user_agent: str
    ip_address: str
    referrer: str
    timestamp: str
