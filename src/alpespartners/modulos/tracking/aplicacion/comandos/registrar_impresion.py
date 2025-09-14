from dataclasses import dataclass, field
from alpespartners.seedwork.aplicacion.comandos import Comando
from alpespartners.modulos.tracking.dominio.objetos_valor import Metadatos, UserAgent, IPAddress, Referrer
from typing import Optional


@dataclass
class RegistrarImpresion(Comando):
    id: str
    campaña_id: str
    influencer_id: Optional[str] = None
    usuario_id: Optional[str] = None
    tipo_evento: str = "IMPRESION"
    user_agent: str = ""
    ip_address: str = ""
    referrer: str = ""
    timestamp: str = ""
