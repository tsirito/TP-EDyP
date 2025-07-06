from leer_archivos import Archivos
from Validaciones import Validaciones
from Vehiculos import *
from nodos import MainRedes
from graficos import *

class MainSolicitudes:
        
    vehiculo_ferroviario = None
    vehiculo_automotor = None
    vehiculo_aereo = None
    vehiculo_maritimo = None

    def inicializar_vehiculos():
        creador = CreadordeVehiculos("vehiculos.csv")
        todos_los_vehiculos= creador.crear_vehiculos()
        MainSolicitudes.vehiculos_por_tipo = todos_los_vehiculos

    def crear_solicitudes(archivo):
        creador_solicitudes = CreadorDeSolicitudes(archivo)
        solicitudes = creador_solicitudes.crear_solicitudes()
        return solicitudes
    
    def procesar_solicitudes(solicitudes):
       
        for solicitud in solicitudes:
            print(f"\n Solicitud: {solicitud.id_carga} ({solicitud.peso} kg) de {solicitud.origen} a {solicitud.destino}:\n")

            caminos_ferro= []
            caminos_auto = []
            caminos_aereo = []
            caminos_fluvial = []

            for tipo, lista in MainSolicitudes.vehiculos_por_tipo.items():
                for vehiculo in lista:
                    if tipo == 'Ferroviario':
                        resultado = MainRedes.red_ferroviaria.mostrar_caminos(
                            solicitud.origen, solicitud.destino, "Ferroviaria", vehiculo, solicitud.peso)
                        if resultado:
                            caminos_ferro += resultado
                    elif tipo == 'Automotor':
                        resultado = MainRedes.red_automotor.mostrar_caminos(
                            solicitud.origen, solicitud.destino, "Automotor", vehiculo, solicitud.peso)
                        if resultado:
                            caminos_auto += resultado
                    elif tipo == 'Aereo':
                        resultado = MainRedes.red_aerea.mostrar_caminos(
                            solicitud.origen, solicitud.destino, "Aérea", vehiculo, solicitud.peso)
                        if resultado:
                            caminos_aereo += resultado
                    elif tipo == 'Maritimo':
                        resultado = MainRedes.red_fluvial.mostrar_caminos(
                            solicitud.origen, solicitud.destino, "Fluvial", vehiculo, solicitud.peso)
                        if resultado:
                            caminos_fluvial += resultado
          
            todos_los_caminos = []
            if caminos_ferro: todos_los_caminos += caminos_ferro
            if caminos_auto: todos_los_caminos += caminos_auto
            if caminos_aereo: todos_los_caminos += caminos_aereo
            if caminos_fluvial: todos_los_caminos += caminos_fluvial

            if not todos_los_caminos:
                print("   No hay caminos viables para esta solicitud.")
                continue

            mejor_costo = min(todos_los_caminos, key=lambda x: x["costo"])
            mejor_tiempo = min(todos_los_caminos, key=lambda x: x["tiempo"])

            print("\n Resumen entre las redes:")
            print(f"    Más barato: {mejor_costo['ruta']} en red {mejor_costo['red']} "
                f"(${mejor_costo['costo']:.2f}) usando vehículo ID {mejor_costo['vehiculo'].id} "
                f"({mejor_costo['vehiculo'].__class__.__name__}, velocidad: {mejor_costo['vehiculo'].velocidad}, Capacidad: {mejor_costo['vehiculo'].carga})")

            print(f"    Más rápido: {mejor_tiempo['ruta']} en red {mejor_tiempo['red']} "
            f"({mejor_tiempo['tiempo']:.2f} hs) usando vehículo ID {mejor_tiempo['vehiculo'].id} "
            f"({mejor_tiempo['vehiculo'].__class__.__name__}, velocidad: {mejor_tiempo['vehiculo'].velocidad}, Capacidad: {mejor_tiempo['vehiculo'].carga})")
            
            MainSolicitudes.graficar(mejor_costo,solicitud.peso)
            
    def graficar(mejor_costo, peso):
                camino_barato = mejor_costo["camino"]
                red_barato = mejor_costo["red"]
                vehiculo_barato = mejor_costo["vehiculo"]

                print("\nA continuacion se muestran los graficos del camino mas barato para esta solicitud: ")
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