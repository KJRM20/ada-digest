# Ada Back

Backend del proyecto Ada, un agente personal que prepara un resumen técnico
diario para programadores y lo envía por correo en formato HTML.

## ¿Qué hace Ada?

Cada día:

1. Consulta novedades de IA aplicada al desarrollo.
2. Recolecta noticias de programación en general.
3. Incluye curiosidades útiles de algoritmos y código.
4. Organiza el contenido para lectura rápida por desarrolladores.
5. Envía un correo HTML al Gmail personal configurado.

## Tecnologías

- Python
- LangChain
- Gemini API
- pygmail
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

Desde la raíz del proyecto:

```bash
poetry run python main.py
```

## Configuración de desarrollo

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

