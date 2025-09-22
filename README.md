## Alpes Partners – Documentación de Arquitectura

### 1. Propósito del Proyecto
Implementar DDD + CQRS + event-driven con Apache Pulsar

## Servicios y Endpoints (Resumen)

Este repositorio contiene tres capacidades principales:

- Marketing_Influencers: API HTTP para creación y orquestación de campañas, con consumidores para mensajería.
- Tracking: API HTTP para registrar impresiones y conversiones (write) y API de consultas basada en read models (queries).
- Pagos: Consumidores para eventos de pagos y comisiones (no expone API HTTP aún).

Puertos (docker compose):
- `8000` → API FastAPI principal (routers: `marketing-influencers`, `tracking`, `tracking/queries`).
- `8001` → API FastAPI secundaria para consultas (opcional, mismo `app`).
- `6650` → Apache Pulsar broker.

### Marketing_Influencers (API)

Base URL: `http://localhost:8000/marketing-influencers`

- `GET /health` → Health check.
- `POST /campanas` → Crear campaña; encola comando para procesamiento asíncrono.
	Cuerpo ejemplo:
	```json
	{
		"id": "acde070d-8c4c-4f0d-9d8a-162843c10111",
		"nombre": "Lanzamiento X",
		"producto": "Producto X",
		"presupuesto": 1000000,
		"moneda": "COP",
		"marca": "MarcaX",
		"influencers_ids": ["acde070d-8c4c-4f0d-9d8a-162843c10222", "acde070d-8c4c-4f0d-9d8a-162843c10333"],
		"conversiones": []
	}
	```
- `GET /campanas/{campaña_id}` → Obtener campaña por id (placeholder/TODO en código actual).

Implementación clave: `api/marketing_influencers.py`, `modulos/marketing_influencers/aplicacion/mapeadores.py`, `modulos/marketing_influencers/infraestructura/`.

### Tracking – Write API (registro)

Base URL: `http://localhost:8000/tracking`

- `GET /health` → Health check.
- `POST /impresiones` → Publica en `comando-registrar-impresion`.
	Cuerpo ejemplo:
	```json
	{
		"id": "imp-123",
		"campaña_id": "cmp-123",
		"influencer_id": "inf-001",
		"usuario_id": "usr-101",
		"tipo_evento": "IMPRESION",
		"user_agent": "Mozilla/5.0",
		"ip_address": "127.0.0.1",
		"referrer": "https://instagram.com",
		"timestamp": "2025-01-01T12:00:00Z"
	}
	```
- `POST /conversiones` → Publica en `comando-registrar-conversion`.
	Cuerpo ejemplo:
	```json
	{
		"id": "conv-123",
		"campaña_id": "cmp-123",
		"influencer_id": "inf-001",
		"usuario_id": "usr-101",
		"tipo_conversion": "VENTA",
		"valor": 150000.0,
		"moneda": "COP",
		"user_agent": "Mozilla/5.0",
		"ip_address": "127.0.0.1",
		"referrer": "https://instagram.com",
		"timestamp": "2025-01-01T12:05:00Z"
	}
	```

Los consumidores definitivos (`modulos/tracking/infraestructura/consumidores_final.py`) procesan los comandos, persisten (in-memory) y publican eventos:
- `evento-impresion-registrada`
- `evento-conversion-registrada`

### Tracking – Queries API (read models)

Base URL recomendada: `http://localhost:8001/tracking/queries` (también disponible bajo `8000`).

- `GET /health`
- `GET /impresiones/{impresion_id}`
- `GET /conversiones/{conversion_id}`
- `GET /campañas/{campaña_id}/impresiones`
- `GET /campañas/{campaña_id}/conversiones`
- `GET /campañas/{campaña_id}/estadisticas`
- `GET /influencers/{influencer_id}/impresiones`
- `GET /influencers/{influencer_id}/conversiones`

Implementación: `api/tracking_queries.py` y `modulos/tracking/infraestructura/read_models.py`.

### Pagos (consumidores)

No expone API HTTP. Incluye consumidores de ejemplo/simulación:
- `infraestructura/consumidor_pagos.py`
- `infraestructura/consumidor_comisiones.py`
- `infraestructura/consumidores.py` (orquestador)

Estado: imprime eventos simulados; pendiente integrar con eventos del dominio.

### 2. Estilo Arquitectónico
- Domain Driven Design (DDD) con módulos de dominio bajo `modulos/`.
- CQRS: existen comandos (`seedwork.aplicacion.comandos` + comandos específicos de marketing_influencers). Queries futuras.
- Event / Message Driven: uso de Apache Pulsar + Avro (esquemas en `infraestructura/schema/v1`).
- Arquitectura Hexagonal(en construcción): capas dominio – aplicación – infraestructura – interfaces (API FastAPI).
- Persistencia prevista con PostgreSQL

### 3. Estructura de Carpetas (Resumen)
```
alpespartners.DockerFile          # Imagen base del servicio FastAPI
docker-compose.yml                # Servicio Pulsar standalone
requirements.txt                  # Dependencias Python
src/alpespartners/
	main.py                         # Creación de FastAPI y montaje de routers
	api/                            # Capa de entrega (endpoints REST)
		marketing_influencers.py
	config/db.py                    # Configuración DB (PostgreSQL)
	modulos/
		marketing_influencers/
			dominio/                    # Entidades, objetos de valor (de este módulo)
			aplicacion/                 # DTOs, comandos, mapeadores, handlers
			infraestructura/            # Repositorios, despachadores Pulsar, esquemas Avro
		pagos/
			dominio/
			aplicacion/
			infraestructura/
		tracking/
			dominio/
			aplicacion/
			infraestructura/
	seedwork/                       # Elementos reutilizables transversales (DDD base)
```

### Flujo
![Transacción](transaccion.png)

1. Marketing de Influencers

	Aquí se configura la campaña inicial:
	- Crear Campaña: Se genera la campaña de marketing.
	- Asignar comisiones: Se definen las condiciones de pago (ejemplo: por impresión, clic o venta).
	- Agrega los influencers: Se suman los influencers que participarán en la campaña.
	- Resultado: Campaña Creada (listo para ejecutarse).

2. Tracking (Seguimiento)

	Se registra la interacción de los usuarios con la campaña:
	- Registrar impresión: Cuando un usuario ve el contenido del influencer.
	- Impresión registrada: Confirmación de que el sistema contabilizó esa visualización.
	- Registrar conversión: Cuando un usuario realiza la acción deseada (ejemplo: compra, registro).
	- Conversión registrada: Confirmación de que esa acción se registró exitosamente.

3. Pagos

	Una vez registradas las conversiones, se gestiona la parte financiera:
	- Calcular comisión: Se determina cuánto gana el influencer por las conversiones.
	- Comisión calculada: El monto queda definido.
	- Programar pago: Se agenda el pago correspondiente.
	- Pago realizado: El influencer recibe su dinero.

### Prubas iniciales
![tracking](tracking1.png)
![tracking](tracking2.png)
![tracking](tracking3.png)

### 4. Capas y Seedwork
| Capa | Rol | Ejemplos |
|------|-----|----------|
| Dominio | Modelo rico: entidades, objetos valor, invariantes | `Entidad`, `Campaña`, `Monto`, `EstadoPago` |
| Aplicación | Orquestación de casos de uso (Handlers de comandos), DTOs, Mapeadores | `CrearCampaña`, `MapeadorCampañaDTOJson` |
| Infraestructura | Adaptadores externos: repositorios persistencia, mensajería, esquemas | `RepositorioCampañasDB`, `Despachador`, Avro schemas |
| Interfaz / API | Transporte HTTP (FastAPI) | `marketing_influencers.py` |
| Seedwork | Abstracciones y patrones genéricos | `Comando`, `ComandoHandler`, `Fabrica`, `Mapeadores`, `Entidad` |

### 5. Dominio Principal (Marketing Influencers)
Entidades clave:
- Campaña: agrupa datos de la campaña (nombre, producto, presupuesto (Objeto Valor `Monto`), marca, influencers, conversiones).
- Influencer: datos del creador (nombre, email, cédula – definidos como objetos de valor en archivos aún no revisados aquí – y métricas base).
- Conversion: monto asociado a una interacción / venta atribuida.
- Pago: estado de liquidación para un influencer (`EstadoPago`).

Objetos de Valor seedwork relevantes:
- `Monto(valor: Decimal, moneda: Moneda)` garantiza tipado y semántica de monto monetario.
- `Moneda` y `EstadoPago` (Enums) encapsulan estados permitidos.

### 6. Flujo de Caso de Uso: Crear Campaña
1. Cliente invoca POST `/marketing-influencers/campanas` con JSON de la campaña.
2. Endpoint usa `MapeadorCampañaDTOJson` para pasar de dict externo a `CampañaDTO` (DTO de aplicación).
3. Se construye comando `CrearCampaña` y se usa `Despachador.publicar_comando` para publicar un mensaje Avro en Pulsar (tópico `crear-campaña`).
4. (Pendiente) Un consumidor debería recibir el comando, construir la entidad `Campaña` mediante fábricas y persistirla vía repositorio.
5. (Pendiente) Emisión de evento de dominio / integración `EventoCampañaCreada` tras persistencia.

Observaciones:
- El handler `CrearCampañaHandler` invoca `fabrica_campañas` pero la base `CrearReservaBaseHandler` solo inicializa `fabrica_repositorio`; falta cohesión y definiciones (posible código heredado o refactor incompleto).
- El método registrado con `@comando.register(CrearCampaña)` crea un handler sin parámetros (`__init__` exige `event_bus` en algunos casos) y llama `handler.handle(comando)` pero `handle` es `async` y no se espera (no await). Debe corregirse.

### 7. Mensajería (Apache Pulsar + Avro)
- `infraestructura/despachadores.py` crea un cliente Pulsar apuntando a `pulsar://<BROKER_HOST>:6650` (variable de entorno `BROKER_HOST`, default `localhost`).
- Publica comandos y eventos usando Avro schemas:
	- Comando: `ComandoCrearCampaña` (payload con atributos de la campaña + `fecha_creacion`).
	- Evento: `EventoCampañaCreada` (payload con `id`).
- Serialización: `pulsar.schema.AvroSchema` a partir de clases con campos declarativos.

### 8. Persistencia (Estado Actual)
- Configuración: `config/db.py`

### 9. Patrones Implementados / Intención
- Comando Handler con `functools.singledispatch` para registrar ejecuciones específicas por tipo de comando.
- Mapeadores duales (externo ↔ DTO ↔ Entidad) para aislar formato de transporte.
- Fábricas: resuelven construcción de repositorios y entidades (aunque hay inconsistencias).
- Repositorio: interfaz para acceso a agregados (implementación incompleta).
- Value Objects: inmutabilidad para expresividad y evitar primitivo-anemia.

### 10. Ejecución Local
Requisitos: Python 3.11.

Instalación dependencias:
```
pip install -r requirements.txt
```

Iniciar Pulsar (contenedor standalone):
```
docker compose up -d pulsar
```

Inicializar DB (opcional si se agregan modelos): abra un shell Python y ejecute:
```python
from alpespartners.config.db import init_db
init_db()
```

Levantar API:
```
uvicorn alpespartners.main:app --reload
```

Probar health:
```
GET http://localhost:8000/
GET http://localhost:8000/marketing-influencers/health
```

Crear campaña (ejemplo):
```json
POST http://127.0.0.1:8000/marketing-influencers/campañas
{
	"id": "cmp-123",
	"nombre": "Lanzamiento X",
	"producto": "Producto X",
	"presupuesto": 1000000,
	"moneda": "COP",
	"marca": "MarcaX"
}
```
Respuesta esperada (actual): `202 { "status": "EN_QUEUED" }`

### 11. Ejecución con Docker Compose

Servicios definidos en `docker-compose.yml`:
- `bff` (FastAPI, puerto `8000`)
- `tracking-queries` (FastAPI, puerto `8001`)
- `marketing-influencers` (consumidores del módulo Marketing)
- `tracking-consumer` (consumidores Tracking)
- `pulsar` y `postgres`

Comando:
```
docker compose up --build
```
Una vez arriba:
- `http://localhost:8000` → API principal (write + queries)
- `http://localhost:8001` → API consultas (queries)

### 12. Variables de Entorno Clave
| Variable | Descripción | Default |
|----------|-------------|---------|
| `BROKER_HOST` | Hostname/IP broker Pulsar | `localhost` |
| `DATABASE_URL` | (Si se externaliza) cadena conexión PostgreSQL | `postgresql+psycopg2://postgres:postgres@postgres:5432/postgres` |

