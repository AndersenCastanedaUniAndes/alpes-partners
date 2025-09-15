# Topología Híbrida Mejorada - Módulo Tracking

## 🎯 **Resumen de la Topología Recomendada**

La nueva topología implementa una **arquitectura híbrida mejorada** que combina:

- **Event Sourcing** para persistencia de eventos
- **CQRS** para separación de comandos y consultas
- **Read Models** optimizados para consultas
- **Proyecciones** para mantener consistencia eventual
- **Event Store** centralizado para auditoría y reconstrucción

## 🏗️ **Arquitectura de la Topología**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Commands  │    │   Event Store    │    │   Read Models   │
│   (Centralizada)│───▶│   (Centralizado) │───▶│ (Descentralizados)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Command       │    │   Projections    │    │   API Queries   │
│   Handlers      │    │   (Descentralizadas)│    │ (Descentralizada)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Apache Pulsar │    │   Event Bus      │    │   SQLite DBs    │
│   (Centralizado)│    │   (Centralizado) │    │ (Descentralizadas)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 **Componentes Implementados**

### **1. Event Store Centralizado**
- **Archivo**: `infraestructura/event_store.py`
- **Función**: Almacena todos los eventos de dominio
- **Ventajas**: Auditoría completa, reconstrucción de estado, trazabilidad

### **2. Read Models Descentralizados**
- **Archivo**: `infraestructura/read_models.py`
- **Función**: Modelos optimizados para consultas específicas
- **Ventajas**: Performance mejorada, consultas especializadas

### **3. Proyecciones (Projections)**
- **Archivo**: `infraestructura/projections.py`
- **Función**: Mantiene read models actualizados desde eventos
- **Ventajas**: Consistencia eventual, escalabilidad

### **4. API de Consultas Separada**
- **Archivo**: `api/tracking_queries.py`
- **Función**: Endpoints optimizados para consultas
- **Ventajas**: Separación clara de responsabilidades

## 📊 **Flujo de Datos**

### **Comandos (Write Side)**
1. Cliente envía comando → API REST
2. API mapea a DTO → Comando de aplicación
3. Comando se publica → Apache Pulsar
4. Consumidor procesa → Handler de comando
5. Se crea entidad → Evento de dominio
6. Evento se guarda → Event Store
7. Proyección actualiza → Read Models
8. Evento se publica → Apache Pulsar

### **Consultas (Read Side)**
1. Cliente consulta → API de Queries
2. API consulta → Read Models
3. Read Models retorna → Datos optimizados
4. API responde → Cliente

## 🚀 **Ventajas de la Nueva Topología**

### **Escalabilidad**
- **Comandos**: Pueden escalarse independientemente
- **Consultas**: Read models optimizados para cada caso de uso
- **Proyecciones**: Pueden ejecutarse en paralelo

### **Resiliencia**
- **Event Store**: Fuente única de verdad
- **Read Models**: Pueden reconstruirse desde eventos
- **Fallos aislados**: Un componente falla sin afectar otros

### **Performance**
- **Consultas rápidas**: Read models pre-calculados
- **Escrituras asíncronas**: No bloquean consultas
- **Caché natural**: Read models actúan como caché

### **Observabilidad**
- **Auditoría completa**: Todos los eventos se almacenan
- **Trazabilidad**: Cada operación es rastreable
- **Métricas**: Estadísticas en tiempo real

## 🔍 **Endpoints Disponibles**

### **Comandos (Write)**
- `POST /tracking/impresiones` - Registrar impresión
- `POST /tracking/conversiones` - Registrar conversión

### **Consultas (Read)**
- `GET /tracking/queries/impresiones/{id}` - Obtener impresión
- `GET /tracking/queries/conversiones/{id}` - Obtener conversión
- `GET /tracking/queries/campañas/{id}/impresiones` - Impresiones por campaña
- `GET /tracking/queries/campañas/{id}/conversiones` - Conversiones por campaña
- `GET /tracking/queries/campañas/{id}/estadisticas` - Estadísticas de campaña
- `GET /tracking/queries/influencers/{id}/impresiones` - Impresiones por influencer
- `GET /tracking/queries/influencers/{id}/conversiones` - Conversiones por influencer

## 🛠️ **Cómo Ejecutar**

### **1. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **2. Levantar Apache Pulsar**
```bash
docker run -it -p 6650:6650 -p 8080:8080 apachepulsar/pulsar:latest bin/pulsar standalone
```

### **3. Ejecutar API**
```bash
cd src
uvicorn alpespartners.main:app --reload --host 127.0.0.1 --port 8000
```

### **4. Ejecutar Consumidores**
```bash
cd src
python -m alpespartners.modulos.tracking.infraestructura
```

## 📈 **Métricas y Monitoreo**

### **Event Store**
- Total de eventos almacenados
- Tasa de eventos por segundo
- Tamaño de la base de datos

### **Read Models**
- Tiempo de respuesta de consultas
- Tamaño de cada read model
- Frecuencia de actualizaciones

### **Proyecciones**
- Latencia de procesamiento
- Eventos procesados por segundo
- Errores de procesamiento

## 🔮 **Próximas Mejoras**

1. **Base de datos distribuida** (PostgreSQL/MySQL)
2. **Caché Redis** para read models
3. **Métricas Prometheus** para monitoreo
4. **Circuit breakers** para resiliencia
5. **Dead letter queues** para mensajes fallidos
6. **Compresión de eventos** para optimizar almacenamiento

## 🎯 **Conclusión**

Esta topología híbrida mejorada proporciona:

- ✅ **Escalabilidad** horizontal y vertical
- ✅ **Resiliencia** ante fallos
- ✅ **Performance** optimizada para consultas
- ✅ **Observabilidad** completa del sistema
- ✅ **Flexibilidad** para futuras mejoras

Es la arquitectura recomendada para sistemas de tracking de alto volumen y alta disponibilidad.
