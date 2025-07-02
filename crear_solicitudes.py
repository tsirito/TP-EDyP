from leer_archivos import Archivos
from Validaciones import Validaciones
from Vehiculos import *
from nodos import MainRedes
from graficos import Graficar

class MainSolicitudes:
    
    vehiculo_ferroviario = Ferroviario()
    vehiculo_automotor = Automotor()
    vehiculo_aereo = Aereo()
    vehiculo_maritimo = Maritimo()
    
    def crear_solicitudes(archivo):
        creador_solicitudes = CreadorDeSolicitudes(archivo)
        solicitudes = creador_solicitudes.crear_solicitudes()
        return solicitudes
    
    def procesar_solicitudes(solicitudes):
       

        for solicitud in solicitudes:
            print(f"\n Solicitud: {solicitud.id_carga} ({solicitud.peso} kg) de {solicitud.origen} a {solicitud.destino}:\n")

            caminos_ferro = MainRedes.red_ferroviaria.mostrar_caminos(solicitud.origen, solicitud.destino, "Ferroviaria", MainSolicitudes.vehiculo_ferroviario, solicitud.peso)
            caminos_auto = MainRedes.red_automotor.mostrar_caminos(solicitud.origen, solicitud.destino, "Automotor", MainSolicitudes.vehiculo_automotor, solicitud.peso)
            caminos_aereo = MainRedes.red_aerea.mostrar_caminos(solicitud.origen, solicitud.destino, "Aérea", MainSolicitudes.vehiculo_aereo, solicitud.peso)
            caminos_fluvial = MainRedes.red_fluvial.mostrar_caminos(solicitud.origen, solicitud.destino, "Fluvial", MainSolicitudes.vehiculo_maritimo, solicitud.peso)

            todos_los_caminos = []
            if caminos_ferro: todos_los_caminos += caminos_ferro
            if caminos_auto: todos_los_caminos += caminos_auto
            if caminos_aereo: todos_los_caminos += caminos_aereo
            if caminos_fluvial: todos_los_caminos += caminos_fluvial

            if not todos_los_caminos:
                print("   No hay caminos viables en ninguna red.")
                continue

            mejor_costo = min(todos_los_caminos, key=lambda x: x["costo"])
            mejor_tiempo = min(todos_los_caminos, key=lambda x: x["tiempo"])

            print("\n Resumen entre las redes:")
            print(f"    Más barato: {mejor_costo['ruta']} en red {mejor_costo['red']} (${mejor_costo['costo']:.2f})")
            print(f"    Más rápido: {mejor_tiempo['ruta']} en red {mejor_tiempo['red']} ({mejor_tiempo['tiempo']:.2f} hs)")

            MainSolicitudes.graficar(mejor_costo, solicitud.peso)
            
    def graficar(mejor_costo, peso):
                camino_barato = mejor_costo["camino"]
                red_barato = mejor_costo["red"]
                vehiculo_barato = {
                "Ferroviaria": MainSolicitudes.vehiculo_ferroviario,
                "Automotor": MainSolicitudes.vehiculo_automotor,
                "Aérea": MainSolicitudes.vehiculo_aereo,
                "Fluvial": MainSolicitudes.vehiculo_maritimo
                }.get(red_barato)

                print("\nA continuacion se muestran los graficos del camino mas barato para cada solitud:")
                Graficar.graficar_itinerario(camino_barato, vehiculo_barato, peso)

class Solicitud():
    """
    Crea una instancia de una solicitud de carga
    """
    def __init__(self, id_carga, peso, origen, destino):
        '''
        inicializa una instancia de la solicitud
        '''
        self.id_carga = id_carga
        self.peso = peso
        self.origen = origen
        self.destino = destino
    

class CreadorDeSolicitudes:
    '''
    Clase encargada de leer las solicitudes y crear las instancias de la clase Solicitud y devuelve una lista de las solicitudes
    '''
    def __init__(self, nombre_archivo):
        """
        Guarda el nombre del archivo donde se van a crear las solicitudes
        """
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)
    

    def crear_solicitudes(self) -> list[Solicitud]:
        """
        Lee las solicitudes y genera una lista con las solicitudes validas
        """
        lineas_solicitudes = self.archivos.leer_archivo()
        solicitudes = []
        for fila in lineas_solicitudes:
            if not fila or len(fila) < 4: # Ignorar filas vacías o incompletas
                continue
            try:
                id_carga = fila[0]
                peso = Validaciones.validar_valor_positivo(fila[1], 'peso')
                origen = Validaciones.validarCiudad(fila[2])
                destino = Validaciones.validarCiudad(fila[3])
                solicitudes.append(Solicitud(id_carga, peso, origen, destino))
            except (ValueError, IndexError) as e:
                print(f"Error: No se pudo leer la fila de solicitud '{fila}'. Asegúrate que el formato sea 'id,peso,origen,destino'. Error: {e}")
        return solicitudes
    
    

