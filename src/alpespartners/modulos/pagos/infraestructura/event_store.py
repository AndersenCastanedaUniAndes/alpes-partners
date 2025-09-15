import json
import sqlite3
from datetime import datetime
from typing import List, Optional
from alpespartners.modulos.pagos.dominio.eventos import PagoRealizado, ComisionCalculada
from alpespartners.seedwork.dominio.eventos import EventoDominio

class EventStorePagos:
    def __init__(self, db_path: str = "pagos_events.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aggregate_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_data TEXT NOT NULL,
                version INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                correlation_id TEXT,
                causation_id TEXT
            )
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_aggregate_id ON events(aggregate_id)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_event_type ON events(event_type)
        ''')
        conn.commit()
        conn.close()

    def guardar_evento(self, aggregate_id: str, evento: EventoDominio, 
                      correlation_id: Optional[str] = None, 
                      causation_id: Optional[str] = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT MAX(version) FROM events WHERE aggregate_id = ?',
            (aggregate_id,)
        )
        result = cursor.fetchone()
        version = (result[0] or 0) + 1
        event_data = self._serialize_event(evento)
        cursor.execute('''
            INSERT INTO events (aggregate_id, event_type, event_data, version, correlation_id, causation_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (aggregate_id, evento.__class__.__name__, event_data, version, correlation_id, causation_id))
        conn.commit()
        conn.close()

    def obtener_eventos(self, aggregate_id: str) -> List[EventoDominio]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT event_type, event_data, version, timestamp
            FROM events 
            WHERE aggregate_id = ?
            ORDER BY version
        ''', (aggregate_id,))
        events = []
        for row in cursor.fetchall():
            event_type, event_data, version, timestamp = row
            event = self._deserialize_event(event_type, event_data)
            events.append(event)
        conn.close()
        return events

    def obtener_eventos_por_tipo(self, event_type: str, limit: int = 100) -> List[EventoDominio]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT event_data, timestamp
            FROM events 
            WHERE event_type = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (event_type, limit))
        events = []
        for row in cursor.fetchall():
            event_data, timestamp = row
            event = self._deserialize_event(event_type, event_data)
            events.append(event)
        conn.close()
        return events

    def _serialize_event(self, evento: EventoDominio) -> str:
        return json.dumps(evento.__dict__, default=str)

    def _deserialize_event(self, event_type: str, event_data: str) -> EventoDominio:
        data = json.loads(event_data)
        if event_type == "PagoRealizado":
            return PagoRealizado(**data)
        elif event_type == "ComisionCalculada":
            return ComisionCalculada(**data)
        else:
            raise ValueError(f"Tipo de evento desconocido: {event_type}")

class EventStorePagosRepository:
    def __init__(self, event_store: EventStorePagos):
        self.event_store = event_store

    def save_pago(self, pago_id: str, evento: PagoRealizado):
        self.event_store.guardar_evento(pago_id, evento)

    def save_comision(self, pago_id: str, evento: ComisionCalculada):
        self.event_store.guardar_evento(pago_id, evento)

    def get_pago_events(self, pago_id: str) -> List[PagoRealizado]:
        events = self.event_store.obtener_eventos(pago_id)
        return [e for e in events if isinstance(e, PagoRealizado)]

    def get_comision_events(self, pago_id: str) -> List[ComisionCalculada]:
        events = self.event_store.obtener_eventos(pago_id)
        return [e for e in events if isinstance(e, ComisionCalculada)]
