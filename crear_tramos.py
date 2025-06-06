from leer_archivos import Archivos
from main import *
from Tramos import TramoAereo, TramoAutomor, TramoMaritimo, TramoFerroviario

class CreadorDeTramos:
    def __init__(self, nombre_archivo, lista_ciudades):
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_tramos(self):

        lineas_de_tramos = self.archivos.leer_archivo()
        tramos = []
        for fila in lineas_de_tramos:
            try:
                origen = fila[0]
                destino = fila[1]
                tipo_transporte = fila[2]
                distancia_km = float(fila[3])
                tipo_restriccion = fila[4] if fila[4] else None  # Manejar si no hay restriccion
                valor_restriccion = float(fila[5]) if fila[5] else None # Manejar si no hay restriccion
                
                if tipo_transporte == "Aereo":
                    tramos.append(TramoAereo(origen, destino, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Automotor":
                    tramos.append(TramoAutomor(origen, destino, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Maritimo":
                    tramos.append(TramoMaritimo(origen, destino, distancia_km, tipo_restriccion, valor_restriccion))
                elif tipo_transporte == "Ferroviario":
                    tramos.append(TramoFerroviario(origen, destino, distancia_km, tipo_restriccion, valor_restriccion))
                else:
                    print(f"Advertencia: Tipo de transporte desconocido '{tipo_transporte}' en la fila: {fila}")
            except (ValueError, IndexError) as e:
                print(f"Error procesando la fila de conexión: {fila}. Error: {e}")
        return tramos