from leer_archivos import Archivos
from Validaciones import Validaciones

class Solicitud():
    
    def __init__(self, id_carga, peso, origen, destino):
        self.id_carga = id_carga
        self.peso = peso
        self.origen = origen
        self.destino = destino
    """Crea una instancia de una solicitud de carga"""

class CreadorDeSolicitudes:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)
    """Guarda el nombre del archivo donde se van a crear las solicitudes"""

    def crear_solicitudes(self) -> list[Solicitud]:
        lineas_solicitudes = self.archivos.leer_archivo()
        solicitudes = []
        for fila in lineas_solicitudes:
            if not fila or len(fila) < 4: # Ignorar filas vacías o incompletas
                continue
            try:
                id_carga = fila[0]
                peso = float(fila[1])
                origen = Validaciones.validarCiudad(fila[2])
                destino = Validaciones.validarCiudad(fila[3])
                solicitudes.append(Solicitud(id_carga, peso, origen, destino))
            except (ValueError, IndexError) as e:
                print(f"Error: No se pudo leer la fila de solicitud '{fila}'. Asegúrate que el formato sea 'id,peso,origen,destino'. Error: {e}")
        return solicitudes
    
    """Lee las solicitudes y genera una lista con las solicitudes validas"""

