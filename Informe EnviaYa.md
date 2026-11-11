# UNIVERSIDAD DE LA GUAJIRA

**Facultad de Ingenierías**\
**Programa de Ingeniería de Sistemas**

## Parcial 3 – Ingeniería de Software I (273365)

### Punto único: Equipo de calidad y mantenimiento de EnvíaYa

**Estudiante: Jaime Rafael González Ballesta**

**Código estudiantil: 0182410070**

**Asignatura: Ingeniería de Software I (273365)**

**Grupo / Semestre: B1 · VI semestre**

**Docente: Ing. Robert Damián Quintero Laverde**

**Período: 2026-2 · Tercer corte**

**Fecha: Miércoles 11 de noviembre de 2026**

**Unidades: 6. Pruebas · 7. Evolución**

**Repositorio: [EnvíaYa](https://github.com/Jaimxgonzalez/Ing-software?utm_source=chatgpt.com)**

## Mis parámetros

Para determinar mis parámetros, tomo los últimos seis dígitos de mi código estudiantil (**410070**), de los cuales obtengo:

**A = 4, B = 1, C = 0, D = 0, E = 7, F = 0.**

| **A** | **B** | **C** | **D** | **E** | **F** | **PMAX** | **L1** | **L2** | **RR** | **RN** | **V** | **S** | **CAMBIO** |
|----|----|----|------|----|----|------|------|------|------|------|------|------|------|
| 4 | 1 | 0 | 0 | 7 | 0 | 50 kg | 3 kg | 10 kg | 25 % | 40 % | 15 % | \$2.000 | 1 |

### Cálculo de los parámetros

| **Parámetro** | **Fórmula**            | **Resultado** |
|---------------|------------------------|---------------|
| PMAX          | 30 + 5 × 4             | 50 kg         |
| L1            | 2 + (1 mod 3)          | 3 kg          |
| L2            | 10 + 0                 | 10 kg         |
| RR            | 10 + 5 × (7 mod 4)     | 25 %          |
| RN            | 40 + 5 × (0 mod 3)     | 40 %          |
| V             | 10 + 5 × (4 mod 3)     | 15 %          |
| S             | 2000 + 500 × (0 mod 4) | \$2.000       |
| CAMBIO        | (4 + 0) mod 3          | 1             |

### Reglas según la paridad de mis dígitos

| **Dígito** | **Valor** | **Regla que me aplica** |
|----|----|----|
| D · Tramo 1 | 0 (par) | Se incluye el límite: peso ≤ 3 kg. |
| E · Recargo de fin de semana | 7 (impar) | El recargo se suma **después de aplicar los descuentos**. |
| B · Cliente y cupón | 1 (impar) | Se aplican **ambos descuentos**: primero el del cliente y luego el del cupón. |
| F · Cupón inexistente | 0 (par) | El cupón inexistente se **ignora**. |

De acuerdo con mis parámetros, calculo la solicitud de cambio de la siguiente manera:

[CAMBIO = (A + F) \\bmod 3]

[CAMBIO = (4 + 0) \\bmod 3 = 1]

**Resultado:** Se me asigna el cambio número **1**, correspondiente a la incorporación de un nuevo tipo de cliente empresarial con un **12 % de descuento**.

Adicionalmente, cuando el peso del envío sea superior a **L2 (10 kg)**, no se cobrará el recargo de zona.

# Parte 1 · Requisitos y criterios de aceptación

## 1.1 Especificación (con mis valores)

| ID | Regla |
|---------------------------|---------------------------------------------|
| R1 | El peso debe cumplir 0 \< peso ≤ 50 kg. Si no, error "peso inválido". |
| R2 | Si la zona no es urbana, rural o nacional, o el día no está entre 1 y 7, se lanza error. |
| R3 | Tarifa base: peso ≤ 3 kg → \$6.000. Hasta 10 kg (inclusive) → \$9.000. Más de 10 kg → \$9.000 + \$800 por cada kg sobre 10 (proporcional). |
| R4 | Recargo por zona: rural +25 %, nacional +40 %, urbana sin recargo. |
| R5 | Fin de semana (día 6 y 7): +\$2.000, sumado DESPUÉS de los descuentos. |
| R6 | Frecuente 5 %, VIP 15 %, cupón ENVIO10 10 %. Se aplican ambos: primero el del cliente y luego el cupón. |
| R7 | Un cupón que no existe se ignora. |
| R8 | El costo nunca es menor a \$5.000. Se redondea al múltiplo de \$100 más cercano; los \$50 suben. |

## 1.2 Historias de usuario

### HU-1 · Validación de datos (R1, R2, R7)

*Como operador de EnvíaYa, quiero que el sistema rechace datos inválidos, para no cobrar mal un envío.*

1.  **Dado** un peso de 0 kg (o de 51 kg), **cuando** calculo el costo, **entonces** se lanza el error "peso inválido".
2.  **Dado** una zona "aérea" o un día 8, **cuando** calculo el costo, **entonces** se lanza un error.
3.  **Dado** un cupón "PROMO99" que no existe, **cuando** calculo el costo, **entonces** se ignora y se calcula como si no hubiera cupón.

### HU-2 · Tarifa por peso, zona y día (R3, R4, R5)

*Como cliente, quiero que el costo dependa del peso, la zona y el día, para pagar un precio justo.*

1.  **Dado** un peso de 3 kg en zona urbana, **cuando** calculo, **entonces** la tarifa base es \$6.000.
2.  **Dado** un peso de 12 kg en zona nacional, **cuando** calculo, **entonces** la base es \$10.600 y con el recargo del 40 % queda en \$14.840.
3.  **Dado** un envío en sábado o domingo, **cuando** calculo, **entonces** se suman \$2.000 después de los descuentos.

### HU-3 · Descuentos, mínimo y redondeo (R6, R8)

*Como cliente frecuente o VIP, quiero que se apliquen mis descuentos y mi cupón, para ahorrar.*

1.  **Dado** un cliente VIP con cupón ENVIO10, **cuando** calculo, **entonces** se aplica primero 15 % y luego 10 % sobre el resultado.
2.  **Dado** un costo calculado menor a \$5.000, **cuando** se finaliza, **entonces** el resultado es \$5.000.
3.  **Dado** un costo de \$7.737,5, **cuando** se redondea, **entonces** el resultado es \$7.700.

## 1.3 Matriz de trazabilidad

| Requisito | Historia | Casos de prueba          |
|-----------|----------|--------------------------|
| R1        | HU-1     | (se completa en Parte 3) |
| R2        | HU-1     | (se completa en Parte 3) |
| R3        | HU-2     | (se completa en Parte 3) |
| R4        | HU-2     | (se completa en Parte 3) |
| R5        | HU-2     | (se completa en Parte 3) |
| R6        | HU-3     | (se completa en Parte 3) |
| R7        | HU-1     | (se completa en Parte 3) |
| R8        | HU-3     | (se completa en Parte 3) |
