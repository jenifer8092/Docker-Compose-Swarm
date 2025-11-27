# Traductor Gen-AI con Docker Compose y Swarm

Aplicación de traducción de texto usando modelos generativos, con interfaz Gradio y tracking de experimentos con MLflow. Soporta despliegue local con Docker Compose y producción escalable con Docker Swarm.

## 📋 Descripción

Sistema de traducción automática que:
- Traduce texto entre múltiples idiomas usando IA generativa
- Registra cada interacción en MLflow para análisis
- Se despliega con Docker Compose para desarrollo
- Escala en producción con Docker Swarm

## 🏗️ Arquitectura

### Desarrollo Local (Docker Compose)
```
┌─────────────────────────────────────────┐
│         Docker Compose Network          │
│                                         │
│  ┌────────────────┐  ┌───────────────┐ │
│  │ app-traductor  │  │ mlflow-server │ │
│  │   (Gradio)     │  │  (Tracking)   │ │
│  │  Puerto: 8080  │  │ Puerto: 5000  │ │
│  └────────────────┘  └───────────────┘ │
│         │                    │          │
│         └────────HTTP────────┘          │
└─────────────────────────────────────────┘
```

### Producción (Docker Swarm)
```
┌──────────────────────────────────────────────┐
│            Docker Swarm Cluster              │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │   Overlay Network (traductor-net)      │ │
│  │                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌─────┐ │ │
│  │  │   App    │  │   App    │  │ ... │ │ │
│  │  │ Replica1 │  │ Replica2 │  │     │ │ │
│  │  └──────────┘  └──────────┘  └─────┘ │ │
│  │                                        │ │
│  │  ┌───────────────────┐                │ │
│  │  │  MLflow Server    │                │ │
│  │  │  (Manager node)   │                │ │
│  │  └───────────────────┘                │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  Load Balancer (Routing Mesh)               │
└──────────────────────────────────────────────┘
```

## 🚀 Imagen Docker Hub

```
jeni001/traductor-genai:1.0.1
```

**Link:** https://hub.docker.com/r/jeni001/traductor-genai

## 📦 Requisitos

- Docker Desktop 20.10+ instalado
- Docker Compose 1.29+ (incluido en Docker Desktop)
- API Key de un proveedor:
  - OpenAI: https://platform.openai.com/api-keys
  - Groq (Gratis): https://console.groq.com/keys ⭐ Recomendado
  - Google AI: https://aistudio.google.com/app/apikey

## 🛠️ Desarrollo Local con Docker Compose

### Paso 1: Clonar el repositorio

```bash
git clone <tu-repo-url>
cd Project-Docker
```

### Paso 2: Configurar variables de entorno

```bash
# Para OpenAI
export API_KEY="sk-..."

# O para Groq (gratis)
export API_KEY="gsk-..."
export OPENAI_BASE_URL="https://api.groq.com/openai/v1"
export MODEL="llama-3.1-8b-instant"
```

### Paso 3: Levantar el stack

```bash
docker-compose up --build
```

### Paso 4: Acceder a las interfaces

- **Gradio (Traductor):** http://localhost:8080
- **MLflow (Tracking):** http://localhost:5000

### Comandos útiles

```bash
# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Detener y limpiar volúmenes
docker-compose down -v
```

## 🐝 Despliegue en Producción con Docker Swarm

### Paso 1: Inicializar Swarm

```bash
docker swarm init
```

### Paso 2: Configurar variables de entorno

```bash
export API_KEY="tu-api-key"
# Agregar otras variables si es necesario
```

### Paso 3: Desplegar el stack

```bash
docker stack deploy -c docker-stack.yml traductor_stack
```

### Paso 4: Verificar despliegue

```bash
# Ver servicios
docker stack services traductor_stack

# Ver réplicas
docker service ls
```

### Paso 5: Escalar la aplicación

```bash
# Escalar a 3 réplicas
docker service scale traductor_stack_app-traductor=3

# Escalar a 5 réplicas
docker service scale traductor_stack_app-traductor=5
```

### Comandos útiles

```bash
# Ver logs
docker service logs traductor_stack_app-traductor

# Actualizar stack
docker stack deploy -c docker-stack.yml traductor_stack

# Eliminar stack
docker stack rm traductor_stack
```

## 📊 Diferencias: Compose vs Swarm

| Aspecto | Docker Compose | Docker Swarm |
|---------|----------------|--------------|
| **Uso** | Desarrollo local | Producción |
| **Escalabilidad** | Manual, limitada | Automática, ilimitada |
| **Red** | Bridge | Overlay |
| **Build** | `build: .` | `image: usuario/imagen:tag` |
| **Réplicas** | 1 por defecto | Configurable con `deploy.replicas` |
| **Load Balancing** | No nativo | Routing Mesh automático |
| **Orquestación** | No | Sí (health checks, rollback) |
| **Comando** | `docker-compose up` | `docker stack deploy` |

## 🔧 Estructura del Proyecto

```
Project-Docker/
├── docker-compose.yml      # Desarrollo local
├── docker-stack.yml        # Producción (Swarm)
├── Dockerfile              # Build de la app
├── requirements.txt        # Dependencias Python
├── app.py                 # Punto de entrada
├── config/
│   └── providers.py       # Proveedores de IA
├── prompts/
│   └── tasks.py          # Prompts de traducción
├── services/
│   └── ai_service.py     # Servicio IA + MLflow
└── ui/
    └── interface.py      # Interfaz Gradio
```

## 📸 Capturas de Pantalla

### Gradio (Interfaz de Traducción)
![Gradio UI](screenshots/gradio.png)

### MLflow (Tracking de Experimentos)
![MLflow UI](screenshots/mlflow.png)

### Docker Swarm (Servicios Escalados)
![Swarm Services](screenshots/swarm.png)

## 🌐 Variables de Entorno

| Variable | Descripción | Requerido | Default |
|----------|-------------|-----------|---------|
| `API_KEY` | API key del proveedor | Sí | - |
| `OPENAI_BASE_URL` | URL base del API | No | OpenAI oficial |
| `MODEL` | Modelo a utilizar | No | gpt-4o-mini |
| `MLFLOW_TRACKING_URI` | URL del servidor MLflow | Auto | http://mlflow-server:5000 |
| `ENABLE_MLFLOW` | Activar tracking (1/0) | No | 1 |

## 🔒 Seguridad y Buenas Prácticas

### Para Desarrollo (Compose)
```bash
# Usar variables de entorno del host
export API_KEY="tu-key"
docker-compose up
```

### Para Producción (Swarm)
```bash
# Método básico (este taller)
export API_KEY="tu-key"
docker stack deploy -c docker-stack.yml traductor_stack

# Método avanzado (recomendado en producción real)
echo "tu-key" | docker secret create api_key -
# Luego modificar docker-stack.yml para usar secrets
```

## 📈 Monitoreo y Logs

### Docker Compose
```bash
# Logs en tiempo real
docker-compose logs -f app-traductor

# Ver últimas 100 líneas
docker-compose logs --tail=100
```

### Docker Swarm
```bash
# Logs del servicio
docker service logs -f traductor_stack_app-traductor

# Ver todas las tareas
docker service ps traductor_stack_app-traductor

# Monitoreo de recursos
docker stats
```

## 🐛 Troubleshooting

### Problema: Puerto 8080 no responde
**Solución:** Verifica que el servicio esté corriendo
```bash
# Compose
docker-compose ps

# Swarm
docker service ls
```

### Problema: MLflow no registra runs
**Solución:** Verifica la conectividad
```bash
# Compose
docker-compose logs mlflow-server

# Swarm
docker service logs traductor_stack_mlflow-server
```

### Problema: Error de API key
**Solución:** Verifica que la variable esté exportada
```bash
echo $API_KEY
```

## 🚀 Comandos Rápidos

### Desarrollo completo
```bash
export API_KEY="tu-key"
docker-compose up --build
# Abrir http://localhost:8080
docker-compose down
```

### Despliegue en Swarm
```bash
docker swarm init
export API_KEY="tu-key"
docker stack deploy -c docker-stack.yml traductor_stack
docker service scale traductor_stack_app-traductor=3
docker stack rm traductor_stack
```

## 📚 Recursos Adicionales

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Gradio Documentation](https://gradio.app/docs/)

## 📝 Licencia

Este proyecto fue desarrollado como parte de un taller académico sobre Docker, Compose y Swarm.

- Docker Hub: https://hub.docker.com/r/jeni001/traductor-genai
