import csv

class Archivos:
    
    def __init__(self, archivo):
        self.archivo = archivo
        '''
        Metodo constructor del tipo de dato que nos va a permitir traducir los archivos csv
        '''
      
    def leer_archivo(self):
        datos = []
        try:
            with open(self.archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                next(lector, None)  # Esto es para que no lea los titulos 
                for fila in lector:
                    datos.append(fila)
        except FileNotFoundError:
            print(f"Error: El archivo '{self.archivo}' no se encontró.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
        return datos
    '''
    Metodo que traduce los datos en los archivos csv. Itera los mismos para permitir almacenarlos en una lista llamada datos de manera ordenada
    '''
        

