from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.tracking.dominio.objetos_valor import TipoConversion, ValorConversion, Metadatos, UserAgent, IPAddress, Referrer
from typing import Optional


@dataclass
class RegistrarConversion(Comando):
    id: str
    campaña_id: str
    influencer_id: Optional[str] = None
    usuario_id: Optional[str] = None
    tipo_conversion: str = "VENTA"
    valor: float = 0.0
    moneda: str = "COP"
    user_agent: str = ""
    ip_address: str = ""
    referrer: str = ""
    timestamp: str = ""
