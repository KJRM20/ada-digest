# Business Rules Instructions

## Propósito del producto

Ada entrega un resumen diario por correo para programadores, con foco técnico.

## Reglas de contenido

1. Priorizar noticias para desarrolladores, no público general.
2. Cubrir tres líneas principales:
   - IA aplicada al desarrollo.
   - Programación en general (herramientas, frameworks, prácticas).
   - Datos curiosos de algoritmos/código.
3. Favorecer utilidad práctica y contexto técnico.

## Reglas de frecuencia y entrega

1. Generación y envío: frecuencia diaria.
2. Canal de salida: correo Gmail personal.
3. Formato de salida: plantilla HTML ordenada.
4. Se permite incluir ejemplos de código cuando agreguen valor.

## Reglas de stack y capacidades

1. El razonamiento/generación usa LangChain + Gemini API.
2. El envío de correo usa simplegmail (Gmail API via OAuth2).
3. El sistema debe ser trazable por contexto (`agent` y `notifications`).

## Criterios mínimos de calidad del resumen

- Claridad: cada bloque debe ser entendible rápidamente.
- Relevancia: incluir solo contenido útil para programadores.
- Organización: estructura consistente por secciones.
- Brevedad: evitar ruido y relleno.
