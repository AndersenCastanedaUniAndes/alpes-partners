# Módulo Tracking - Alpes Partners

## Descripción
Módulo de tracking para registrar impresiones y conversiones de campañas de marketing digital.

## Funcionalidades

### Comandos
- **RegistrarImpresion**: Registra una impresión de campaña
- **RegistrarConversion**: Registra una conversión (venta, registro, etc.)

### Eventos de Dominio
- **ImpresionRegistrada**: Se emite cuando se registra una impresión
- **ConversionRegistrada**: Se emite cuando se registra una conversión

### API REST Endpoints

#### Impresiones
- `POST /tracking/impresiones` - Registrar nueva impresión
- `GET /tracking/impresiones/{id}` - Obtener impresión por ID
- `GET /tracking/campañas/{campaña_id}/impresiones` - Obtener impresiones por campaña

#### Conversiones
- `POST /tracking/conversiones` - Registrar nueva conversión
- `GET /tracking/conversiones/{id}` - Obtener conversión por ID
- `GET /tracking/campañas/{campaña_id}/conversiones` - Obtener conversiones por campaña

## Ejemplos de Uso

### Registrar Impresión
```bash
curl -X POST "http://localhost:8000/tracking/impresiones" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "imp-123",
    "campaña_id": "cmp-456",
    "influencer_id": "inf-789",
    "usuario_id": "usr-101",
    "tipo_evento": "IMPRESION",
    "user_agent": "Mozilla/5.0...",
    "ip_address": "192.168.1.1",
    "referrer": "https://instagram.com",
    "timestamp": "2024-01-15T10:30:00Z"
  }'
```

### Registrar Conversión
```bash
curl -X POST "http://localhost:8000/tracking/conversiones" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "conv-123",
    "campaña_id": "cmp-456",
    "influencer_id": "inf-789",
    "usuario_id": "usr-101",
    "tipo_conversion": "VENTA",
    "valor": 150000.0,
    "moneda": "COP",
    "user_agent": "Mozilla/5.0...",
    "ip_address": "192.168.1.1",
    "referrer": "https://instagram.com",
    "timestamp": "2024-01-15T10:35:00Z"
  }'
```

## Arquitectura

### Flujo de Datos
1. Cliente envía request a API REST
2. API mapea JSON a DTO
3. Se crea comando de aplicación
4. Comando se publica en Apache Pulsar
5. Consumidor procesa comando
6. Se crea entidad de dominio
7. Se persiste en repositorio
8. Se emite evento de dominio
9. Evento se publica en Pulsar

### Tópicos de Pulsar
- `comando-registrar-impresion`
- `comando-registrar-conversion`
- `evento-impresion-registrada`
- `evento-conversion-registrada`

## Ejecución

### Con Docker
```bash
docker compose up -d
```

### Local
```bash
# Terminal 1: API
uvicorn alpespartners.main:app --reload

# Terminal 2: Consumidores
python -m alpespartners.modulos.tracking.infraestructura
```

## Estructura de Archivos
```
tracking/
├── dominio/
│   ├── entidades.py          # Impresion, Conversion
│   ├── objetos_valor.py      # Metadatos, ValorConversion, etc.
│   ├── eventos.py            # ImpresionRegistrada, ConversionRegistrada
│   └── repositorios.py       # Interfaces de repositorios
├── aplicacion/
│   ├── comandos/             # RegistrarImpresion, RegistrarConversion
│   ├── dto.py               # DTOs de aplicación
│   ├── mapeadores.py        # Mapeadores entre capas
│   └── handlers.py          # Handlers de comandos
└── infraestructura/
    ├── repositorios.py       # Implementaciones de repositorios
    ├── despachadores.py      # Despachador de Pulsar
    ├── consumidores.py       # Consumidores de eventos
    └── schema/v1/           # Esquemas Avro para Pulsar
```
