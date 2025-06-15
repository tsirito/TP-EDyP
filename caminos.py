
from nodos import Nodo, RedNodos 
from crear_tramos import Tramo

def buscar_caminos(nodo_actual: Nodo, destino, red, camino_actual, caminos_visitados):
    if nodo_actual.ciudad.nombre == destino:
        caminos_visitados.append(list(camino_actual))
        return

    for tramo in nodo_actual.destinos:
        ciudad_vecina = tramo.destino  # es un string
        if ciudad_vecina not in [t.origen for t in camino_actual]:  # evitar ciclos
            siguiente_nodo = red.nodos_totales.get(ciudad_vecina)
            if siguiente_nodo:
                camino_actual.append(tramo)
                buscar_caminos(siguiente_nodo, destino, red, camino_actual, caminos_visitados)
                camino_actual.pop()

def mostrar_caminos(origen, destino, red, nombre_red):
    nodo_origen = red.nodos_totales.get(origen)
    if not nodo_origen:
        print(f"No se encontró el nodo de origen '{origen}' en la red {nombre_red}")
        return

    caminos = []
    buscar_caminos(nodo_origen, destino, red, [], caminos)

    print(f"\n Caminos posibles en red {nombre_red} de {origen} a {destino}:")
    
    if not caminos:
        print("   No hay caminos.")
    
    for i, camino in enumerate(caminos, 1):
        ruta = " -> ".join([tramo.origen for tramo in camino] + [camino[-1].destino])
        distancia_total = sum(t.distancia_km for t in camino)
        
        print(f"  {i}) {ruta}")
        print(f"     Distancia total: {distancia_total} km")

        restricciones = []
        for tramo in camino:
            if tramo.restriccion:
                restricciones.append((tramo.restriccion, tramo.valor_restriccion))
        
        if restricciones:
            print(f"     Restricciones del camino:")
            for restr, val in restricciones:
                print(f"       - {restr}: {val}")
        else:
            print("     Sin restricciones.")