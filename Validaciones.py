class Nodo():
    def __init__(self,dato,sig=None):
        self.dato = dato
        self.sig = sig

class Validaciones:
    def validarCiudad(ciudad):
        if not isinstance(ciudad, ciudadesExitentes):
            raise ValueError("la ciudad ingresada no existe")
    
    
    def convertir_a_float(valor, linea=None):
        try:
            return float(valor) if valor != 'null' else None
        except ValueError:
            return valor

    
    #En vez de retornar none que diga que no lo cree.

class ciudadesExitentes():
    def __init__(self, inicio=None):
        self.inicio = inicio
    
    def agregar(self,ciudad):
        if self.inicio == None:
            self.inicio = ciudad
        else:
            ciudad.sig = self.inicio
            self.inicio = ciudad

    def buscarDato(self,num):
        buscar=self.inicio
       
        while buscar!=None:
            if buscar.dato==num:
                return True
            else:
                buscar=buscar.sig
        return False

    def eliminar(self, nombre):
        if self.buscarDato(nombre):
            actual = self.inicio
            previo = None
            while actual != None:
                if actual.dato == nombre:
                    if previo == None:
                        self.inicio = actual.sig
                    else:
                        previo.sig = actual.sig
                    print('El nodo ha sido eliminado')
                    actual = None  # salir del bucle
                else:
                    previo = actual
                    actual = actual.sig

<<<<<<< HEAD
=======
        
>>>>>>> ca4382e058d27d465b7f1fd878f56f27c533b229
