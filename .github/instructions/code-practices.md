# Code Practices Instructions

## Calidad y code smells

- Detectar y corregir code smells temprano.
- Evitar funciones largas con múltiples objetivos.
- Evitar clases con responsabilidades mezcladas.
- Preferir nombres expresivos sobre comentarios extensos.

## Reglas estructurales

- Funciones con responsabilidad única.
- Una clase por archivo.
- Scripts con máximo 100 líneas.
- Usar type hints cuando el nombre de función no haga obvio el contrato.

## Reglas de mantenibilidad

- Reducir acoplamiento entre módulos.
- Favorecer composición sobre herencia compleja.
- Mantener dependencias externas encapsuladas en adaptadores.
- Evitar utilidades globales sin contexto de dominio.

## Documentación separada

- La documentación técnica/funcional se mantiene fuera de `src`.
- Carpeta base de documentación: `docs/`.
- La estructura de `docs/` debe reflejar divisiones de `src/app`.

## Estilo y formato

- Black como formateador por defecto.
- Longitud máxima de línea: 79 caracteres.
- Consistencia de estilo en todo el proyecto.
