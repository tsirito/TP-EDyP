
from Nodos import Nodo, RedNodos 
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

def mostrar_caminos(origen, destino, red, nombre_red, vehiculo, peso):
    nodo_origen = red.nodos_totales.get(origen)
    if not nodo_origen:
        print(f"No se encontró el nodo de origen '{origen}' en la red {nombre_red}")
        return

    caminos = []
    buscar_caminos(nodo_origen, destino, red, [], caminos)

    print(f"\n Caminos posibles en red {nombre_red} de {origen} a {destino}:")

    if not caminos:
        print("   No hay caminos.")
        return

    for i, camino in enumerate(caminos, 1):
        ruta = " -> ".join([tramo.origen for tramo in camino] + [camino[-1].destino])
        distancia_total = sum(t.distancia_km for t in camino)

        restricciones = []
        tiempo_horas = 0

        # Cálculo del tiempo y costo

        vehiculos_necesarios = int((peso + vehiculo.carga - 1) // vehiculo.carga)  # redondeo hacia arriba""

        camino_invalido = False

        for tramo in camino:
            if tramo.restriccion:
                restricciones.append((tramo.restriccion, tramo.valor_restriccion))
            
            velocidad_tramo = vehiculo.velocidad  # por defecto
            
            if tramo.restriccion == "velocidad_max" and tramo.valor_restriccion:
                velocidad_tramo = min(tramo.valor_restriccion, vehiculo.velocidad)
            
            if tramo.restriccion == "peso_max" and peso/vehiculos_necesarios > tramo.valor_restriccion:
                    camino_invalido = True

            tiempo_horas += tramo.distancia_km / velocidad_tramo

        if camino_invalido:
            print(f"  {i}) {ruta}")
            print("   Este camino no es válido para esta carga porque excede el peso máximo permitido.")
            continue

        costo_total = (
            vehiculo.costoFijo * vehiculos_necesarios +
            vehiculo.costoKm * distancia_total * vehiculos_necesarios +
            vehiculo.costoKg * peso
        )

        print(f"  {i}) {ruta}")
        print(f"     Distancia total: {distancia_total:.2f} km")
        if restricciones:
            print("     Restricciones:")
            for restr, val in restricciones:
                print(f"       - {restr}: {val}")
        else:
            print("     Sin restricciones.")
        print(f"     Tiempo estimado: {tiempo_horas:.2f} horas")
        print(f"     Vehículos necesarios: {vehiculos_necesarios}")
        print(f"     Costo total estimado: ${costo_total:.2f}")
