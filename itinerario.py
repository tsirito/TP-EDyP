# itinerario.py
import math
from crear_tramos import Tramo, TramoMaritimo, TramoAereo # Importa las subclases de Tramo si las usas para type hinting o lógica específica
from crear_solicitudes import Solicitud
from Vehiculos import Vehiculo, Ferroviario, Automotor, Maritimo, Aereo # Importa todas las subclases de Vehiculo

class Itinerario:
    def __init__(self, camino: list[Tramo], solicitud: Solicitud, tipo_vehiculo_str: str):
        self.camino = camino
        self.solicitud = solicitud
        self.tipo_vehiculo_str = tipo_vehiculo_str
        
        # Instanciar el objeto Vehiculo concreto
        self.vehiculo = self._instanciar_vehiculo() 

        self.distancia_total_km = 0
        self.tiempo_total_horas = 0
        self.costo_total_pesos = 0
        self.cantidad_vehiculos_necesarios = 1 

        self._calcular_totales()

    def _instanciar_vehiculo(self) -> Vehiculo:
        # Crea una instancia del vehículo correcto
        if self.tipo_vehiculo_str == "Ferroviaria":
            return Ferroviario()
        elif self.tipo_vehiculo_str == "Automotor":
            return Automotor()
        elif self.tipo_vehiculo_str == "Aerea":
            return Aereo()
        elif self.tipo_vehiculo_str == "Fluvial": # Usar el mismo string que en tramos
            return Maritimo()
        else:
            raise ValueError(f"Tipo de vehículo desconocido: {self.tipo_vehiculo_str}")

    def _calcular_totales(self):
        self.distancia_total_km = sum(tramo.distancia_km for tramo in self.camino)

        # Cantidad de vehículos necesarios
        if self.solicitud.peso > 0 and self.vehiculo.carga > 0: # Evitar divisiones por cero o negativas
            self.cantidad_vehiculos_necesarios = math.ceil(self.solicitud.peso / self.vehiculo.carga)
        else:
            self.cantidad_vehiculos_necesarios = 1 # Si la carga es 0 o el vehículo no tiene capacidad, 1 vehículo.

        tiempo_acumulado = 0
        costo_acumulado = 0

        for tramo in self.camino:
            # Calcular tiempo del tramo
            velocidad_efectiva = tramo.aplicar_restriccion_tiempo(self.vehiculo.velocidad)
            tiempo_acumulado += self.vehiculo.calcular_tiempo_tramo(tramo.distancia_km, velocidad_efectiva)

            # Calcular costos por kilómetro y fijos del tramo
            # Cada vehículo sabe cómo calcular su costo por Km según el tramo.
            costo_acumulado += self.vehiculo.calcular_costo_km_tramo(tramo.distancia_km) * self.cantidad_vehiculos_necesarios
            
            # El costo fijo de Marítimo depende de la restricción del tramo
            if isinstance(self.vehiculo, Maritimo):
                costo_acumulado += self.vehiculo.calcular_costo_fijo_tramo(tramo.restriccion) * self.cantidad_vehiculos_necesarios
            else:
                costo_acumulado += self.vehiculo.calcular_costo_fijo_tramo() * self.cantidad_vehiculos_necesarios
        
        self.tiempo_total_horas = tiempo_acumulado
        
        # Costo por Kg se calcula una vez al final, por la carga total de la solicitud
        costo_acumulado += self.vehiculo.calcular_costo_kg_total(self.solicitud.peso) * self.cantidad_vehiculos_necesarios
        self.costo_total_pesos = costo_acumulado

    def __repr__(self):
        return (f"Itinerario(Tipo={self.tipo_vehiculo_str}, Distancia={self.distancia_total_km:.2f} Km, "
                f"Tiempo={self.tiempo_total_horas:.2f} hs, Costo=${self.costo_total_pesos:.2f}, "
                f"Vehiculos={self.cantidad_vehiculos_necesarios}, "
                f"Ruta: {self.get_ruta_str()})")

    # Métodos para acceder a los resultados
    def get_tiempo_total(self):
        return self.tiempo_total_horas

    def get_costo_total(self):
        return self.costo_total_pesos

    def get_vehiculo_tipo(self):
        return self.tipo_vehiculo_str

    def get_cantidad_vehiculos(self):
        return self.cantidad_vehiculos_necesarios

    def get_ruta_str(self):
        if self.camino:
            return " -> ".join([t.origen for t in self.camino] + [self.camino[-1].destino])
        return "N/A"