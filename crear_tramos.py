from leer_archivos import Archivos
from Tramos import TramoAereo, TramoAutomor, TramoMaritimo, TramoFerroviario
from Validaciones import Validaciones

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