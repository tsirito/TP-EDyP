from ciudades import Ciudad

class Validaciones:
    """
    Clase en donde se van a crear las validaciones que seran usadas a lo largo del programa
    """
    def validarCiudad(ciudad):
        """
        Valida que la ciudad este en la lista de ciudades que estan dentro de la red de transporte
        """
        if ciudad not in Ciudad.ciudades_existentes:
            raise ValueError("la ciudad ingresada no existe")
        else:
            return ciudad 
    
    def convertir_a_float(valor, linea=None):
        """
        Se usa para validar el valor de la restriccion ya que puede ser float, str o vacio.
        Retornamos el valor para cada caso posible.
        """
        try:
            return float(valor) if valor != 'null' else None
        except ValueError:
            return valor
    
    # def valor_negativo(valor, variable):
    #      """
    #      Verifica si un valor numérico es negativo , y si no lo es ademas verifica que sea numerico.
    #      """
    #      if valor <= 0: 
    #          raise ValueError(f'el valor '{valor}' de {variable}, no puede ser negativo o cero.')
    #      else:
    #          try:
    #              return float(valor)

    #          except (ValueError, TypeError) as e:
    #              raise ValueError(f'no se puede convertir el valor '{valor}', a un numero float para la {variable}: {e}')
        
"""
Validaciones q hay q hacer:
tipos de datos de los archivos:
 (distancias y pesos negativos o en forma no numerica)
 (valor restriccion para caso str solo maritimo o fluvial)
 (que la carga no sea la misma?)


"""

