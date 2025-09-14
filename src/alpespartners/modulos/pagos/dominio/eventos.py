from alpespartners.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ComisionCalculada(EventoDominio):
    pago_id: str
    monto_comision: float
    moneda: str = "COP"
    timestamp: datetime = None
    fecha_creacion: datetime = None
    def __post_init__(self):
        super().__post_init__()

@dataclass
class PagoProgramado(EventoDominio):
    pago_id: str
    usuario_id: Optional[str] = None
    monto: float = 0.0
    moneda: str = "COP"
    fecha_programada: Optional[str] = None
    timestamp: datetime = None
    fecha_creacion: datetime = None
    def __post_init__(self):
        super().__post_init__()

@dataclass
class PagoRealizado(EventoDominio):
    pago_id: str
    usuario_id: Optional[str] = None
    monto_pagado: float = 0.0
    moneda: str = "COP"
    fecha_realizacion: Optional[str] = None
    timestamp: datetime = None
    fecha_creacion: datetime = None
    def __post_init__(self):
        super().__post_init__()
