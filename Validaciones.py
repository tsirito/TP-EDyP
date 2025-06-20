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


    def validar_valor_positivo(valor, variable):
        """
        Verifica si el valor es un numero y despues verifico que sea positivo.
        """        
        try:
            valor_float = float(valor)

        except (ValueError, TypeError):
            raise ValueError(f"No se puede convertir el valor '{valor}' a número para {variable}")
        
        if valor_float >= 0:
            return valor_float
        else:
            raise ValueError(f"El valor '{valor}' de {variable} no puede ser negativo.")

    
    def restriccion_existente(valor):
        '''
        Verifica que la restricción leída en el archivo sea una de las existentes.
        '''
        restricciones_existentes = ['prob_mal_tiempo', 'tipo', 'velocidad_max', 'peso_max']

        if valor is None or valor.strip() == "":
            return None

        elif valor not in restricciones_existentes:
            raise ValueError(f"La restricción '{valor}' no está dentro de las restricciones válidas: {restricciones_existentes}")
        
        else:
            return valor

