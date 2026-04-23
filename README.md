# Evidence Storage Service

Microservicio de Almacenamiento de Evidencias con integración a Azure Storage (Azurite).

## Descripcion

API REST para almacenar y consultar evidencias (texto o JSON) en un almacenamiento Blob compatible con Azure Storage.

## Arquitectura

```
┌─────────────┐         ┌─────────────┐
│   Client    │────────▶│  Evidence   │
│  (curl/     │         │    API      │
│  Postman)   │         │  (FastAPI) │
└─────────────┘         └──────┬──────┘
                                │
                                ▼
                        ┌─────────────┐
                        │   Azurite   │
                        │  (Blob     │
                        │  Storage)  │
                        └─────────────┘
```

## Requisitos Previos

- Docker 20.10+
- Docker Compose 2.0+
- Puertos disponibles: 8080, 10000

## Inicio Rapido

### 1. Construir y levantar servicios

```bash
docker-compose up --build
```

### 2. Verificar que los servicios estan activos

```bash
# Health check de la API
curl http://localhost:8080/health
```

### 3. Usar la API

**Crear una evidencia:**
```bash
curl -X POST http://localhost:8080/api/evidence \
  -H "Content-Type: application/json" \
  -d '{"contenido": "Primera evidencia de prueba"}'
```

**Recuperar una evidencia:**
```bash
curl http://localhost:8080/api/evidence/{EVIDENCE_ID}
```

## Endpoints

| Metodo | Path | Descripcion |
|-------|------|------------|
| POST | /api/evidence | Almacenar una evidencia |
| GET | /api/evidence/{id} | Recuperar una evidencia |
| GET | /health | Health check |

## Parametros de Configuracion

Copiar `.env.example` a `.env` y ajustar segun necesidad:

| Variable | Descripcion | Default |
|----------|------------|---------|
| AZURITE_ACCOUNT_NAME | Nombre de cuenta Azurite | devstoreaccount |
| AZURITE_ACCOUNT_KEY | Clave Azurite | (default key) |
| AZURITE_BLOB_ENDPOINT | Endpoint Blob | http://azurite:10000/... |
| AZURITE_CONTAINER_NAME | Nombre del contenedor | evidences |
| LOG_LEVEL | Nivel de logs | INFO |

## Comandos Utiles

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo API
docker-compose logs -f app

# Solo Azurite
docker-compose logs -f azurite
```

### Detener servicios
```bash
docker-compose down
```

### Detener incluyendo volúmenes
```bash
docker-compose down -v
```

### Reconstruir desde cero
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Migracion a Azure Cloud

Para migrar a Azure Storage real en cloud:

1. **Cambiar credentials**: Actualizar `AZURITE_ACCOUNT_NAME` y `AZURITE_ACCOUNT_KEY` con las credenciales de Azure Storage
2. **Cambiar endpoint**: Cambiar `AZURITE_BLOB_ENDPOINT` al endpoint de Azure Blob Storage
3. **Sin cambios en codigo**: El SDK de Azure es compatible con ambos (Azurite local y Azure cloud)

### Ejemplo de configuracion Azure Cloud
```
AZURITE_ACCOUNT_NAME=mystorageaccount
AZURITE_ACCOUNT_KEY=<azure_storage_account_key>
AZURITE_BLOB_ENDPOINT=https://mystorageaccount.blob.core.windows.net
```

## Desarrollo Local (sin Docker)

### Requisitos
- Python 3.11+

### Instalacion
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Ejecucion
```bash
# Iniciar Azurite standalone (requerido)
docker run -d -p 10000:10000 mcr.microsoft.com/azure-storage/azurite:latest azurite-blob --blobHost 0.0.0.0 --blobPort 10000

# Iniciar API
python -m app.main
```

## Estructura del Proyecto

```
.
├── app/
│   ├── main.py              # Entry point FastAPI
│   ├── config.py            # Configuracion
│   ├── models.py           # Modelos Pydantic
│   ├── routes/
│   │   └── evidence.py     # Endpoints
│   └── services/
│       └── storage.py       # Servicio Azurite
├── tests/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── requirements.txt
└── README.md
```

## Licencia

MIT