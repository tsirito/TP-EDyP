# Vehiculos.py
import math

class Vehiculos: 
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg):
        self.velocidad = velocidad
        self.carga = carga
        self.costoFijo = costoFijo
        self.costoKm = costoKm
        self.costoKg = costoKg

    def calcular_vehiculos_necesarios(self, peso_carga: float) -> int:
        """
        Calcula cuántos vehículos de este tipo son necesarios para transportar la carga.
        Devuelve 0 si la carga es 0, o 1 si la carga es positiva pero no supera la capacidad.
        Si supera, calcula ceil(carga / capacidad).
        """
        if peso_carga <= 0:
            return 0
        return math.ceil(peso_carga / self.carga)

    def calcular_costo_tramo(self, distancia_km: float, peso_carga: float, tipo_restriccion_tramo: str = None, valor_restriccion_tramo: float = None) -> float:
        """
        Calcula el costo total de un tramo, considerando múltiples vehículos si es necesario.
        Este método es la base y será sobrescrito en las subclases.
        """
        num_vehiculos = self.calcular_vehiculos_necesarios(peso_carga)
        if num_vehiculos == 0:
            return 0.0

        # Costo base por un solo vehículo
        costo_unitario_fijo = self.costoFijo 
        costo_unitario_km = self.costoKm * distancia_km
        # Para el costo por kg, lo aplicamos al peso total de la carga (aunque se reparta)
        # o se asume que cada vehículo en el convoy lleva una fracción y el costo se aplica por fracción.
        # Aquí, lo más simple es aplicar costo_kg al peso_carga total, ya que la tarifa por kg es fija para el vehículo.
        # PERO: si el costo por kg VARÍA según la carga del VEHÍCULO INDIVIDUAL, esta lógica cambia.
        # Revisando Vehiculos.pdf: Automotor tiene costo por kg VARIABLE según carga (>15000kg).
        # Esto significa que el costo por Kg se calcula por *cada vehículo individualmente*.
        # Por lo tanto, necesitamos pasar el peso_carga_por_vehiculo a las subclases.

        # Delegamos a un método auxiliar que cada subclase sobrescribirá
        return self._calcular_costo_tramo_unitario_con_multiplicador(distancia_km, peso_carga, num_vehiculos, tipo_restriccion_tramo, valor_restriccion_tramo)

    def _calcular_costo_tramo_unitario_con_multiplicador(self, distancia_km: float, peso_carga: float, num_vehiculos: int, tipo_restriccion_tramo: str, valor_restriccion_tramo: float) -> float:
        # Método auxiliar que las subclases sobrescribirán para su lógica de costo variable.
        # Aquí, en la clase base, es simplemente la suma de los costos base multiplicados por el número de vehículos.
        costo_fijo_total = self.costoFijo * num_vehiculos
        costo_km_total = self.costoKm * distancia_km * num_vehiculos
        # El costo por Kg es más complejo si las tarifas son por vehículo individual.
        # Para la clase base, simplemente lo aplicamos al peso_carga dividido entre los vehículos (promedio)
        # o al peso_carga total si el costo por kg no es variable por vehículo.
        # Dada la variabilidad (ej: Automotor), es mejor que cada subclase maneje su costo por Kg.
        # Por ahora, dejemos el base simple.
        costo_kg_total = self.costoKg * peso_carga # Esto es si el costo por Kg es por la carga TOTAL
        
        return costo_fijo_total + costo_km_total + costo_kg_total


    def calcular_tiempo_tramo(self, distancia_km: float, peso_carga: float, tipo_restriccion_tramo: str = None, valor_restriccion_tramo: float = None) -> float:
        """
        Calcula el tiempo total de un tramo, considerando múltiples vehículos si es necesario.
        El tiempo de un tramo no debería variar con el número de vehículos, solo con la velocidad del vehículo.
        """
        if self.velocidad == 0:
            return float('inf') # Evitar división por cero
        
        # El tiempo es el tiempo de UN vehículo, el número de vehículos no afecta el tiempo de TRANSITO.
        # Delegamos a un método auxiliar que cada subclase sobrescribirá
        return self._calcular_tiempo_tramo_unitario(distancia_km, tipo_restriccion_tramo, valor_restriccion_tramo)
    
    def _calcular_tiempo_tramo_unitario(self, distancia_km: float, tipo_restriccion_tramo: str, valor_restriccion_tramo: float) -> float:
        # En la clase base, es simple distancia / velocidad
        return distancia_km / self.velocidad


# --- Subclases de Vehiculos ---

class Ferroviario(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=100, carga=150000, costoFijo=100, costoKm=20, costoKg=3)

    def calcular_costo_tramo(self, distancia_km: float, peso_carga: float, tipo_restriccion_tramo: str = None, valor_restriccion_tramo: float = None) -> float:
        num_vehiculos = self.calcular_vehiculos_necesarios(peso_carga)
        if num_vehiculos == 0:
            return 0.0
        
        costo_km_variable = 20 if distancia_km < 200 else 15
        
        # El costo fijo se multiplica por el número de vehículos
        costo_fijo_total = self.costoFijo * num_vehiculos
        # El costo por KM se multiplica por el número de vehículos
        costo_km_total = costo_km_variable * distancia_km * num_vehiculos
        # El costo por KG se aplica al peso total de la carga (no por vehículo individual)
        costo_kg_total = self.costoKg * peso_carga 
        
        return costo_fijo_total + costo_km_total + costo_kg_total

    # No se menciona variación de tiempo para ferroviario, así que la base está bien.


class Aereo(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=600, carga=5000, costoFijo=750, costoKm=40, costoKg=10)

    def calcular_tiempo_tramo(self, distancia_km: float, peso_carga: float, tipo_restriccion_tramo: str = None, valor_restriccion_tramo: float = None) -> float:
        # No depende del número de vehículos, solo de la velocidad.
        velocidad_real = self.velocidad
        if tipo_restriccion_tramo == "Clima" and valor_restriccion_tramo == 1: 
            velocidad_real = 400
        if velocidad_real == 0:
            return float('inf')
        return distancia_km / velocidad_real

    # No se menciona variación de costo para aereo, así que la base está bien.


class Automotor(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=80, carga=30000, costoFijo=30, costoKm=5, costoKg=1)

    def calcular_costo_tramo(self, distancia_km: float, peso_carga: float, tipo_restriccion_tramo: str = None, valor_restriccion_tramo: float = None) -> float:
        num_vehiculos = self.calcular_vehiculos_necesarios(peso_carga)
        if num_vehiculos == 0:
            return 0.0

        costo_fijo_total = self.costoFijo * num_vehiculos
        costo_km_total = self.costoKm * distancia_km * num_vehiculos

        # El costo por Kg VARÍA según la carga del vehículo INDIVIDUAL
        # Distribuimos la carga entre los vehículos de la forma "más equitativa"
        # Esto es una simplificación; en la realidad sería más complejo.
        carga_por_vehiculo_promedio = peso_carga / num_vehiculos
        costo_kg_por_vehiculo = 1 if carga_por_vehiculo_promedio < 15000 else 2
        costo_kg_total = costo_kg_por_vehiculo * peso_carga # Se multiplica por peso_carga total, no por la de un vehículo.

        return costo_fijo_total + costo_km_total + costo_kg_total


class Maritimo(Vehiculos):
    def __init__(self):
        super().__init__(velocidad=40, carga=100000, costoFijo=500, costoKm=15, costoKg=2)

    def calcular_costo_tramo(self, distancia_km: float, peso_carga: float, tipo_restriccion_tramo: str = None, valor_restriccion_tramo: float = None) -> float:
        num_vehiculos = self.calcular_vehiculos_necesarios(peso_carga)
        if num_vehiculos == 0:
            return 0.0
        
        costo_fijo_unitario = self.costoFijo # Default a fluvial (500)
        if tipo_restriccion_tramo == "Tasa" and valor_restriccion_tramo == 1500:
             costo_fijo_unitario = 1500 # Tasa marítima
        elif tipo_restriccion_tramo == "Tasa" and valor_restriccion_tramo == 500:
            costo_fijo_unitario = 500 # Tasa fluvial explícita
            
        costo_fijo_total = costo_fijo_unitario * num_vehiculos
        costo_km_total = self.costoKm * distancia_km * num_vehiculos
        costo_kg_total = self.costoKg * peso_carga 
        
        return costo_fijo_total + costo_km_total + costo_kg_total



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