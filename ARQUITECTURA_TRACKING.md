# Arquitectura del Módulo Tracking

## Diagrama de Flujo

```
Cliente HTTP
    ↓
API REST (FastAPI)
    ↓
Mapeadores (DTO ↔ Entidad)
    ↓
Comandos de Aplicación
    ↓
Despachador Pulsar
    ↓
Apache Pulsar (Tópicos)
    ↓
Consumidores
    ↓
Handlers de Comandos
    ↓
Entidades de Dominio
    ↓
Repositorios (Persistencia)
    ↓
Eventos de Dominio
    ↓
Despachador Pulsar
    ↓
Otros Módulos (Suscripciones)
```

## Estructura de Capas

### 1. Capa de Presentación (API)
- **tracking.py**: Endpoints REST
- Maneja requests HTTP
- Valida datos de entrada
- Mapea JSON a DTOs

### 2. Capa de Aplicación
- **Comandos**: RegistrarImpresion, RegistrarConversion
- **DTOs**: ImpresionDTO, ConversionDTO
- **Mapeadores**: Conversión entre capas
- **Handlers**: Lógica de procesamiento

### 3. Capa de Dominio
- **Entidades**: Impresion, Conversion
- **Objetos Valor**: Metadatos, ValorConversion
- **Eventos**: ImpresionRegistrada, ConversionRegistrada
- **Repositorios**: Interfaces de persistencia

### 4. Capa de Infraestructura
- **Repositorios**: Implementaciones concretas
- **Despachadores**: Comunicación con Pulsar
- **Consumidores**: Procesamiento de eventos
- **Esquemas Avro**: Serialización de mensajes

## Tópicos de Pulsar

### Comandos (Entrada)
- `comando-registrar-impresion`
- `comando-registrar-conversion`

### Eventos (Salida)
- `evento-impresion-registrada`
- `evento-conversion-registrada`

## Patrones Implementados

1. **CQRS**: Separación de comandos y queries
2. **Event Sourcing**: Eventos como fuente de verdad
3. **Domain Events**: Comunicación entre módulos
4. **Repository Pattern**: Abstracción de persistencia
5. **Command Pattern**: Encapsulación de operaciones
6. **DTO Pattern**: Transferencia de datos
