#!/usr/bin/env python3
"""
Script de prueba simple para el módulo de tracking
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(url, method="GET", data=None):
    """Función auxiliar para probar endpoints"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        print(f"✅ {method} {url} - Status: {response.status_code}")
        if response.status_code < 400:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
        return response
    except Exception as e:
        print(f"❌ {method} {url} - Error: {e}")
        return None

def main():
    print("🚀 Probando el módulo de tracking...")
    print("=" * 50)
    
    # 1. Probar endpoint principal
    print("\n1. Probando endpoint principal...")
    test_endpoint(f"{BASE_URL}/")
    
    # 2. Probar health check de tracking
    print("\n2. Probando health check de tracking...")
    test_endpoint(f"{BASE_URL}/tracking/health")
    
    # 3. Probar health check de queries
    print("\n3. Probando health check de queries...")
    test_endpoint(f"{BASE_URL}/tracking/queries/health")
    
    # 4. Probar registro de impresión
    print("\n4. Probando registro de impresión...")
    impresion_data = {
        "id": f"imp-test-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "campaña_id": "cmp-test-123",
        "influencer_id": "inf-test-456",
        "usuario_id": "usr-test-789",
        "tipo_evento": "IMPRESION",
        "user_agent": "Mozilla/5.0 (Test Browser)",
        "ip_address": "192.168.1.100",
        "referrer": "https://test.com",
        "timestamp": datetime.now().isoformat()
    }
    response = test_endpoint(f"{BASE_URL}/tracking/impresiones", "POST", impresion_data)
    
    # 5. Probar registro de conversión
    print("\n5. Probando registro de conversión...")
    conversion_data = {
        "id": f"conv-test-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "campaña_id": "cmp-test-123",
        "influencer_id": "inf-test-456",
        "usuario_id": "usr-test-789",
        "tipo_conversion": "VENTA",
        "valor": 150000.0,
        "moneda": "COP",
        "user_agent": "Mozilla/5.0 (Test Browser)",
        "ip_address": "192.168.1.100",
        "referrer": "https://test.com",
        "timestamp": datetime.now().isoformat()
    }
    response = test_endpoint(f"{BASE_URL}/tracking/conversiones", "POST", conversion_data)
    
    # 6. Probar consultas (si el servidor está funcionando)
    print("\n6. Probando consultas...")
    test_endpoint(f"{BASE_URL}/tracking/queries/campañas/cmp-test-123/estadisticas")
    
    print("\n✅ Pruebas completadas!")

if __name__ == "__main__":
    main()
