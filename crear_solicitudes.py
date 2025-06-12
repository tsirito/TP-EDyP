
from leer_archivos import Archivos
from solicitudes import Solicitud # Asegúrate de que solicitudes.py existe y contenga la clase Solicitud

class CreadorDeSolicitudes:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_solicitudes(self) -> list[Solicitud]:
        lineas_solicitudes = self.archivos.leer_archivo()
        solicitudes = []
        for fila in lineas_solicitudes:
            if not fila or len(fila) < 4: # Ignorar filas vacías o incompletas
                continue
            try:
                id_carga = fila[0]
                peso = float(fila[1])
                origen = fila[2]
                destino = fila[3]
                solicitudes.append(Solicitud(id_carga, peso, origen, destino))
            except (ValueError, IndexError) as e:
                print(f"Error: No se pudo leer la fila de solicitud '{fila}'. Asegúrate que el formato sea 'id,peso,origen,destino'. Error: {e}")
        return solicitudes