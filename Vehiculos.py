import random

class Vehiculo:
    def __init__(self, velocidad,carga,costoFijo,costoKm,costoKg ):
         self.velocidad = velocidad
         self.carga = carga
         self.costoFijo = costoFijo
         self.costoKm = costoKm
         self.costoKg = costoKg
    
class Ferroviario(Vehiculo):
    def __init__(self):
        super().__init__(velocidad=100, carga=150000, costoFijo=100, costoKm=20, costoKg=3)
    
    def restriccion_Ferroviaria(self, distancia):
        costo = self.costoKm
        if distancia >= 200:
            costo = 15
            return costo
        else:
            return self.costoKm
        
class Aereo(Vehiculo):
    def __init__(self):
        super().__init__(velocidad=600, carga=5000, costoFijo=750, costoKm=40, costoKg=10)

    def restriccion_Aerea(self, tramo):
        if tramo.restriccion == "prob_mal_tiempo":
            if random.random() < tramo.valor_restriccion:
                return 400, True  # velocidad reducida, mal tiempo ocurrió
        return self.velocidad, False
    
class Automotor(Vehiculo):
    def __init__(self):
        super().__init__(velocidad=80, carga=30000, costoFijo=30, costoKm=5, costoKg=1)
    
    def restriccion_Automotor(self, peso):
        autos_llenos = peso // self.carga
        extra = 0
        if autos_llenos >= 1:
            extra += autos_llenos * 2 * self.carga
            restante = peso - (self.carga * autos_llenos)
            extra += restante if restante < 15000 else 2 * restante #1*kilos, 15001 y 30k, 2*restante
        else:
            extra += peso
        return extra

class Maritimo(Vehiculo):
    def __init__(self):
        super().__init__(velocidad=40, carga=100000, costoFijo=500, costoKm=15, costoKg=2)

    def restriccion_Maritima(self, tramo):
        if tramo.restriccion == "tipo" and tramo.valor_restriccion == "maritimo":
            return 1500
        return self.costoFijo
    
