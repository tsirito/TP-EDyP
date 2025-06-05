# crear_tramos.py
from leer_archivos import Archivos
from Tramos import TramoAereo, TramoAutomor, TramoMaritimo, TramoFerroviario

class CreadorDeTramos:
    def __init__(self, archivo_conexiones_csv: str):
        self.archivo_conexiones_csv = archivo_conexiones_csv

    def crear_tramos(self):
        """
        Lee el archivo CSV de conexiones y crea instancias de las clases
        de tramo correspondientes.
        """
        lector_archivos = Archivos(self.archivo_conexiones_csv)
        datos_conexiones = lector_archivos.leer_archivo()

        tramos = []
        for fila in datos_conexiones:
            # Asumiendo el orden de las columnas en el CSV:
            # Origen, Destino, Tipo_Transporte, Distancia_Km, Tipo_Restriccion, Valor_Restriccion
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