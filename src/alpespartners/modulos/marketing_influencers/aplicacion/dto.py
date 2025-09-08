from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CampañaDTO:
    id: str
    nombre: str
    producto: str
    presupuesto: float
    moneda: str
    marca: str
    influencers_ids: list[str]
    conversiones: list
