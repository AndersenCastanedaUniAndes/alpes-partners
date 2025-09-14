"""
Read Models descentralizados para el módulo de tracking
Implementa CQRS con proyecciones específicas para consultas
"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ImpresionReadModel:
    id: str
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_evento: str
    user_agent: str
    ip_address: str
    referrer: str
    timestamp: datetime
    created_at: datetime


@dataclass
class ConversionReadModel:
    id: str
    campaña_id: str
    influencer_id: Optional[str]
    usuario_id: Optional[str]
    tipo_conversion: str
    valor: float
    moneda: str
    user_agent: str
    ip_address: str
    referrer: str
    timestamp: datetime
    created_at: datetime


@dataclass
class CampañaStatsReadModel:
    campaña_id: str
    total_impresiones: int
    total_conversiones: int
    valor_total_conversiones: float
    tasa_conversion: float
    ultima_actualizacion: datetime


class ImpresionReadModelRepository:
    """Repositorio para consultas de impresiones"""
    
    def __init__(self, db_path: str = "tracking_read_models.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos de read models"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS impresiones_read_model (
                id TEXT PRIMARY KEY,
                campaña_id TEXT NOT NULL,
                influencer_id TEXT,
                usuario_id TEXT,
                tipo_evento TEXT NOT NULL,
                user_agent TEXT,
                ip_address TEXT,
                referrer TEXT,
                timestamp DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_impresiones_campaña ON impresiones_read_model(campaña_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_impresiones_influencer ON impresiones_read_model(influencer_id)
        ''')
        
        conn.commit()
        conn.close()

    def save_impresion(self, impresion: ImpresionReadModel):
        """Guarda una impresión en el read model"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO impresiones_read_model 
            (id, campaña_id, influencer_id, usuario_id, tipo_evento, user_agent, ip_address, referrer, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            impresion.id, impresion.campaña_id, impresion.influencer_id, impresion.usuario_id,
            impresion.tipo_evento, impresion.user_agent, impresion.ip_address, impresion.referrer,
            impresion.timestamp, impresion.created_at
        ))
        
        conn.commit()
        conn.close()

    def get_impresion(self, impresion_id: str) -> Optional[ImpresionReadModel]:
        """Obtiene una impresión por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, campaña_id, influencer_id, usuario_id, tipo_evento, user_agent, ip_address, referrer, timestamp, created_at
            FROM impresiones_read_model WHERE id = ?
        ''', (impresion_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return ImpresionReadModel(*row)
        return None

    def get_impresiones_by_campaña(self, campaña_id: str) -> List[ImpresionReadModel]:
        """Obtiene impresiones por campaña"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, campaña_id, influencer_id, usuario_id, tipo_evento, user_agent, ip_address, referrer, timestamp, created_at
            FROM impresiones_read_model WHERE campaña_id = ?
            ORDER BY timestamp DESC
        ''', (campaña_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [ImpresionReadModel(*row) for row in rows]

    def get_impresiones_by_influencer(self, influencer_id: str) -> List[ImpresionReadModel]:
        """Obtiene impresiones por influencer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, campaña_id, influencer_id, usuario_id, tipo_evento, user_agent, ip_address, referrer, timestamp, created_at
            FROM impresiones_read_model WHERE influencer_id = ?
            ORDER BY timestamp DESC
        ''', (influencer_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [ImpresionReadModel(*row) for row in rows]


class ConversionReadModelRepository:
    """Repositorio para consultas de conversiones"""
    
    def __init__(self, db_path: str = "tracking_read_models.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos de read models"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversiones_read_model (
                id TEXT PRIMARY KEY,
                campaña_id TEXT NOT NULL,
                influencer_id TEXT,
                usuario_id TEXT,
                tipo_conversion TEXT NOT NULL,
                valor REAL NOT NULL,
                moneda TEXT NOT NULL,
                user_agent TEXT,
                ip_address TEXT,
                referrer TEXT,
                timestamp DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversiones_campaña ON conversiones_read_model(campaña_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversiones_influencer ON conversiones_read_model(influencer_id)
        ''')
        
        conn.commit()
        conn.close()

    def save_conversion(self, conversion: ConversionReadModel):
        """Guarda una conversión en el read model"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO conversiones_read_model 
            (id, campaña_id, influencer_id, usuario_id, tipo_conversion, valor, moneda, user_agent, ip_address, referrer, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            conversion.id, conversion.campaña_id, conversion.influencer_id, conversion.usuario_id,
            conversion.tipo_conversion, conversion.valor, conversion.moneda, conversion.user_agent,
            conversion.ip_address, conversion.referrer, conversion.timestamp, conversion.created_at
        ))
        
        conn.commit()
        conn.close()

    def get_conversion(self, conversion_id: str) -> Optional[ConversionReadModel]:
        """Obtiene una conversión por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, campaña_id, influencer_id, usuario_id, tipo_conversion, valor, moneda, user_agent, ip_address, referrer, timestamp, created_at
            FROM conversiones_read_model WHERE id = ?
        ''', (conversion_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return ConversionReadModel(*row)
        return None

    def get_conversiones_by_campaña(self, campaña_id: str) -> List[ConversionReadModel]:
        """Obtiene conversiones por campaña"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, campaña_id, influencer_id, usuario_id, tipo_conversion, valor, moneda, user_agent, ip_address, referrer, timestamp, created_at
            FROM conversiones_read_model WHERE campaña_id = ?
            ORDER BY timestamp DESC
        ''', (campaña_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [ConversionReadModel(*row) for row in rows]

    def get_conversiones_by_influencer(self, influencer_id: str) -> List[ConversionReadModel]:
        """Obtiene conversiones por influencer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, campaña_id, influencer_id, usuario_id, tipo_conversion, valor, moneda, user_agent, ip_address, referrer, timestamp, created_at
            FROM conversiones_read_model WHERE influencer_id = ?
            ORDER BY timestamp DESC
        ''', (influencer_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [ConversionReadModel(*row) for row in rows]


class CampañaStatsReadModelRepository:
    """Repositorio para estadísticas de campañas"""
    
    def __init__(self, db_path: str = "tracking_read_models.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos de estadísticas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaña_stats_read_model (
                campaña_id TEXT PRIMARY KEY,
                total_impresiones INTEGER DEFAULT 0,
                total_conversiones INTEGER DEFAULT 0,
                valor_total_conversiones REAL DEFAULT 0.0,
                tasa_conversion REAL DEFAULT 0.0,
                ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def update_stats(self, campaña_id: str, impresiones: int, conversiones: int, valor_total: float):
        """Actualiza las estadísticas de una campaña"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tasa_conversion = (conversiones / impresiones * 100) if impresiones > 0 else 0
        
        cursor.execute('''
            INSERT OR REPLACE INTO campaña_stats_read_model 
            (campaña_id, total_impresiones, total_conversiones, valor_total_conversiones, tasa_conversion, ultima_actualizacion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (campaña_id, impresiones, conversiones, valor_total, tasa_conversion, datetime.now()))
        
        conn.commit()
        conn.close()

    def get_stats(self, campaña_id: str) -> Optional[CampañaStatsReadModel]:
        """Obtiene estadísticas de una campaña"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT campaña_id, total_impresiones, total_conversiones, valor_total_conversiones, tasa_conversion, ultima_actualizacion
            FROM campaña_stats_read_model WHERE campaña_id = ?
        ''', (campaña_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return CampañaStatsReadModel(*row)
        return None
