from alpespartners.modulos.pagos.dominio.entidades import Pago, Comision
from alpespartners.modulos.pagos.dominio.eventos import ComisionCalculada, PagoProgramado, PagoRealizado
import requests

class HandlerCalcularComision:
    def handle(self, comando):
        # Ejemplo de lógica para calcular comisión
        porcentaje = 10  # Porcentaje fijo de ejemplo
        monto_comision = comando.monto * (porcentaje / 100)
        evento = ComisionCalculada(
            pago_id=comando.pago_id,
            monto_comision=monto_comision,
            moneda=comando.moneda
        )
        return evento

class HandlerProgramarPago:
    def handle(self, comando):
        # Simulación de envío de datos a servicio externo de pagos
        datos_pago = {
            "usuario_id": comando.usuario_id,
            "nombre": comando.nombre,
            "email": comando.email,
            "monto": comando.monto,
            "moneda": comando.moneda,
            "tarjeta": {
                "numero": comando.numero_tarjeta,
                "expiracion": comando.expiracion,
                "cvv": comando.cvv
            }
        }
        # Simulación de llamada a API externa (puedes cambiar la URL por la real)
        try:
            response = requests.post("https://api-externa-pagos.com/efectuar-pago", json=datos_pago)
            if response.status_code == 200:
                print("✅ Pago realizado correctamente")
                evento = PagoRealizado(
                    pago_id=comando.pago_id,
                    usuario_id=comando.usuario_id,
                    monto_pagado=comando.monto,
                    moneda=comando.moneda,
                    fecha_realizacion=comando.fecha_programada
                )
                return evento
            else:
                print("❌ Error en el pago:", response.text)
                return None
        except Exception as e:
            print("❌ Error de conexión con el servicio externo:", e)
            return None
