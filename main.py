"""Aca vamos a ir armando el codigo"""
from crear_tramos import CreadorDeTramos
from Ciudades import CreadordeCiudades
from crear_solicitudes import CreadorDeSolicitudes
from Nodos import RedNodos
from Nodos import NodoCiudad
from caminos import mostrar_caminos
from Vehiculos import *

def main():
    #Ciudades
    creador_ciudades = CreadordeCiudades("nodos.csv")
    ciudades_creadas = creador_ciudades.crear_ciudades()
    
    #Tramos
    creador_tramos = CreadorDeTramos("conexiones.csv",ciudades_creadas) 
    tramos_creados = creador_tramos.crear_tramos()

    #print(type(tramos_creados[0].origen))
    #print(tramos_creados[0].origen)
    
    #Instanciar la red de nodos
    #Instanciar cada nodo

    # for tramo in tramos_creados:
    #     print(f"Tramo: {tramo.origen} a {tramo.destino}, Tipo: {tramo.tipo}, Distancia: {tramo.distancia_km} km")
    #     if tramo.restriccion:
    #         print(f"  Restricción: {tramo.restriccion}, Valor: {tramo.valor_restriccion}")

    tramos_ferroviarios = list(filter(lambda t: t.tipo == "Ferroviaria", tramos_creados))
    tramos_automotores = list(filter(lambda t: t.tipo == "Automotor", tramos_creados))
    tramos_aereos = list(filter(lambda t: t.tipo == "Aerea", tramos_creados))
    tramos_fluviales = list(filter(lambda t: t.tipo == "Fluvial", tramos_creados))

    red_ferroviaria = RedNodos(ciudades_creadas, tramos_ferroviarios)
    red_automotor = RedNodos(ciudades_creadas, tramos_automotores)
    red_aerea = RedNodos(ciudades_creadas, tramos_aereos)
    red_fluvial = RedNodos(ciudades_creadas, tramos_fluviales)

    # print("\n Red Ferroviaria:")
    # for nombre, nodo in red_ferroviaria.nodos_totales.items():
    #     print(f"Ciudad: {nombre}, tiene {len(nodo.destinos)} destinos ferroviarios")

    # print("\n Red Automotor:")
    # for nombre, nodo in red_automotor.nodos_totales.items():
    #     print(f"Ciudad: {nombre}, tiene {len(nodo.destinos)} destinos automotores")

    # print("\n Red Aérea:")
    # for nombre, nodo in red_aerea.nodos_totales.items():
    #     print(f"Ciudad: {nombre}, tiene {len(nodo.destinos)} destinos aéreos")

    # print("\n Red Fluvial:")
    # for nombre, nodo in red_fluvial.nodos_totales.items():
    #     print(f"Ciudad: {nombre}, tiene {len(nodo.destinos)} destinos fluviales")
    
    #red = RedNodos(ciudades_creadas, tramos_creados)

    #for nombre, nodo in red.nodos_totales.items():
        #print(f"Ciudad: {nombre}, tiene {len(nodo.destinos)} destinos posibles")
    
    vehiculo_ferroviario = Ferroviario()
    vehiculo_automotor = Automotor()
    vehiculo_aereo = Aereo()
    vehiculo_maritimo = Maritimo()

    #Solicitudes
    creador_solicitudes = CreadorDeSolicitudes("solicitudes.csv")
    solicitudes = creador_solicitudes.crear_solicitudes()

    for solicitud in solicitudes:
        print(f"\n Procesando solicitud {solicitud.id_carga} ({solicitud.peso} kg) de {solicitud.origen} a {solicitud.destino}:\n")

        caminos_ferro = mostrar_caminos(solicitud.origen, solicitud.destino, red_ferroviaria, "Ferroviaria", vehiculo_ferroviario, solicitud.peso)
        caminos_auto = mostrar_caminos(solicitud.origen, solicitud.destino, red_automotor, "Automotor", vehiculo_automotor, solicitud.peso)
        caminos_aereo = mostrar_caminos(solicitud.origen, solicitud.destino, red_aerea, "Aérea", vehiculo_aereo, solicitud.peso)
        caminos_fluvial = mostrar_caminos(solicitud.origen, solicitud.destino, red_fluvial, "Fluvial", vehiculo_maritimo, solicitud.peso)

    todos_los_caminos = []
    if caminos_ferro: todos_los_caminos += caminos_ferro
    if caminos_auto: todos_los_caminos += caminos_auto
    if caminos_aereo: todos_los_caminos += caminos_aereo
    if caminos_fluvial: todos_los_caminos += caminos_fluvial

    if not todos_los_caminos:
        print("   ❌ No hay caminos viables en ninguna red.")

    mejor_costo = min(todos_los_caminos, key=lambda x: x["costo"])
    mejor_tiempo = min(todos_los_caminos, key=lambda x: x["tiempo"])

    print("\n Resumen consolidado:")
    print(f"    Más barato: {mejor_costo['ruta']} en red {mejor_costo['red']} (${mejor_costo['costo']:.2f})")
    print(f"    Más rápido: {mejor_tiempo['ruta']} en red {mejor_tiempo['red']} ({mejor_tiempo['tiempo']:.2f} hs)")

main()