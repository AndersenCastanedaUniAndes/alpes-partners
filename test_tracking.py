#!/usr/bin/env python3
"""
Script de prueba para el módulo de tracking
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Prueba el endpoint de health check"""
    print("🔍 Probando health check...")
    response = requests.get(f"{BASE_URL}/tracking/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_registrar_impresion():
    """Prueba el registro de una impresión"""
    print("📊 Probando registro de impresión...")
    
    impresion_data = {
        "id": f"imp-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "campaña_id": "cmp-123",
        "influencer_id": "inf-456",
        "usuario_id": "usr-789",
        "tipo_evento": "IMPRESION",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "ip_address": "192.168.1.100",
        "referrer": "https://instagram.com/p/abc123",
        "timestamp": datetime.now().isoformat()
    }
    
    response = requests.post(
        f"{BASE_URL}/tracking/impresiones",
        json=impresion_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_registrar_conversion():
    """Prueba el registro de una conversión"""
    print("💰 Probando registro de conversión...")
    
    conversion_data = {
        "id": f"conv-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "campaña_id": "cmp-123",
        "influencer_id": "inf-456",
        "usuario_id": "usr-789",
        "tipo_conversion": "VENTA",
        "valor": 250000.0,
        "moneda": "COP",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "ip_address": "192.168.1.100",
        "referrer": "https://instagram.com/p/abc123",
        "timestamp": datetime.now().isoformat()
    }
    
    response = requests.post(
        f"{BASE_URL}/tracking/conversiones",
        json=conversion_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_consultar_impresiones_campaña():
    """Prueba la consulta de impresiones por campaña"""
    print("📈 Probando consulta de impresiones por campaña...")
    
    response = requests.get(f"{BASE_URL}/tracking/campañas/cmp-123/impresiones")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_consultar_conversiones_campaña():
    """Prueba la consulta de conversiones por campaña"""
    print("📊 Probando consulta de conversiones por campaña...")
    
    response = requests.get(f"{BASE_URL}/tracking/campañas/cmp-123/conversiones")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    print("🚀 Iniciando pruebas del módulo de tracking...")
    print("=" * 50)
    
    try:
        test_health()
        test_registrar_impresion()
        test_registrar_conversion()
        test_consultar_impresiones_campaña()
        test_consultar_conversiones_campaña()
        
        print("✅ Todas las pruebas completadas!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
