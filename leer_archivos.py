import csv

class Archivos:
    
    def __init__(self, archivo):
        self.archivo = archivo
    
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
    
    
#Creo Archivos
archivo_conexiones = Archivos("conexiones.csv")
archivo_nodos=Archivos("nodos.csv")
archivo_solicitudes=Archivos("solicitudes.csv")

#Leo archivos
conexiones = archivo_conexiones.leer_archivo()
nodos = archivo_nodos.leer_archivo()
solicitudes= archivo_solicitudes.leer_archivo()

print(conexiones)
print(solicitudes)
print(nodos)




