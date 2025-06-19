from leer_archivos import Archivos

class CreadordeCiudades():
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)
    '''Esta clase hace uso de la clase archivos para traducir los elementos del csv al tipo de dato donde almacenamos las ciudades'''

    def crear_ciudades(self):
        lineas_de_ciudades = self.archivos.leer_archivo()
        return  list(map(lambda linea: Ciudad(nombre=linea[0]), lineas_de_ciudades))
    '''Usamos el metodo map en conjunto con la estructura brindada por el lector de archivos y de ahi instanciamos a cada ciudad'''

class Ciudad():
    ciudades_existentes = []
    def __init__(self,nombre):
        self.nombre = nombre
        Ciudad.ciudades_existentes.append(self.nombre)
    '''La clase que almacena las ciudades. Adicionalmente guardamos los nombres de cada ciudad para ser usados en validaciones cuando las solicitudes sean ingresadas al sistema'''

    def __repr__(self):
        return f"Ciudad({self.nombre})"
    def __str__(self):
        return self.nombre