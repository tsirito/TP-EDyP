from main import *

class Validaciones:
    nodosExistentes = ['']
    def validarNodo(nodo):
        if nodo not in Validaciones.nodosExistentes:
            raise ValueError("la ciudad ingresada no existe")