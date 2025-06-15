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

class Aereo(Vehiculo):
    def __init__(self):
        super().__init__(velocidad=600, carga=5000, costoFijo=750, costoKm=40, costoKg=10)

class Automotor(Vehiculo):
    def __init__(self):
        super().__init__(velocidad=80, carga=30000, costoFijo=30, costoKm=5, costoKg=1)

class Maritimo(Vehiculo):
    def __init__(self):
        super().__init__(velocidad=40, carga=100000, costoFijo=500, costoKm=15, costoKg=2)
