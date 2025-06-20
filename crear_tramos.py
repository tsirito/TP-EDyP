from leer_archivos import Archivos
from Validaciones import Validaciones
from ciudades import Ciudad
from Vehiculos import *

class CreadorDeTramos:
    """
    Clase encargada de crear tramos de transporte entre ciudades a partir de un archivo csv.
    """

    def __init__(self, nombre_archivo, lista_ciudades):
        """
        Inicializa una instancia del creador de tramos.
        """
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_tramos(self):
        """
        Crea objetos de tipo Tramo en base a los datos del archivo y devuelve una lista de tramos creados, según el tipo de transporte.
        """
        lineas_de_tramos = self.archivos.leer_archivo()
        tramos = []
        for fila in lineas_de_tramos:
            try:
                origen = Validaciones.validarCiudad(fila[0])
                destino = Validaciones.validarCiudad(fila[1])
                tipo_transporte = fila[2] 
                distancia_km = Validaciones.validar_valor_positivo(fila[3], 'distancia_km')  
                tipo_restriccion = Validaciones.restriccion_existente(fila[4])  
                valor_restriccion = Validaciones.convertir_a_float(fila[5], fila)

                if tipo_transporte == "Aerea":
                    tramos.append(TramoAereo(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Automotor":
                    tramos.append(TramoAutomotor(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Fluvial":
                    tramos.append(TramoMaritimo(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Ferroviaria":
                    tramos.append(TramoFerroviario(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                else:
                    print(f"Advertencia: Tipo de transporte desconocido '{tipo_transporte}' en la fila: {fila}")
    
            except (ValueError, IndexError) as e:
                print(f"Error procesando la fila de conexión: {fila}. Error: {e}")
        return tramos


# Tramos.py
class Tramo:
    """
    Clase que representa un tramo de transporte entre dos ciudades.
    """

    def __init__(self, origen: str, destino: str, tipo: str, distancia_km: float):
        """
        Inicializa una instancia de Tramo.
        """
        self.origen = origen
        self.destino = destino
        self.tipo = tipo
        self.distancia_km = distancia_km
        self.restriccion = None
        self.valor_restriccion = None

    def __eq__(self, otro):
        """
        Compara dos tramos considerando que el orden del origen y destino no importa si el tipo es el mismo. Devuelve True si los tramos son equivalentes, False en caso contrario.
        """
        if not isinstance(otro, Tramo):
            return NotImplemented

        return (self.origen == otro.origen and self.destino == otro.destino and self.tipo == otro.tipo) or \
               (self.origen == otro.destino and self.destino == otro.origen and self.tipo == otro.tipo)

    def aplicar_restricciones(self, vehiculo, peso, vehiculos_necesarios):
        velocidad = vehiculo.velocidad
        costo_fijo = vehiculo.costoFijo
        costo_km = vehiculo.costoKm
        camino_invalido = False

        if self.restriccion == "velocidad_max" and self.valor_restriccion:
            velocidad = min(self.valor_restriccion, vehiculo.velocidad)

        if self.restriccion == "peso_max":
            peso_por_vehiculo = peso / vehiculos_necesarios
            if peso_por_vehiculo > self.valor_restriccion:
                camino_invalido = True
     

        return velocidad, costo_fijo, costo_km, camino_invalido
    
class TramoAereo(Tramo):
    def __init__(self, origen: str, destino: str, tipo: str, distancia_km: float, restriccion: str = None, valor_restriccion: float = None):
        super().__init__(origen, destino, "Aerea", distancia_km) 
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion
    
class TramoAutomotor(Tramo):
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