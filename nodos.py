class NodoCiudad(): #Clase que tiene cada nodo individual
    def __init__(self,ciudad,destinos):
        self.ciudad=ciudad 
        self.destinos=destinos #Lista de destinos

    def __repr__(self):
        return f"Nodo({self.ciudad}, {len(self.destinos)} destinos)"
# Agarrar tramos

class RedNodos: #Clase que tiene todos los nodos
    
    @staticmethod
    def crear_nodos(ciudades, tramos):
        red = {}
        for ciudad in ciudades:
            destinos_desde_ciudad = []
            for tramo in tramos: # Aca recorro los tramos y le agrego cada tramo a la lista 
                if tramo.origen == ciudad.nombre:
                    destinos_desde_ciudad.append(tramo)
                if tramo.destino == ciudad.nombre:
                    #Si estamos parados en Zarate
                    #Aca lo que hacemos es si vemos un tramo Buenos Aires --> Zarate
                    #Guardamos el tramo inverso Zarate --> Buenos Aires  (En en nodo de ZARATE)
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
        
    #Para cada ciudad agarro cada uno de los tramos y con el destino armo cada uno de los nodos 
    def __init__(self, ciudades, tramos):
        self.nodos_totales = RedNodos.crear_nodos(ciudades, tramos)
 