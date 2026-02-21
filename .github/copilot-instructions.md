# Copilot Instructions - Ada

## Contexto del proyecto

Ada es un agente personal para programadores que diariamente:

1. Consulta novedades sobre IA, programación y curiosidades de algoritmos.
2. Resume y organiza contenido relevante.
3. Envía un correo HTML al Gmail personal del propietario.

Stack objetivo:

- LangChain + Gemini API para razonamiento/generación.
- simplegmail para envío de correos (Gmail API via OAuth2).
- Python como lenguaje principal.

## Prioridades del asistente

1. Respetar arquitectura hexagonal + clean architecture.
2. Mantener separación de contextos `agent` y `notifications`.
3. Entregar cambios pequeños, verificables y con bajo acoplamiento.
4. Seguir flujo de planificación antes de escribir código.

## Qué archivo consultar según la tarea

- Arquitectura y capas:
  - `./instructions/architecture.md`
- Patrones de diseño y principios:
  - `./instructions/code-patterns.md`
- Flujo de trabajo para implementar cambios:
  - `./instructions/coding-guidelines.md`
- Calidad de código, smells y reglas de estructura:
  - `./instructions/code-practices.md`
- Reglas de negocio del dominio Ada:
  - `./instructions/business-rules.md`

## Flujo de uso recomendado

Antes de implementar:

1. Consultar `coding-guidelines.md`.
2. Revisar `architecture.md` para validar límites de capa.
3. Aplicar `code-patterns.md` y `code-practices.md` durante el desarrollo.
4. Verificar `business-rules.md` para no romper reglas del producto.
