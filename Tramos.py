# Tramos.py
class Tramo():
    def __init__(self, origen: str, destino: str, tipo: str, distancia_km: float):
        self.origen = origen
        self.destino = destino
        self.tipo = tipo
        self.distancia_km = distancia_km
        self.restriccion = None
        self.valor_restriccion = None

    def __eq__(self, otro):
        if not isinstance(otro, Tramo):
            return NotImplemented

        return (self.origen == otro.origen and self.destino == otro.destino and self.tipo == otro.tipo) or \
               (self.origen == otro.destino and self.destino == otro.origen and self.tipo == otro.tipo)

    def __hash__(self):
        return hash(frozenset({self.origen, self.destino, self.tipo}))


class TramoAereo(Tramo):
    def __init__(self, origen: str, destino: str, tipo: str, distancia_km: float, restriccion: str = None, valor_restriccion: float = None):
        super().__init__(origen, destino, "Aerea", distancia_km) 
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion

class TramoAutomor(Tramo):
    def __init__(self, origen: str, destino: str, tipo: str, distancia_km: float, restriccion: str = None, valor_restriccion: float = None):
        super().__init__(origen, destino, "Automotor", distancia_km)
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion

class TramoMaritimo(Tramo):
    def __init__(self, origen: str, destino: str, tipo: str, distancia_km: float, restriccion: str = None, valor_restriccion: float = None):
        super().__init__(origen, destino, "Fluvial", distancia_km) 
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion

class TramoFerroviario(Tramo):
    def __init__(self, origen: str, destino: str, tipo: str, distancia_km: float, restriccion: str = None, valor_restriccion: float = None):
        super().__init__(origen, destino, "Ferroviaria", distancia_km)
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion