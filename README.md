## Alpes Partners – Documentación de Arquitectura

### 1. Propósito del Proyecto
Implementar DDD + CQRS + event-driven con Apache Pulsar

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
	seedwork/                       # Elementos reutilizables transversales (DDD base)
```

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
1. Cliente invoca POST `/marketing-influencers/campañas` con JSON de la campaña.
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

### 11. Levantar servicio
```
docker compose -f 'docker-compose.yml' up -d --build
```

### 12. Variables de Entorno Clave
| Variable | Descripción | Default |
|----------|-------------|---------|
| `BROKER_HOST` | Hostname/IP broker Pulsar | `localhost` |
| `DATABASE_URL` | (Si se externaliza) cadena conexión PostgreSQL | `postgresql+psycopg2://postgres:postgres@postgres:5432/postgres` |

