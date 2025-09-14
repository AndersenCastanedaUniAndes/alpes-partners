import time
from .consumidor_pagos import ConsumidorPagos
from .consumidor_comisiones import ConsumidorComisiones

class ConsumidoresPagos:
    def __init__(self, broker_url=None):
        self.consumidor_pagos = ConsumidorPagos(broker_url)
        self.consumidor_comisiones = ConsumidorComisiones(broker_url)

    def consumir_todos(self):
        print("Iniciando consumidores de pagos y comisiones...")
        self.consumidor_pagos.consumir()
        self.consumidor_comisiones.consumir()

class ConsumidorPagos:
    def __init__(self, broker_url=None):
        self.broker_url = broker_url or "pulsar://localhost:6650"

    def consumir(self):
        print(f"🔄 Suscrito al broker de pagos en {self.broker_url}")
        while True:
            # Simulación de consumo de eventos
            print("⏳ Esperando eventos de pagos...")
            # Aquí iría la lógica real de suscripción y procesamiento
            time.sleep(5)
            print("🔔 Evento de pago recibido y procesado!")
            # Procesar el evento, actualizar modelos, despachar eventos, etc.
            # ...
            # Romper el ciclo en un entorno real o por condición
            break
