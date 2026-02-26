# Ada Back

Backend del proyecto Ada, un agente personal que prepara un resumen técnico
diario para programadores y lo envía por correo en formato HTML.

## ¿Qué hace Ada?

Dos veces al día (mañana y noche):

1. Consulta novedades de IA aplicada al desarrollo.
2. Recolecta noticias de programación en general.
3. Busca datos curiosos y educativos sobre algoritmos.
4. Genera un digest estructurado y legible.
5. Renderiza HTML con template Jinja2.
6. Envía un correo al Gmail personal configurado.

## Tecnologías

- Python 3.11+
- LangChain + LangGraph
- Groq API (modelos open-source vía Groq)
- simplegmail (Gmail API via OAuth2)
- Jinja2 para templates HTML
- schedule + pytz para jobs diarios
- Arquitectura hexagonal + clean architecture
- Poetry para gestión de dependencias y entorno

## Estructura del proyecto

La estructura está separada por contexto y por capas:

- `src/app/agent`: curación y generación de contenido
- `src/app/notifications`: composición y envío de correo

Capas por contexto:

- `domain`: entidades, value objects, eventos de dominio
- `application`: casos de uso y puertos
- `infrastructure`: adaptadores de entrada/salida

## Requisitos previos

- Python 3.11+ recomendado
- Poetry instalado

Instalar Poetry (si no lo tienes):

```bash
pip install poetry
```

## Instalación con Poetry

1. Clonar el repositorio.
2. Instalar dependencias:

```bash
poetry install
```

3. Activar entorno virtual:

```bash
poetry shell
```

## Ejecución

### Scheduler (modo producción)

Desde la raíz del proyecto:

```bash
poetry run python main.py
```

Inicia el scheduler que ejecuta automáticamente:
- **08:00** (hora Colombia): digest de mañana
- **20:00** (hora Colombia): digest de noche

Los horarios y timezone son configurables en `.env`:

```dotenv
MORNING_DIGEST_TIME=08:00
EVENING_DIGEST_TIME=20:00
DIGEST_TIMEZONE=America/Bogota
```

### Ejecución única (desarrollo/testing)

Para ejecutar una sola vez sin scheduler:

```bash
poetry run python main.py --once
```

Útil para debugging o pruebas puntuales.

## Configuración requerida

Crear o completar `.env` en la raíz con:

```dotenv
# LLM API
GROQ_API_KEY=your_groq_api_key_here

# Gmail (simplegmail via OAuth2)
GMAIL_SENDER=your_gmail@gmail.com
GMAIL_RECIPIENT=your_gmail@gmail.com
GMAIL_CLIENT_SECRET_PATH=.secrets/client_secret.json
GMAIL_TOKEN_PATH=.secrets/gmail-token.json

# Scheduler (opcional, si no se define usa defaults)
MORNING_DIGEST_TIME=08:00
EVENING_DIGEST_TIME=20:00
DIGEST_TIMEZONE=America/Bogota
```

**Nota sobre Gmail:**
Requiere `client_secret.json` descargado desde la
[Google Cloud Console](https://console.cloud.google.com/apis/credentials).
En la primera ejecución se abrirá el navegador para autenticación OAuth2.

- Formato con Black al guardar.
- Longitud máxima de línea: 79.
- Reglas de diseño: SOLID, DRY, KISS y Observer.

## Deployment en Render (Free Tier)

Ada incluye configuración para deployment gratuito en [Render](https://render.com) como web service con scheduler en background.

### ¿Por qué Render?

- **Free tier permanente** con 750 horas/mes (suficiente para un servicio 24/7)
- Soporta **procesos de larga duración** (a diferencia de serverless como Vercel)
- Deploy automático desde GitHub
- Variables de entorno y secretos gestionados en dashboard

### Arquitectura del deployment

El deployment combina dos componentes:

1. **FastAPI server** (`server.py`): Expone endpoint `/health` para health checks
2. **Scheduler background**: Thread daemon que ejecuta `DigestScheduler` continuamente

Esto evita que Render "duerma" el servicio por inactividad (free tier duerme instancias sin tráfico HTTP).

### Pasos para deployar

#### 1. Preparar repositorio

Asegúrate de que los siguientes archivos están en el repo:
- `render.yaml` ✅ (configuración IaC)
- `server.py` ✅ (FastAPI con scheduler en background)
- `pyproject.toml` y `poetry.lock` ✅

#### 2. Crear servicio en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New +"** → **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente `render.yaml`
5. Click en **"Apply"**

#### 3. Configurar variables de entorno

En **Environment** del dashboard, configura:

| Variable | Valor | Notas |
|----------|-------|-------|
| `GROQ_API_KEY` | `gsk_...` | Requerida - obtener en [Groq Console](https://console.groq.com) |
| `GMAIL_SENDER` | `tu@gmail.com` | Email remitente |
| `GMAIL_RECIPIENT` | `tu@gmail.com` | Email destinatario |
| `GMAIL_CLIENT_SECRET_JSON` | `{"installed":{...}}` | JSON completo de `client_secret.json` (ver paso 4) |
| `GMAIL_TOKEN_JSON` | `{"access_token":...}` | JSON completo de `gmail-token.json` (ver paso 4) |
| `MORNING_DIGEST_TIME` | `08:00` | Opcional - hora del digest matutino |
| `EVENING_DIGEST_TIME` | `20:00` | Opcional - hora del digest nocturno |
| `DIGEST_TIMEZONE` | `America/Bogota` | Opcional - zona horaria IANA |

#### 4. Configurar secretos OAuth de Gmail

El adapter de Gmail soporta **dos modos** de carga de credenciales:

**Modo producción (Render):** Variables de entorno con JSON completo.

1. Abre tu archivo local `.secrets/client_secret.json`
2. Copia **todo el contenido** del archivo
3. En Render Dashboard → **Environment** → **Add Environment Variable**
4. Key: `GMAIL_CLIENT_SECRET_JSON`, Value: (pega el JSON completo)
5. Repite con `.secrets/gmail-token.json` → Key: `GMAIL_TOKEN_JSON`
6. Click en **"Save Changes"** → Render hará redeploy automáticamente

El adapter detecta estas variables, las materializa como archivos temporales y las pasa a simplegmail. Esto funciona sin necesidad de Shell ni acceso a disco persistente.

**Modo desarrollo (local):** Archivos en disco.

En desarrollo local, el adapter sigue usando los archivos `.secrets/client_secret.json` y `.secrets/gmail-token.json` vía las variables `GMAIL_CLIENT_SECRET_PATH` y `GMAIL_TOKEN_PATH`. No es necesario cambiar nada.

> **Prioridad de resolución:**
> `GMAIL_CLIENT_SECRET_JSON` > `GMAIL_CLIENT_SECRET_PATH` > default `.secrets/client_secret.json`

#### 5. Configurar UptimeRobot (mantener servicio activo)

El free tier de Render duerme servicios sin tráfico HTTP después de 15 min de inactividad.

**Solución:** Configurar un monitor externo que haga ping cada 5 minutos.

1. Regístrate en [UptimeRobot](https://uptimerobot.com) (gratis)
2. Crea un monitor:
   - **Monitor Type:** HTTP(s)
   - **URL:** `https://ada-scheduler.onrender.com/health`
   - **Monitoring Interval:** 5 minutes
3. Guarda el monitor

Ahora UptimeRobot hará ping cada 5 min, manteniendo el servicio activo 24/7.

### Verificar deployment

1. **Health check:** Visita `https://ada-scheduler.onrender.com/health`
   - Debe retornar: `{"status": "ok", "service": "ada-scheduler", "timestamp": "..."}`

2. **Logs del scheduler:** En Render Dashboard → Logs
   - Busca: `"🚀 Iniciando scheduler de digest en background thread..."`
   - Busca: `"✅ Scheduler thread iniciado"`
   - A las 08:00 y 20:00 (hora configurada) verás logs de ejecución del digest

3. **Recepción de emails:** Verifica tu Gmail a las horas programadas

### Limitaciones del Free Tier

- **750 horas/mes:** Suficiente para **1 servicio** corriendo 24/7 (~720h/mes)
- **Sleep automático:** Si no hay tráfico HTTP por 15 min (mitigado con UptimeRobot)
- **CPU/RAM compartidos:** Rendimiento limitado pero suficiente para Ada

### Troubleshooting

| Problema | Solución |
|----------|----------|
| Build falla: `"--no-dev" does not exist` | Actualizar `render.yaml`: `poetry install --without dev` |
| Build falla: "Poetry not found" | `render.yaml` incluye `pip install poetry` en buildCommand |
| Servicio se duerme | Configurar UptimeRobot (ver paso 5) |
| Gmail: "credentials not found" | Verificar que `GMAIL_CLIENT_SECRET_JSON` y `GMAIL_TOKEN_JSON` están configuradas en Environment |
| Gmail: "JSON no válido" | Revisar en los logs: "no contiene JSON válido". Asegurarse de copiar el JSON completo sin saltos de línea extra |
| Digest no se ejecuta | Verificar timezone y horarios en variables de entorno |
| "ZoneInfoNotFoundError" | Proyecto incluye `tzdata` en dependencias (compatible con Render) |

### Comandos útiles

```bash
# Ver logs en tiempo real (local)
poetry run uvicorn server:app --reload

# Probar health check local
curl http://localhost:8000/health

# Ver documentación interactiva (local)
# Visita: http://localhost:8000/docs
```

## Guía interna del proyecto

Las instrucciones de trabajo están en:

- `.github/copilot-instructions.md`
- `.github/instructions/architecture.md`
- `.github/instructions/code-patterns.md`
- `.github/instructions/coding-guidelines.md`
- `.github/instructions/code-practices.md`
- `.github/instructions/business-rules.md`

## Autora

Karen Rincón

