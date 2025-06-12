class Vehiculos:
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg):
        self.velocidad = velocidad
        self.carga = carga
        self.costoFijo = costoFijo
        self.costoKm = costoKm
        self.costoKg = costoKg


    def calcular_costo_tramo(self, distancia_km, peso_carga, tipo_restriccion_tramo=None, valor_restriccion_tramo=None):
        # Este método será sobrescrito en las subclases para manejar las particularidades
        costo_total = self.costoFijo + (self.costoKm * distancia_km) + (self.costoKg * peso_carga)
        return costo_total

    def calcular_tiempo_tramo(self, distancia_km, tipo_restriccion_tramo=None, valor_restriccion_tramo=None):
        if self.velocidad == 0:
            return float('inf') # Evitar división por cero
        return distancia_km / self.velocidad

class Ferroviario(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=100, carga=150000, costoFijo=100, costoKm=20, costoKg=3)

    def calcular_costo_tramo(self, distancia_km, peso_carga, tipo_restriccion_tramo=None, valor_restriccion_tramo=None):
        costo_km_variable = 20 if distancia_km < 200 else 15
        costo_total = self.costoFijo + (costo_km_variable * distancia_km) + (self.costoKg * peso_carga)
        return costo_total

    # No se menciona variación de tiempo para ferroviario, así que la base está bien.

class Aereo(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=600, carga=5000, costoFijo=750, costoKm=40, costoKg=10)

    def calcular_tiempo_tramo(self, distancia_km, tipo_restriccion_tramo=None, valor_restriccion_tramo=None):
        velocidad_real = self.velocidad
        if tipo_restriccion_tramo == "Prob_mal_tiempo" and valor_restriccion_tramo >= 0.3: # Mayor o igual a 0.3 es mucha probabilidad de mal tiempo
            velocidad_real = 400
        if velocidad_real == 0:
            return float('inf')
        return distancia_km / velocidad_real



class Automotor(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=80, carga=30000, costoFijo=30, costoKm=5, costoKg=1)

    def calcular_costo_tramo(self, distancia_km, peso_carga, tipo_restriccion_tramo=None, valor_restriccion_tramo=None):
        costo_kg_variable = 1 if peso_carga < 15000 else 2
        costo_total = self.costoFijo + (self.costoKm * distancia_km) + (costo_kg_variable * peso_carga)
        return costo_total


class Maritimo(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=40, carga=100000, costoFijo=500, costoKm=15, costoKg=2)

    def calcular_costo_tramo(self, distancia_km, peso_carga, tipo_restriccion_tramo=None, valor_restriccion_tramo=None):
        costo_fijo_variable = self.costoFijo # Default a fluvial
        if tipo_restriccion_tramo == "tipo" and valor_restriccion_tramo == "maritimo": # Asumiendo 1500 es la tasa maritima
             costo_fijo_variable = 1500 # Si el tramo es marítimo, el costo fijo es $1500
        elif tipo_restriccion_tramo == "tipo" and valor_restriccion_tramo == "fluvial": # Asumiendo 500 es la tasa fluvial
            costo_fijo_variable = 500
            
        costo_total = costo_fijo_variable + (self.costoKm * distancia_km) + (self.costoKg * peso_carga)
        return costo_total

    # No se menciona variación de tiempo para maritimo, así que la base está bien.





# class Vehiculos:
#     def __init__(self, velocidad,carga,costoFijo,costoKm,costoKg ):
#         self.velocidad = velocidad
#         self.carga = carga
#         self.costoFijo = costoFijo
#         self.costoKm = costoKm
#         self.costoKg = costoKg

    
# class Ferroviario(Vehiculos):
#     def __init__(self):
#         Vehiculos.__init__( velocidad = 100,
#         carga = 150000,
#         costoFijo = 100,
#         costoKm = 20,
#         costoKg= 3)

    
# class Aereo(Vehiculos):
#     def __init__(self):
#         Vehiculos.__init__( velocidad = 600,
#         carga = 5000,
#         costoFijo = 750,
#         costoKm = 40,
#         costoKg= 10)

    
# class Automotor(Vehiculos):
#     def __init__(self):
#         Vehiculos.__init__( velocidad = 80,
#         carga = 30000,
#         costoFijo = 30,
#         costoKm = 5,
#         costoKg= 1)

    
# class Maritimo(Vehiculos):
#     def __init__(self):
#         Vehiculos.__init__( velocidad = 40,
#         carga = 100000,
#         costoFijo = 500,
#         costoKm = 15,
#         costoKg= 2)