# Code Patterns Instructions

## Principios base

## SOLID

- Single Responsibility: cada clase/módulo cumple un objetivo claro.
- Open/Closed: extender por composición y puertos, evitar modificar lógica estable.
- Liskov: implementaciones de puertos deben mantener contratos.
- Interface Segregation: puertos pequeños y específicos por caso de uso.
- Dependency Inversion: casos de uso dependen de abstracciones, no adaptadores.

## DRY

- Evitar duplicación en mapeos, validaciones y construcción de prompts/templates.
- Extraer utilidades reutilizables cuando la duplicación sea semántica.
- No abstraer prematuramente: duplicación puntual aceptable hasta confirmar patrón.

## KISS

- Elegir la solución más simple que cumpla el requerimiento.
- Minimizar número de capas/adaptadores adicionales sin necesidad real.
- Evitar complejidad accidental en flujos diarios de ingesta y envío.

## Observer (event-driven)

- Usar eventos de dominio para desacoplar acciones derivadas.
- Ejemplo: `ResumenDiarioGenerado` puede disparar proceso de notificación.
- Evitar que un caso de uso conozca detalles internos de otro contexto.

## Antipatrones a evitar

- Lógica de negocio en adaptadores HTTP/router.
- Clases utilitarias gigantes con múltiples responsabilidades.
- Interfaces genéricas ambiguas (`IService`, `IManager`) sin intención clara.
- Acoplar `agent` con `notifications` por imports concretos de infraestructura.
