"""Calculo del costo de envio de EnviaYa."""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.25,
    "RECARGO_NACIONAL": 0.40,
    "DESC_VIP": 0.15,
    "RECARGO_FINDE": 2000,  # pesos
}

PESO_MAX = 50
TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_EXTRA = 800
DESC_FRECUENTE = 0.05
DESC_CUPON_ENVIO10 = 0.10
COSTO_MINIMO = 5000
MULTIPLO_REDONDEO = 100
DIA_MIN = 1
DIA_SABADO = 6
DIA_MAX = 7


# ---------- Patron Estrategia ----------
class Ajuste(ABC):
    """Interfaz: recibe un valor y devuelve el valor ajustado."""

    @abstractmethod
    def aplicar(self, valor):
        """Devuelve el valor despues de aplicar el ajuste."""


class SinAjuste(Ajuste):
    """No modifica el valor."""

    def aplicar(self, valor):
        return valor


class Recargo(Ajuste):
    """Suma un porcentaje al valor."""

    def __init__(self, porcentaje):
        self.porcentaje = porcentaje

    def aplicar(self, valor):
        return valor * (1 + self.porcentaje)


class Descuento(Ajuste):
    """Resta un porcentaje al valor."""

    def __init__(self, porcentaje):
        self.porcentaje = porcentaje

    def aplicar(self, valor):
        return valor * (1 - self.porcentaje)


SIN_AJUSTE = SinAjuste()

ZONAS = {
    "urbana": SIN_AJUSTE,
    "rural": Recargo(CONFIG["RECARGO_RURAL"]),
    "nacional": Recargo(CONFIG["RECARGO_NACIONAL"]),
}
CLIENTES = {
    "frecuente": Descuento(DESC_FRECUENTE),
    "vip": Descuento(CONFIG["DESC_VIP"]),
}
CUPONES = {
    "ENVIO10": Descuento(DESC_CUPON_ENVIO10),
}


# ---------- Funciones extraidas ----------
def _validar(peso, zona, dia):
    """Lanza ValueError si peso, dia o zona no son validos."""
    if peso <= 0 or peso > PESO_MAX:
        raise ValueError("peso invalido")
    if dia < DIA_MIN or dia > DIA_MAX:
        raise ValueError("dia invalido")
    if zona not in ZONAS:
        raise ValueError("zona invalida")


def _tarifa_base(peso):
    """Tarifa segun el tramo de peso, antes de recargos y descuentos."""
    if peso <= CONFIG["L1"]:
        return TARIFA_TRAMO_1
    if peso <= CONFIG["L2"]:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - CONFIG["L2"]) * TARIFA_KG_EXTRA


def _redondear(valor):
    """Redondea al multiplo de 100 mas cercano; los 50 suben."""
    cociente = Decimal(str(valor)) / MULTIPLO_REDONDEO
    return int(cociente.quantize(Decimal(1), rounding=ROUND_HALF_UP)) * MULTIPLO_REDONDEO


def calc(peso, zona, cliente, dia, cupon=None):
    """Costo del envio en pesos."""
    _validar(peso, zona, dia)
    total = _tarifa_base(peso)
    total = ZONAS[zona].aplicar(total)
    total = CLIENTES.get(cliente, SIN_AJUSTE).aplicar(total)
    total = CUPONES.get(cupon, SIN_AJUSTE).aplicar(total)  # cupon inexistente se ignora (F par)
    if dia >= DIA_SABADO:  # despues de descuentos (E impar)
        total = total + CONFIG["RECARGO_FINDE"]
    total = max(total, COSTO_MINIMO)
    return _redondear(total)