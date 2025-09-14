import time

class ConsumidorComisiones:
    def __init__(self, broker_url=None):
        self.broker_url = broker_url or "pulsar://localhost:6650"

    def consumir(self):
        print(f"🔄 Suscrito al broker de comisiones en {self.broker_url}")
        while True:
            print("⏳ Esperando eventos de comisiones...")
            # Simulación de procesamiento de evento ComisionCalculada
            time.sleep(5)
            print("🔔 Evento de comisión procesado!")
            # Aquí iría la lógica real de procesamiento
            break
