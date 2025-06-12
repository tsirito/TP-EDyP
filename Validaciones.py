
class Validaciones:
    ciudadesExistentes = ['']
    def validarCiudad(ciudad):
        if ciudad not in Validaciones.ciudadesExistentes:
            raise ValueError("la ciudad ingresada no existe")
    
    
    def convertir_a_float(valor, linea=None):
        try:
            return float(valor) if valor != 'null' else None
        except ValueError:
            return None #'restriccion invalida'

    #En vez de retornar none que diga que no lo cree.