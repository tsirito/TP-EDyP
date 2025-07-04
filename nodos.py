from crear_tramos import *
from Vehiculos import *

class MainRedes:
    
    red_ferroviaria=[]
    red_automotor=[]
    red_aerea=[]
    red_fluvial=[]
    
    def generar_redes(ciudades_creadas):
        MainRedes.red_ferroviaria = RedNodos(ciudades_creadas, MainTramos.tramos_ferroviarios)
        MainRedes.red_automotor = RedNodos(ciudades_creadas, MainTramos.tramos_automotores)
        MainRedes.red_aerea = RedNodos(ciudades_creadas, MainTramos.tramos_aereos)
        MainRedes.red_fluvial = RedNodos(ciudades_creadas, MainTramos.tramos_fluviales)


class NodoCiudad:
    """
    Representa un nodo individual dentro de la red de ciudades.
    """

    def __init__(self, ciudad, destinos):
        """
        Inicializa un nodo con su ciudad asociada y los tramos de destino.
        """
        self.ciudad = ciudad 
        self.destinos = destinos

    def __repr__(self):
        """
        Devuelve una representación formal del nodo, incluyendo la cantidad de destinos.
        """
        return f"Nodo({self.ciudad}, {len(self.destinos)} destinos)"


class RedNodos:
    """
    Representa una red de nodos de ciudades conectadas por tramos.
    """

    @staticmethod
    def crear_nodos(ciudades, tramos):
        """
        Crea un diccionario de nodos a partir de una lista de ciudades y tramos.
        Devuelve un Diccionario donde las claves son nombres de ciudades y los valores son los nodos creados de estas ciudades.
        """
        red = {}
        for ciudad in ciudades:
            destinos_desde_ciudad = []
            #
            for tramo in tramos:
                if tramo.origen == ciudad.nombre:
                    destinos_desde_ciudad.append(tramo)
                if tramo.destino == ciudad.nombre:
                    tipo_tramo_clase = type(tramo)
                    tramo_inverso = tipo_tramo_clase(
                        origen=tramo.destino,
                        destino=tramo.origen,
                        tipo=tramo.tipo, 
                        distancia_km=tramo.distancia_km,
                        restriccion=tramo.restriccion, 
                        valor_restriccion=tramo.valor_restriccion
                    )
                    destinos_desde_ciudad.append(tramo_inverso)
            nodo = NodoCiudad(ciudad, destinos_desde_ciudad)
            red[ciudad.nombre] = nodo
        return red

    def __init__(self, ciudades, tramos):
        """
        Inicializa la red de nodos a partir de ciudades y tramos.
        """
        self.nodos_totales = RedNodos.crear_nodos(ciudades, tramos)

    def buscar_caminos(self, nodo_actual, destino, camino_actual, caminos_visitados):
        """
        Realiza una búsqueda RECURSIVA (la funcion es usada dentro de la misma funcion) de todos los caminos posibles desde un nodo origen a un destino.
        Toma el origen del viaje y va analizando y uniendo tramos hasta llegar a destino. Una vez que llego a destino, 
        agrego el camino y vuelvo para atras uniendo nuevos tramos y asi generando todos los caminos posibles hasta nuestro destino.
        Almacena todos los caminos encontrados en una lista.
        """
        if nodo_actual.ciudad.nombre == destino:
            caminos_visitados.append(list(camino_actual))
            return

        for tramo in nodo_actual.destinos:
            ciudad_vecina = tramo.destino
            if ciudad_vecina not in [t.origen for t in camino_actual]:  # evitar ciclos
                siguiente_nodo = self.nodos_totales.get(ciudad_vecina)
                if siguiente_nodo:
                    camino_actual.append(tramo)
                    self.buscar_caminos(siguiente_nodo, destino, camino_actual, caminos_visitados)
                    camino_actual.pop() 

    def mostrar_caminos(self, origen, destino, nombre_red, vehiculo, peso): #Consigna para el final --> Modularizar en varias funciones: una que calcule los caminos, otra que muestre los mínimos, etc.
        """
        Muestra todos los caminos posibles entre dos ciudades, calcula distancia, tiempo, costos y restricciones.
        También identifica el camino más barato y el más rápido dentro de la red.
        Ademas devuelve la lista de caminos válidos con información de ruta, tiempo, costo y restricciones.
        (LA PARTE DE LAS RESTRICCIONES HAY Q METERLA EN LOS VEHICULOS Y TRAMOS ASI Q EL DOCSTRINGS HABRIA Q MODIFICARLO MAS ADELANTE)
        """
        nodo_origen = self.nodos_totales.get(origen)
        
        if not nodo_origen:
            print(f"No se encontró el nodo de origen '{origen}' en la red {nombre_red}")
            return

        caminos = []
        self.buscar_caminos(nodo_origen, destino, [], caminos)

        print(f"\n Caminos posibles en red {nombre_red} de {origen} a {destino}:")

        if not caminos:
            print("No hay caminos.")
            return
        
        caminos_validos = []

        for i, camino in enumerate(caminos, 1):
            ruta = " -> ".join([tramo.origen for tramo in camino] + [camino[-1].destino])
            distancia_total = sum(t.distancia_km for t in camino)
            tiempo_total = 0
            costo_total = 0
            restricciones_totales = []
            invalido = False
            vehiculos_necesarios = int((peso + vehiculo.carga - 1) // vehiculo.carga)

            for tramo in camino:
                velocidad, costo_fijo, costo_km, inval, restricciones, adicionales = vehiculo.procesar_tramo(tramo, peso, vehiculos_necesarios)

                if inval:
                    invalido = True
                    restricciones_totales.extend(restricciones)
                    break
                
                tiempo_total += tramo.distancia_km / velocidad
                costo_total += (costo_fijo * vehiculos_necesarios) + (costo_km * tramo.distancia_km * vehiculos_necesarios) + adicionales
                restricciones_totales.extend(restricciones)
            
                """if tramo.restriccion:
                    restricciones.append((tramo.restriccion, tramo.valor_restriccion))
                
                velocidad_tramo = vehiculo.velocidad

                #Restricciones de Tramos
                velocidad_tramo, costoFijo, costo_por_km, invalido = tramo.aplicar_restricciones(vehiculo,peso,vehiculos_necesarios)

                #Restricciones de Vehiculos

                velocidad_tramo,costo_por_km, costoFijo = RedNodos.restriccion_vehiculo(tramo,vehiculo,velocidad_tramo,costo_por_km,costoFijo, mal_tiempo,"""
                '''
                if isinstance(tramo, TramoAereo):
                    velocidad_tramo, mal_tiempo = vehiculo.restriccion_Aerea(tramo)            
                
                if mal_tiempo:
                    print(f"    Este tramo tuvo mal tiempo en algún tramo aéreo. Velocidad reducida.")                

                if isinstance(tramo, TramoFerroviario): #Correcto
                    costo_por_km = vehiculo.restriccion_Ferroviaria(tramo.distancia_km)
                
                if isinstance(tramo, TramoMaritimo):
                    costoFijo = vehiculo.restriccion_Maritima(tramo)

                '''

                #costo_total += (costoFijo * vehiculos_necesarios + costo_por_km * tramo.distancia_km * vehiculos_necesarios)
                #tiempo_horas += tramo.distancia_km / velocidad_tramo      

            #if isinstance(tramo, TramoAutomotor):
                #costo_total += vehiculo.restriccion_Automotor(peso)
            #else:
                #costo_total += costo_kg * peso

            if invalido:
                print(f"  {ruta} - Camino inválido por restricciones:")
                for restr, val in restricciones:
                    print(f"     - {restr}: {val}")
                continue

            caminos_validos.append({
                "indice": i,
                "ruta": ruta,
                "distancia": distancia_total,
                "tiempo": tiempo_total,
                "costo": costo_total,
                "vehiculos": vehiculos_necesarios,
                "restricciones": restricciones,
                "red": nombre_red,
                "camino": camino  
            })

        if not caminos_validos: 
            print("    No hay caminos viables para esta solicitud.")
            return

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
    
    def restriccion_vehiculo(tramo, vehiculo, velocidad_tramo, costo_por_km, costoFijo,mal_tiempo, invalido):
        if isinstance(tramo, TramoAereo):
            invalido, velocidad_tramo, mal_tiempo = vehiculo.restriccion_Aerea(tramo)                
            if mal_tiempo:
                print(f"    Este tramo tuvo mal tiempo en algún tramo aéreo. Velocidad reducida.")
        elif isinstance(tramo, TramoFerroviario): #Correcto
            invalido, costo_por_km = vehiculo.restriccion_Ferroviaria(tramo.distancia_km)
        elif isinstance(tramo, TramoMaritimo):
            invalido, costoFijo = vehiculo.restriccion_Maritima(tramo)
        return invalido, velocidad_tramo, costo_por_km, costoFijo
    