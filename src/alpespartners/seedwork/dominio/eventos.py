from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EventoDominio(ABC):
    """Clase base para eventos de dominio"""
    fecha_creacion: datetime = None
    
    def __post_init__(self):
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now()


# Comandos
crear_campaña = "crear-campaña";
registrar_impresión = "registrar-impresión";
registrar_conversión = "registrar-conversión";
calcular_comisión = "calcular-comisión";
procesar_pago = "procesar-pago";

# Eventos
campaña_creada = "campaña-creada";
impresión_registrada = "impresión-registrada";
conversión_registrada = "conversión-registrada";
comisión_calculada = "comisión-calculada";
pago_procesado = "pago-procesado";
