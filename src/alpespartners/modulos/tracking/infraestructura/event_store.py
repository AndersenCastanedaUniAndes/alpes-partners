"""
Event Store centralizado para el módulo de tracking
Implementa Event Sourcing para mantener el estado completo de los eventos
"""
import json
import sqlite3
from datetime import datetime
from typing import List, Optional
from alpespartners.modulos.tracking.dominio.eventos import ImpresionRegistrada, ConversionRegistrada
from alpespartners.seedwork.dominio.eventos import EventoDominio


class EventStore:
    def __init__(self, db_path: str = "tracking_events.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos de eventos"""
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

    def append_event(self, aggregate_id: str, event: EventoDominio, 
                    correlation_id: Optional[str] = None, 
                    causation_id: Optional[str] = None):
        """Agrega un evento al store"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obtener la siguiente versión
        cursor.execute(
            'SELECT MAX(version) FROM events WHERE aggregate_id = ?',
            (aggregate_id,)
        )
        result = cursor.fetchone()
        version = (result[0] or 0) + 1
        
        # Serializar el evento
        event_data = self._serialize_event(event)
        
        cursor.execute('''
            INSERT INTO events (aggregate_id, event_type, event_data, version, correlation_id, causation_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (aggregate_id, event.__class__.__name__, event_data, version, correlation_id, causation_id))
        
        conn.commit()
        conn.close()

    def get_events(self, aggregate_id: str) -> List[EventoDominio]:
        """Obtiene todos los eventos de un agregado"""
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

    def get_events_by_type(self, event_type: str, limit: int = 100) -> List[EventoDominio]:
        """Obtiene eventos por tipo"""
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

    def _serialize_event(self, event: EventoDominio) -> str:
        """Serializa un evento a JSON"""
        return json.dumps(event.__dict__, default=str)

    def _deserialize_event(self, event_type: str, event_data: str) -> EventoDominio:
        """Deserializa un evento desde JSON"""
        data = json.loads(event_data)
        
        if event_type == "ImpresionRegistrada":
            return ImpresionRegistrada(**data)
        elif event_type == "ConversionRegistrada":
            return ConversionRegistrada(**data)
        else:
            raise ValueError(f"Tipo de evento desconocido: {event_type}")


class EventStoreRepository:
    """Repositorio que usa Event Store para reconstruir agregados"""
    
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def save_impresion(self, impresion_id: str, event: ImpresionRegistrada):
        """Guarda una impresión usando Event Store"""
        self.event_store.append_event(impresion_id, event)

    def save_conversion(self, conversion_id: str, event: ConversionRegistrada):
        """Guarda una conversión usando Event Store"""
        self.event_store.append_event(conversion_id, event)

    def get_impresion_events(self, impresion_id: str) -> List[ImpresionRegistrada]:
        """Obtiene eventos de una impresión"""
        events = self.event_store.get_events(impresion_id)
        return [e for e in events if isinstance(e, ImpresionRegistrada)]

    def get_conversion_events(self, conversion_id: str) -> List[ConversionRegistrada]:
        """Obtiene eventos de una conversión"""
        events = self.event_store.get_events(conversion_id)
        return [e for e in events if isinstance(e, ConversionRegistrada)]
