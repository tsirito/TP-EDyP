"""Aca vamos a ir armando el codigo"""
from crear_tramos import CreadorDeTramos
from ciudades import CreadordeCiudades, Ciudad
from crear_solicitudes import CreadorDeSolicitudes
from Nodos import RedNodos
from Nodos import NodoCiudad
from Vehiculos import *
from graficos import graficar_itinerario




def main():
    """
    Función principal que se usa para la creación de ciudades, tramos, redes de transporte y solicitudes de envío.

    Hace lo siguiente:
    - Lee las ciudades desde un archivo y las instancia.
    - Lee los tramos y los separa por tipo de transporte.
    - Crea una red distinta por tipo de transporte (ferroviaria, automotor, aérea y fluvial).
    - Instancia los distintos tipos de vehículos.
    - Procesa solicitudes de transporte, muestra los caminos posibles por red,
      y elige el camino más barato y el más rápido para cada red, y luego para toda la solicitud en gral.
    """
    #Ciudades
    creador_ciudades = CreadordeCiudades("nodos.csv")
    ciudades_creadas = creador_ciudades.crear_ciudades()
    
    #Tramos
    creador_tramos = CreadorDeTramos("conexiones.csv",ciudades_creadas) 
    tramos_creados = creador_tramos.crear_tramos()

    tramos_ferroviarios = list(filter(lambda t: t.tipo == "Ferroviaria", tramos_creados))
    tramos_automotores = list(filter(lambda t: t.tipo == "Automotor", tramos_creados))
    tramos_aereos = list(filter(lambda t: t.tipo == "Aerea", tramos_creados))
    tramos_fluviales = list(filter(lambda t: t.tipo == "Fluvial", tramos_creados))

    red_ferroviaria = RedNodos(ciudades_creadas, tramos_ferroviarios)
    red_automotor = RedNodos(ciudades_creadas, tramos_automotores)
    red_aerea = RedNodos(ciudades_creadas, tramos_aereos)
    red_fluvial = RedNodos(ciudades_creadas, tramos_fluviales)

    vehiculo_ferroviario = Ferroviario()
    vehiculo_automotor = Automotor()
    vehiculo_aereo = Aereo()
    vehiculo_maritimo = Maritimo()

    #Solicitudes
    creador_solicitudes = CreadorDeSolicitudes("muchas_solicitudes.csv")
    solicitudes = creador_solicitudes.crear_solicitudes()

    for solicitud in solicitudes:
        print(f"\n Solicitud: {solicitud.id_carga} ({solicitud.peso} kg) de {solicitud.origen} a {solicitud.destino}:\n")

        caminos_ferro = red_ferroviaria.mostrar_caminos(solicitud.origen, solicitud.destino,  "Ferroviaria", vehiculo_ferroviario, solicitud.peso)
        caminos_auto = red_automotor.mostrar_caminos(solicitud.origen, solicitud.destino, "Automotor", vehiculo_automotor, solicitud.peso)
        caminos_aereo = red_aerea.mostrar_caminos(solicitud.origen, solicitud.destino, "Aérea", vehiculo_aereo, solicitud.peso)
        caminos_fluvial = red_fluvial.mostrar_caminos(solicitud.origen, solicitud.destino, "Fluvial", vehiculo_maritimo, solicitud.peso)

        todos_los_caminos = []
        if caminos_ferro: todos_los_caminos += caminos_ferro
        if caminos_auto: todos_los_caminos += caminos_auto
        if caminos_aereo: todos_los_caminos += caminos_aereo
        if caminos_fluvial: todos_los_caminos += caminos_fluvial

        if not todos_los_caminos:
            print("   No hay caminos viables en ninguna red.")
            continue  # Pasa a la siguiente solicitud

        mejor_costo = min(todos_los_caminos, key=lambda x: x["costo"])
        mejor_tiempo = min(todos_los_caminos, key=lambda x: x["tiempo"])

        print("\n Resumen consolidado:")
        print(f"    Más barato: {mejor_costo['ruta']} en red {mejor_costo['red']} (${mejor_costo['costo']:.2f})")
        print(f"    Más rápido: {mejor_tiempo['ruta']} en red {mejor_tiempo['red']} ({mejor_tiempo['tiempo']:.2f} hs)")
        
        
        # Elegir el camino más barato (ya lo tenés en mejor_costo)
        camino_a_graficar = mejor_costo["camino"]  # lista de tramos
        red_caminos = mejor_costo["red"]

        # Elegir el vehículo según la red
        if red_caminos == "Ferroviaria":
            vehiculo = vehiculo_ferroviario
        elif red_caminos == "Automotor":
            vehiculo = vehiculo_automotor
        elif red_caminos == "Aérea":
            vehiculo = vehiculo_aereo
        elif red_caminos == "Fluvial":
            vehiculo = vehiculo_maritimo
        else:
            vehiculo = None  # o lanzá un error

        # Peso de la solicitud
        peso = solicitud.peso

        # Llamar a la función para graficar
        graficar_itinerario(camino_a_graficar, vehiculo, peso)
            

main()



