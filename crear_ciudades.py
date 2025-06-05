from leer_archivos import Archivos
from main import *
from ciudades import Ciudad

class CreadordeCiudades():
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_ciudades(self):
        lineas_de_ciudades = self.archivos.leer_archivo()
        return list(map(lambda linea: Ciudad(nombre_ciudad=linea[0]), lineas_de_ciudades))