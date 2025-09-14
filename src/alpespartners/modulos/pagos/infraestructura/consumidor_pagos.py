import time

class ConsumidorPagos:
    def __init__(self, broker_url=None):
        self.broker_url = broker_url or "pulsar://localhost:6650"

    def consumir(self):
        print(f"🔄 Suscrito al broker de pagos en {self.broker_url}")
        while True:
            print("⏳ Esperando eventos de pagos...")
            # Simulación de procesamiento de evento PagoProgramado/PagoRealizado
            time.sleep(5)
            print("🔔 Evento de pago procesado!")
            # Aquí iría la lógica real de procesamiento
            break
