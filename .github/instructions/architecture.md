# Architecture Instructions

## Estilo arquitectónico

Este proyecto aplica:

- Arquitectura Hexagonal (Ports and Adapters)
- Principios de Clean Architecture

## Capas y responsabilidades

### domain

- Contiene entidades, value objects y eventos de dominio.
- No depende de frameworks, librerías externas ni infraestructura.
- Debe ser código puro y testeable de forma aislada.

### application

- Define casos de uso y puertos (interfaces).
- Orquesta flujo de negocio usando `domain`.
- Puede depender de `domain`, nunca de `infrastructure` concreta.

### infrastructure

- Implementa adaptadores de entrada/salida.
- Integra con LangChain, Gemini API, pygmail y elementos externos.
- Depende de `application` para implementar puertos.

## Reglas de dependencia

1. `domain` no conoce `application` ni `infrastructure`.
2. `application` conoce `domain` y contratos, no detalles externos.
3. `infrastructure` depende de contratos de `application`.
4. En dependencias circulares, mover contratos a `application/ports`.

## Contextos actuales

### src/app/agent

- Responsabilidad: investigación, curación y resumen técnico.
- Capas:
  - `application/ports`
  - `application/use_cases`
  - `domain/entities|events|value_objects`
  - `infrastructure/driven_adapters/langgraph/*`
  - `infrastructure/driving_adapters/*`

### src/app/notifications

- Responsabilidad: composición y envío de correos HTML.
- Capas:
  - `application/ports`
  - `application/use_cases`
  - `domain/entities|events|value_objects`
  - `infrastructure/driven_adapters/langgraph/*`
  - `infrastructure/driving_adapters/*`

## Reglas prácticas de implementación

- Casos de uso en `application/use_cases`.
- Interfaces de integración en `application/ports`.
- Adaptadores concretos en `infrastructure/driven_adapters`.
- Entradas API/config/router en `infrastructure/driving_adapters`.
- Evitar lógica de negocio en controladores, routers y handlers.
