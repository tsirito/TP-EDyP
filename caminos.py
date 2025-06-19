<<<<<<< HEAD
from Nodos import NodoCiudad, RedNodos 
=======

from nodos import NodoCiudad, RedNodos 
>>>>>>> e6eef559f5d8d50630278696ce687cfe4fedb1e3
from crear_tramos import Tramo
import random

def buscar_caminos(nodo_actual: NodoCiudad, destino, red, camino_actual, caminos_visitados):
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
        print(f"No se encontró el nodo de origen '{origen}' en la red {nombre_red}")  #VALIDACION
        return

    caminos = []
    buscar_caminos(nodo_origen, destino, red, [], caminos)

    print(f"\n Caminos posibles en red {nombre_red} de {origen} a {destino}:")

    if not caminos:
        print("No hay caminos.")
        return
    
    caminos_validos = []

    for i, camino in enumerate(caminos, 1):  #  
        ruta = " -> ".join([tramo.origen for tramo in camino] + [camino[-1].destino])
        distancia_total = sum(t.distancia_km for t in camino)

        restricciones = []
        tiempo_horas = 0
        costo_total=0

        # Cálculo del tiempo y costo

        vehiculos_necesarios = int((peso + vehiculo.carga - 1) // vehiculo.carga)  # redondeo hacia arriba"" con el -1

        camino_invalido = False

        for tramo in camino:
            costoFijo= vehiculo.costoFijo
            costo_por_km= vehiculo.costoKm
            costo_kg= vehiculo.costoKg
            mal_tiempo = False

            if tramo.restriccion:
                restricciones.append((tramo.restriccion, tramo.valor_restriccion))
            
            velocidad_tramo = vehiculo.velocidad  # por defecto
            
            if tramo.tipo == "Aerea" and tramo.restriccion == "prob_mal_tiempo":
                probabilidad = tramo.valor_restriccion
                if random.random() < probabilidad:
                    mal_tiempo = True
                    velocidad_tramo = 400
                else:
                    velocidad_tramo = vehiculo.velocidad
            else:
                # Si no es aéreo, usar la velocidad normal o restringida
                if tramo.restriccion == "velocidad_max" and tramo.valor_restriccion:
                    velocidad_tramo = min(tramo.valor_restriccion, vehiculo.velocidad)
                
                if tramo.restriccion == "tipo" and tramo.valor_restriccion=="fluvial":
                    costoFijo= 500
                    
                if tramo.restriccion == "tipo" and tramo.valor_restriccion=="maritimo":
                    costoFijo= 1500

            if tramo.restriccion == "peso_max" and peso/vehiculos_necesarios > tramo.valor_restriccion:
                camino_invalido = True            
            
            tiempo_horas += tramo.distancia_km / velocidad_tramo            

            if mal_tiempo:
                print(f"    Este tramo tuvo mal tiempo en algún tramo aéreo. Velocidad reducida.")
                restricciones.append((tramo.restriccion, tramo.valor_restriccion))
            
            if nombre_red == "Ferroviaria" and  tramo.distancia_km >= 200:
                costo_por_km = 15


            #peso % capacidad = autos llenos
            #peso - (Capacidad * autos llenos)= restante en kg
            #si restante >15000, costo =2, sino costo =1
            costo_total += (costoFijo * vehiculos_necesarios + costo_por_km * tramo.distancia_km * vehiculos_necesarios)
            
        if nombre_red == "Automotor":
            autos_llenos= peso//vehiculo.carga  
            if autos_llenos>=1:
                costo_total+= autos_llenos*2*vehiculo.carga 
                restante= peso - (vehiculo.carga*autos_llenos)
                if restante <15000:
                    costo_total += restante
                else:
                    costo_total+= 2*restante
            else:
                costo_total+= 1* peso


        else:
            costo_total+= costo_kg * peso
        
            # A REVISAR:
            #
            # costo_total += (
            # vehiculo.costoFijo * vehiculos_necesarios +
            # vehiculo.costoKm * tramo.distancia * vehiculos_necesarios +
            # vehiculo.costoKg * peso)

        if camino_invalido:
            print(f"  {i}) {ruta}")
            print("   Este camino no es válido para esta carga porque excede el peso máximo permitido.")
            continue

        caminos_validos.append({
            "indice": i,
            "ruta": ruta,
            "distancia": distancia_total,
            "tiempo": tiempo_horas,
            "costo": costo_total,
            "vehiculos": vehiculos_necesarios,
            "restricciones": restricciones,
            "red": nombre_red

        })
        """
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
        """
    if not caminos_validos: 
        print("    No hay caminos viables para esta solicitud.")
        return

    # Buscar el más barato y el más rápido
    camino_mas_barato = min(caminos_validos, key=lambda x: x["costo"])
    camino_mas_rapido = min(caminos_validos, key=lambda x: x["tiempo"])
    
    for camino in caminos_validos:
        caso = ""
        if camino["costo"] == camino_mas_barato["costo"] and camino["tiempo"] == camino_mas_rapido["tiempo"]:
            caso = "|| Más barato y más rápido de esta red"
        elif camino["costo"] == camino_mas_barato["costo"]:
            caso = "|| Más barato de esta red"
        elif camino["tiempo"] == camino_mas_rapido["tiempo"]:
            caso = "|| Más rápido de esta red"

        print(f"  {camino['indice']}) {camino['ruta']} {caso}")
        print(f"     Distancia total: {camino['distancia']:.2f} km")
        
        if camino['restricciones']:
            print("     Restricciones:")
            for restr, val in camino['restricciones']:
                print(f"       - {restr}: {val}")
        else:
            print("     Sin restricciones.")
        print(f"     Tiempo estimado: {camino['tiempo']:.2f} horas")
        print(f"     Vehículos necesarios: {camino['vehiculos']}")
        print(f"     Costo total estimado: ${camino['costo']:.2f}")
    
    return caminos_validos