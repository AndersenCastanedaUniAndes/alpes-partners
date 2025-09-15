import sqlite3
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class PagoReadModel:
    pago_id: str
    usuario_id: str
    monto_pagado: float
    moneda: str
    fecha_realizacion: str
    timestamp: datetime

@dataclass
class ComisionReadModel:
    pago_id: str
    monto_comision: float
    moneda: str
    timestamp: datetime

class PagoReadModelRepository:
    def __init__(self, db_path: str = "pagos_read_models.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pagos_read_model (
                pago_id TEXT PRIMARY KEY,
                usuario_id TEXT,
                monto_pagado REAL,
                moneda TEXT,
                fecha_realizacion TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def save_pago(self, pago: PagoReadModel):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO pagos_read_model 
            (pago_id, usuario_id, monto_pagado, moneda, fecha_realizacion, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            pago.pago_id, pago.usuario_id, pago.monto_pagado, pago.moneda, pago.fecha_realizacion, pago.timestamp
        ))
        conn.commit()
        conn.close()

    def get_pago(self, pago_id: str) -> Optional[PagoReadModel]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pago_id, usuario_id, monto_pagado, moneda, fecha_realizacion, timestamp
            FROM pagos_read_model WHERE pago_id = ?
        ''', (pago_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return PagoReadModel(*row)
        return None

    def get_pagos_by_usuario(self, usuario_id: str) -> List[PagoReadModel]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pago_id, usuario_id, monto_pagado, moneda, fecha_realizacion, timestamp
            FROM pagos_read_model WHERE usuario_id = ?
            ORDER BY timestamp DESC
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [PagoReadModel(*row) for row in rows]

class ComisionReadModelRepository:
    def __init__(self, db_path: str = "pagos_read_models.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comisiones_read_model (
                pago_id TEXT PRIMARY KEY,
                monto_comision REAL,
                moneda TEXT,
                timestamp DATETIME
            )
        ''')
        conn.commit()
        conn.close()

    def save_comision(self, comision: ComisionReadModel):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO comisiones_read_model 
            (pago_id, monto_comision, moneda, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (
            comision.pago_id, comision.monto_comision, comision.moneda, comision.timestamp
        ))
        conn.commit()
        conn.close()

    def get_comision(self, pago_id: str) -> Optional[ComisionReadModel]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pago_id, monto_comision, moneda, timestamp
            FROM comisiones_read_model WHERE pago_id = ?
        ''', (pago_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return ComisionReadModel(*row)
        return None

    def get_comisiones_by_usuario(self, usuario_id: str) -> List[ComisionReadModel]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pago_id, monto_comision, moneda, timestamp
            FROM comisiones_read_model WHERE pago_id IN (
                SELECT pago_id FROM pagos_read_model WHERE usuario_id = ?
            )
            ORDER BY timestamp DESC
        ''', (usuario_id,))
        rows = cursor.fetchall()
        conn.close()
        return [ComisionReadModel(*row) for row in rows]
