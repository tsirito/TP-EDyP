from leer_archivos import Archivos
class MainCiudades:
    def crear(archivo):
        creadorCiudades = CreadordeCiudades(archivo)
        ciudades_creadas = creadorCiudades.crear_ciudades()
        return ciudades_creadas

class CreadordeCiudades:
    """
    Clase encargada de crear instancias de la clase Ciudad a partir de un archivo de datos.
    """
    def __init__(self, nombre_archivo):
        """
        Inicializa la clase con el nombre del archivo a utilizar.
        """
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_ciudades(self):
        """
        Crea instancias de la clase Ciudad a partir de las líneas leídas del archivo y retorna una lista de objetos de la clase Ciudad.
        """
        lineas_de_ciudades = self.archivos.leer_archivo()
        return list(map(lambda linea: Ciudad(nombre=linea[0]), lineas_de_ciudades))


class Ciudad:
    """
    Representa una ciudad dentro del sistema. Lleva un registro de todas las ciudades creadas.
    """
    ciudades_existentes = set()

    def __init__(self, nombre):
        """
        Inicializa una nueva instancia de Ciudad y la agrega al conjunto de ciudades existentes.
        """
        self.nombre = nombre
        Ciudad.ciudades_existentes.add(self.nombre)

    def __repr__(self):
        """
        Devuelve el nombre de la ciudad
        """
        return f"Ciudad({self.nombre})"

    def __str__(self):

        return self.nombre

