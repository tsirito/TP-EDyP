from ciudades import Ciudad
class Nodo():
    def __init__(self,dato,sig=None):
        self.dato = dato
        self.sig = sig

class Validaciones:
    def validarCiudad(ciudad):
        if ciudad not in Ciudad.ciudades_existentes:
            raise ValueError("la ciudad ingresada no existe")
        else:
            return ciudad
        
    """Valida que la ciudad este en la lista de ciudades que estan dentro de la red de transporte"""
    
    def convertir_a_float(valor, linea=None):
        try:
            return float(valor) if valor != 'null' else None
        except ValueError:
            return valor
        
    """Se usa para el valor de la restriccion ya que puede ser float, str o vacio"""

    
