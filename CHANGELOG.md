# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Sin publicar]
## [2.1.0] - 2026-11-11

### Añadido
- Nuevo tipo de cliente `empresarial` con 12 % de descuento, combinable con cupón.
- El cliente empresarial no paga recargo de zona cuando el peso es mayor que L2 (10 kg).
- 10 casos de prueba nuevos (CE01 a CE10).
## [2.0.0] - 2026-11-11

### Cambiado
- **CAMBIO INCOMPATIBLE:** se elimina el parámetro `flag` de `calc`. Ya no imprime el costo; quien lo necesite debe imprimir el valor devuelto.
- Zonas, descuentos de cliente y cupones se resuelven con el patrón Estrategia (`Ajuste`, `Recargo`, `Descuento`).
- Se extraen las funciones `_validar`, `_tarifa_base` y `_redondear`.
- Los números mágicos pasan a constantes con nombre y se mejoran los nombres de variables.

### Eliminado
- Parámetro `flag` y su `print` de depuración.

## [1.0.1] - 2026-11-11

### Corregido
- DEF-01: `calc` lanza `ValueError` si la zona no es urbana, rural o nacional (R2).
- DEF-02: `calc` lanza `ValueError` si el día no está entre 1 y 7 (R2).
- DEF-03: el sábado (día 6) también cobra el recargo de fin de semana (R5).
- DEF-04: el recargo de fin de semana se suma después de los descuentos (R5).
- DEF-05: el resultado se redondea al múltiplo de $100 más cercano, con $50 hacia arriba, en lugar de truncar (R8).

### Cambiado
- Limpieza sin cambio de comportamiento: se quitó un `elif` duplicado y comentarios de depuración.

## [1.0.0] - 2026-11-11

### Añadido
- Versión heredada de `calc` con mi configuración (L1=3, L2=10, rural 25 %, nacional 40 %, VIP 15 %, fin de semana $2.000), sin modificar. Contiene los defectos DEF-01 a DEF-05.

[Sin publicar]: https://github.com/Jaimxgonzalez/Ing-software/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/Jaimxgonzalez/Ing-software/compare/v2.0.0...v2.1.0
[1.0.1]: https://github.com/Jaimxgonzalez/Ing-software/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/Jaimxgonzalez/Ing-software/releases/tag/v1.0.0
