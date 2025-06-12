"""Aca vamos a ir armando el codigo"""
from crear_tramos import CreadorDeTramos
from crear_ciudades import CreadordeCiudades

def main():
    creador_cuidades = CreadordeCiudades("nodos.csv")
    cuidades_creadas = creador_cuidades.crear_ciudades()


    #Solicitud
    creador_tramos = CreadorDeTramos("conexiones.csv",cuidades_creadas) 
    tramos_creados = creador_tramos.crear_tramos()


    for tramo in tramos_creados:
        print(f"Tramo: {tramo.origen} a {tramo.destino}, Tipo: {tramo.tipo}, Distancia: {tramo.distancia_km} km")
        if tramo.restriccion:
            print(f"  Restricción: {tramo.restriccion}, Valor: {tramo.valor_restriccion}")   


main()

