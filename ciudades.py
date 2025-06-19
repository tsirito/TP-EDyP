from leer_archivos import Archivos

class CreadordeCiudades():
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_ciudades(self):
        lineas_de_ciudades = self.archivos.leer_archivo()
        return  list(map(lambda linea: Ciudad(nombre=linea[0]), lineas_de_ciudades))

class Ciudad():
    ciudades_existentes = set()
    def __init__(self,nombre):
        self.nombre = nombre
        Ciudad.ciudades_existentes.add(self.nombre)

    def __repr__(self):
        return f"Ciudad({self.nombre})"
    def __str__(self):
        return self.nombre