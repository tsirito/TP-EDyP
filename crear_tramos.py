from leer_archivos import Archivos
from Validaciones import Validaciones
from ciudades import Ciudad

class CreadorDeTramos:
    def __init__(self, nombre_archivo, lista_ciudades):
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_tramos(self):

        lineas_de_tramos = self.archivos.leer_archivo()
        tramos = []
        for fila in lineas_de_tramos:
            try:
                origen = Validaciones.validarCiudad(fila[0])
                destino = Validaciones.validarCiudad(fila[1])
                tipo_transporte = fila[2]
                distancia_km = float(fila[3])
                tipo_restriccion = fila[4] if fila[4] else None  # Manejar si no hay restriccion
                valor_restriccion = Validaciones.convertir_a_float(fila[5], fila)
                
                if tipo_transporte == "Aerea":
                        tramos.append(TramoAereo(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Automotor":
                        tramos.append(TramoAutomor(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Fluvial":
                        tramos.append(TramoMaritimo(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Ferroviaria":
                        tramos.append(TramoFerroviario(origen, destino, tipo_transporte, distancia_km, tipo_restriccion, valor_restriccion))
                else:
                        print(f"Advertencia: Tipo de transporte desconocido '{tipo_transporte}' en la fila: {fila}")
    
            except (ValueError, IndexError) as e:
                print(f"Error procesando la fila de conexión: {fila}. Error: {e}")
        return tramos
    
# crear_tramos y crear_ciudades devuelven los datos de distinta estructura. Crear tramos devuelva una lista de listas y crear ciudades devuelve una lista de ciudades. Deberia ser lo mismo para los dos (ambas lista de listas o ambas lista de tramos/ciudades)

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