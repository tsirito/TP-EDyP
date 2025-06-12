# Itinerarios.py
from Tramos import Tramo,TramoAereo, TramoAutomor, TramoMaritimo, TramoFerroviario
from Vehiculos import  Vehiculos,Ferroviario, Aereo, Automotor, Maritimo
from solicitudes import Solicitud 

class Itinerario:
    def __init__(self, solicitud: Solicitud, tramos_en_ruta: list[Tramo], vehiculo_usado: Vehiculos):
        """
        Representa un posible itinerario para una solicitud dada.
        
        Args:
            solicitud (Solicitud): La solicitud de transporte que este itinerario intenta cumplir.
            tramos_en_ruta (list[Tramo]): Una lista ordenada de objetos Tramo que componen la ruta.
            vehiculo_usado (Vehiculos): El objeto Vehiculo que se usaría para este itinerario.
        """
        self.solicitud = solicitud
        self.tramos_en_ruta = tramos_en_ruta
        self.vehiculo_usado = vehiculo_usado
        self._costo_total = None  # Se calculará bajo demanda
        self._tiempo_total = None # Se calculará bajo demanda

    def calcular_costo_total(self) -> float:
        if self._costo_total is not None:
            return self._costo_total

        total_costo = 0.0
        for tramo in self.tramos_en_ruta:
            total_costo += self.vehiculo_usado.calcular_costo_tramo(
                distancia_km=tramo.distancia_km,
                peso_carga=self.solicitud.peso, # ¡IMPORTANTE! Pasar peso_carga
                tipo_restriccion_tramo=tramo.restriccion,
                valor_restriccion_tramo=tramo.valor_restriccion
            )
        self._costo_total = total_costo
        return total_costo

    def calcular_tiempo_total(self) -> float:
        if self._tiempo_total is not None:
            return self._tiempo_total

        total_tiempo = 0.0
        for tramo in self.tramos_en_ruta:
            total_tiempo += self.vehiculo_usado.calcular_tiempo_tramo(
                distancia_km=tramo.distancia_km,
                peso_carga=self.solicitud.peso, # ¡IMPORTANTE! Pasar peso_carga (incluso si no se usa en tiempo)
                tipo_restriccion_tramo=tramo.restriccion,
                valor_restriccion_tramo=tramo.valor_restriccion
            )
        self._tiempo_total = total_tiempo
        return total_tiempo

    def es_valido(self) -> bool:
        """
        Ahora esta validación ya no verifica directamente la capacidad, 
        sino que la carga no sea negativa y que el cálculo de vehículos
        sea mayor que 0 si la carga es positiva (es decir, que se puedan usar vehículos).
        La lógica de si el vehículo PUEDE llevar la carga está ahora más en el cálculo de costo/tiempo.
        """
        # Un itinerario es válido si la carga no es negativa
        # y si los vehículos necesarios son > 0 si hay carga.
        if self.solicitud.peso < 0:
            return False
        
        # Si la carga es 0, no se necesitan vehículos, es válido.
        if self.solicitud.peso == 0:
            return True

        # Si hay carga, verificar que el tipo de vehículo sea adecuado para transportarla
        # (ej. si la capacidad individual es 0, math.ceil daría error si no se maneja,
        # pero tus vehiculos tienen capacidad > 0.
        # Aquí, simplemente nos aseguramos de que el cálculo del número de vehículos sea válido
        # y que el costo/tiempo no sea infinito si la carga no es cero.
        # Esta función `es_valido` podría ser más compleja, pero por ahora sirve.
        num_vehiculos = self.vehiculo_usado.calcular_vehiculos_necesarios(self.solicitud.peso)
        return num_vehiculos > 0 and self.calcular_costo_total() != float('inf') and self.calcular_tiempo_total() != float('inf')

    def __str__(self):
        tramos_str = " -> ".join([f"{t.origen} a {t.destino} ({t.tipo})" for t in self.tramos_en_ruta])
        # Asegurarse que se haya podido calcular el costo/tiempo antes de mostrarlos
        costo_str = f"${self.calcular_costo_total():.2f}" if self._costo_total is not None else "N/A"
        tiempo_str = f"{self.calcular_tiempo_total():.2f} horas" if self._tiempo_total is not None else "N/A"

        return (f"Itinerario para Solicitud ID {self.solicitud.id_carga} (Peso: {self.solicitud.peso} Kg):\n"
                f"  Ruta: {tramos_str}\n"
                f"  Vehículo: {type(self.vehiculo_usado).__name__}\n"
                f"  Costo Total: {costo_str}\n"
                f"  Tiempo Total: {tiempo_str}")