from leer_archivos import Archivos
archivo_conexiones = Archivos("conexiones.csv")
archivo_nodos=Archivos("nodos.csv")
archivo_solicitudes=Archivos("solicitudes.csv")

archivo_conexiones.leer_archivo()
archivo_nodos.leer_archivo()
archivo_solicitudes.leer_archivo()



  