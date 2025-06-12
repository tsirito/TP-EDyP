class Nodo: #Clase que tiene cada nodo individual
    def init(self,ciudad,destinos):
        self.ciudad=ciudad 
        self.destinos=destinos #Diccionario

# Agarrar tramos

class RedNodos: #Clase que tiene todos los nodos
    
    @staticmethod
    def crear_nodos(ciudades, tramos):
        red = {}
        for ciudad in ciudades:
            destinos_desde_ciudad = {}
            for tramo in tramos: # Aca recorro los tramos y le agrego cada tramo al diccionario
                if tramo.origen == ciudad:
                    destinos_desde_ciudad[tramo.destino]
            nodo = Nodo(ciudad, destinos_desde_ciudad)
            red[ciudad.nombre] = nodo
        return red
            
        
    #Para cada ciudad agarro cada uno de los tramos y con el destino armo cada uno de los nodos 
    def init(self, ciudades, tramos):
        self.nodos_totales = RedNodos.crear_nodos(ciudades, tramos)
        
