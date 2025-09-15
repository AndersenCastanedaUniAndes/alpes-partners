# Esquemas para eventos de pagos v1

class EsquemaEventoPagoRealizado:
    def __init__(self, pago_id, usuario_id, monto_pagado, moneda, fecha_realizacion, timestamp=None, fecha_creacion=None):
        self.pago_id = pago_id
        self.usuario_id = usuario_id
        self.monto_pagado = monto_pagado
        self.moneda = moneda
        self.fecha_realizacion = fecha_realizacion
        self.timestamp = timestamp
        self.fecha_creacion = fecha_creacion

class EsquemaEventoComisionCalculada:
    def __init__(self, pago_id, monto_comision, moneda, timestamp=None, fecha_creacion=None):
        self.pago_id = pago_id
        self.monto_comision = monto_comision
        self.moneda = moneda
        self.timestamp = timestamp
        self.fecha_creacion = fecha_creacion
