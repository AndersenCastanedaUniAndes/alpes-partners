# Esquemas para comandos de pagos v1

class EsquemaComandoProgramarPago:
    def __init__(self, pago_id, usuario_id, nombre, email, monto, moneda, numero_tarjeta, expiracion, cvv, fecha_programada):
        self.pago_id = pago_id
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.email = email
        self.monto = monto
        self.moneda = moneda
        self.numero_tarjeta = numero_tarjeta
        self.expiracion = expiracion
        self.cvv = cvv
        self.fecha_programada = fecha_programada

class EsquemaComandoCalcularComision:
    def __init__(self, pago_id, usuario_id, monto, moneda, fecha_programada):
        self.pago_id = pago_id
        self.usuario_id = usuario_id
        self.monto = monto
        self.moneda = moneda
        self.fecha_programada = fecha_programada
