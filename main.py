from crear_tramos import CreadorDeTramos, MainTramos
from ciudades import CreadordeCiudades, Ciudad, MainCiudades
from crear_solicitudes import CreadorDeSolicitudes, MainSolicitudes
from nodos import RedNodos, NodoCiudad, MainRedes
from Vehiculos import CreadordeVehiculos

def main():
    ciudades_creadas = MainCiudades.crear('nodos.csv')
    tramos = MainTramos
    tramos.cargar_tramos('conexiones.csv', ciudades_creadas)
    
    redes = MainRedes
    redes.generar_redes(ciudades_creadas)

    MainSolicitudes.inicializar_vehiculos()

    solicitudes = MainSolicitudes.crear_solicitudes('solicitudes.csv')
    MainSolicitudes.procesar_solicitudes(solicitudes)

main()
