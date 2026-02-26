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

