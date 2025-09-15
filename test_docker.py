#!/usr/bin/env python3
"""
Script de prueba para el servicio de tracking en Docker
"""
import requests
import json
import time
from datetime import datetime

# URLs de los servicios
API_URL = "http://localhost:8000"
QUERIES_URL = "http://localhost:8001"

def wait_for_service(url, service_name, max_retries=30):
    """Espera a que un servicio esté disponible"""
    print(f"⏳ Esperando que {service_name} esté disponible...")
    
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/", timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} está disponible!")
                return True
        except:
            pass
        
        print(f"   Intento {i+1}/{max_retries}...")
        time.sleep(2)
    
    print(f"❌ {service_name} no está disponible después de {max_retries} intentos")
    return False

def test_endpoint(url, method="GET", data=None, description=""):
    """Función auxiliar para probar endpoints"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        status = "✅" if response.status_code < 400 else "❌"
        print(f"{status} {method} {url}")
        print(f"   {description}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code < 400:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            except:
                print(f"   Response: {response.text}")
        else:
            print(f"   Error: {response.text}")
        
        return response
    except Exception as e:
        print(f"❌ {method} {url} - Error: {e}")
        return None

def main():
    print("🐳 Probando el servicio de tracking en Docker...")
    print("=" * 60)
    
    # 1. Esperar a que los servicios estén disponibles
    if not wait_for_service(API_URL, "API Principal"):
        return
    
    if not wait_for_service(QUERIES_URL, "API de Queries"):
        return
    
    print("\n" + "=" * 60)
    print("🚀 Iniciando pruebas...")
    print("=" * 60)
    
    # 2. Probar endpoints principales
    print("\n📋 1. Probando endpoints principales...")
    test_endpoint(f"{API_URL}/", description="Endpoint raíz")
    test_endpoint(f"{API_URL}/tracking/health", description="Health check de tracking")
    test_endpoint(f"{QUERIES_URL}/tracking/queries/health", description="Health check de queries")
    
    # 3. Probar registro de impresión
    print("\n📊 2. Probando registro de impresión...")
    impresion_data = {
        "id": f"imp-docker-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "campaña_id": "cmp-docker-123",
        "influencer_id": "inf-docker-456",
        "usuario_id": "usr-docker-789",
        "tipo_evento": "IMPRESION",
        "user_agent": "Mozilla/5.0 (Docker Test Browser)",
        "ip_address": "172.17.0.1",
        "referrer": "https://docker-test.com",
        "timestamp": datetime.now().isoformat()
    }
    test_endpoint(f"{API_URL}/tracking/impresiones", "POST", impresion_data, "Registrar impresión")
    
    # 4. Probar registro de conversión
    print("\n💰 3. Probando registro de conversión...")
    conversion_data = {
        "id": f"conv-docker-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "campaña_id": "cmp-docker-123",
        "influencer_id": "inf-docker-456",
        "usuario_id": "usr-docker-789",
        "tipo_conversion": "VENTA",
        "valor": 250000.0,
        "moneda": "COP",
        "user_agent": "Mozilla/5.0 (Docker Test Browser)",
        "ip_address": "172.17.0.1",
        "referrer": "https://docker-test.com",
        "timestamp": datetime.now().isoformat()
    }
    test_endpoint(f"{API_URL}/tracking/conversiones", "POST", conversion_data, "Registrar conversión")
    
    # 5. Esperar un poco para que se procesen los eventos
    print("\n⏳ 4. Esperando procesamiento de eventos...")
    time.sleep(5)
    
    # 6. Probar consultas
    print("\n🔍 5. Probando consultas...")
    test_endpoint(f"{QUERIES_URL}/tracking/queries/campañas/cmp-docker-123/estadisticas", 
                  description="Estadísticas de campaña")
    test_endpoint(f"{QUERIES_URL}/tracking/queries/campañas/cmp-docker-123/impresiones", 
                  description="Impresiones de campaña")
    test_endpoint(f"{QUERIES_URL}/tracking/queries/campañas/cmp-docker-123/conversiones", 
                  description="Conversiones de campaña")
    
    # 7. Probar consultas por influencer
    print("\n👤 6. Probando consultas por influencer...")
    test_endpoint(f"{QUERIES_URL}/tracking/queries/influencers/inf-docker-456/impresiones", 
                  description="Impresiones de influencer")
    test_endpoint(f"{QUERIES_URL}/tracking/queries/influencers/inf-docker-456/conversiones", 
                  description="Conversiones de influencer")
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas!")
    print("=" * 60)
    print("\n📊 Resumen de servicios:")
    print(f"   • API Principal: {API_URL}")
    print(f"   • API de Queries: {QUERIES_URL}")
    print(f"   • Apache Pulsar: http://localhost:8080")
    print(f"   • Datos persistentes: ./data/")

if __name__ == "__main__":
    main()
