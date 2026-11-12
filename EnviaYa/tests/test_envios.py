import os
import sys

import pytest  # type: ignore

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from envios import calc  # noqa: E402


# ---------- R1, R2: validaciones (CP01-CP05) ----------
@pytest.mark.parametrize("peso", [0, 51])
def test_cp01_cp02_peso_invalido(peso):
    with pytest.raises(ValueError):
        calc(peso, "urbana", "normal", 3)


def test_cp03_zona_invalida():
    with pytest.raises(ValueError):
        calc(5, "aerea", "normal", 3)


@pytest.mark.parametrize("dia", [8, 0])
def test_cp04_cp05_dia_invalido(dia):
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", dia)


# ---------- R3: tarifa base (CP06-CP11) ----------
@pytest.mark.parametrize(
    "peso, esperado",
    [
        (0.1, 6000),    # CP06
        (3, 6000),      # CP07 (L1 incluido)
        (3.01, 9000),   # CP08
        (10, 9000),     # CP09 (L2 incluido)
        (10.5, 9400),   # CP10: 9000 + 0.5*800
        (50, 41000),    # CP11: 9000 + 40*800
    ],
)
def test_r3_tarifa_base(peso, esperado):
    assert calc(peso, "urbana", "normal", 3) == esperado


# ---------- R4: zona (CP12-CP13) ----------
def test_cp12_rural():
    assert calc(5, "rural", "normal", 3) == 11300


def test_cp13_nacional():
    assert calc(5, "nacional", "normal", 3) == 12600


# ---------- R5: sabado (CP14) ----------
def test_cp14_sabado():
    assert calc(5, "urbana", "normal", 6) == 11000


# ---------- R7: cupon inexistente (CP15) ----------
def test_cp15_cupon_inexistente():
    assert calc(5, "urbana", "normal", 3, "PROMO99") == 9000


# ---------- R8: minimo 5000 (CP16) ----------
def test_cp16_minimo():
    assert calc(3, "urbana", "vip", 3, "ENVIO10") == 5000


# ---------- Tabla de decisión (CP17-CP28) ----------
@pytest.mark.parametrize(
    "cliente, cupon, dia, esperado",
    [
        ("normal",    None,      3, 9000),    # CP17
        ("normal",    None,      7, 11000),   # CP18
        ("normal",    "ENVIO10", 3, 8100),    # CP19
        ("normal",    "ENVIO10", 7, 10100),   # CP20
        ("frecuente", None,      3, 8600),    # CP21
        ("frecuente", None,      7, 10600),   # CP22
        ("frecuente", "ENVIO10", 3, 7700),    # CP23
        ("frecuente", "ENVIO10", 7, 9700),    # CP24
        ("vip",       None,      3, 7700),    # CP25
        ("vip",       None,      7, 9700),    # CP26
        ("vip",       "ENVIO10", 3, 6900),    # CP27
        ("vip",       "ENVIO10", 7, 8900),    # CP28
    ],
)
def test_tabla_decision(cliente, cupon, dia, esperado):
    assert calc(5, "urbana", cliente, dia, cupon) == esperado


# ---------- CP29: caja blanca (flag) ----------
def test_cp29_calc_no_imprime(capsys):
    assert calc(5, "urbana", "normal", 3) == 9000
    assert capsys.readouterr().out == ""


# ---------- Ejemplos de verificación ----------
def test_ejemplo_1_rural_vip_sabado_cupon():
    assert calc(3, "rural", "vip", 6, "ENVIO10") == 7700


def test_ejemplo_2_nacional_frecuente_domingo():
    assert calc(12, "nacional", "frecuente", 7) == 16100


# ---------- Parte 8: cliente empresarial (12 %; sin recargo de zona si peso > L2) ----------
@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon, esperado",
    [
        (5,    "urbana",   "empresarial", 3, None,      7900),    # CE01
        (5,    "rural",    "empresarial", 3, None,      9900),    # CE02
        (12,   "rural",    "empresarial", 3, None,      9300),    # CE03
        (12,   "nacional", "empresarial", 3, None,      9300),    # CE04
        (10,   "rural",    "empresarial", 3, None,      9900),    # CE05
        (10.5, "rural",    "empresarial", 3, None,      8300),    # CE06
        (12,   "rural",    "frecuente",   3, None,      12600),   # CE07
        (5,    "urbana",   "empresarial", 7, "ENVIO10", 9100),    # CE08
        (12,   "rural",    "empresarial", 7, "ENVIO10", 10400),   # CE09
        (3,    "urbana",   "empresarial", 3, "ENVIO10", 5000),    # CE10
    ],
)
def test_cliente_empresarial(peso, zona, cliente, dia, cupon, esperado):
    assert calc(peso, zona, cliente, dia, cupon) == esperado