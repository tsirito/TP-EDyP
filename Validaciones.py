from main import *

class Validaciones:
    ciudadesExistentes = ['']
    def validarCiudad(ciudad):
        if ciudad not in Validaciones.ciudadesExistentes:
            raise ValueError("la ciudad ingresada no existe")