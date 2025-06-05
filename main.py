"""Aca vamos a ir armando el codigo"""
from leer_archivos import *
from Vehiculos import *
from Validaciones import *
from solicitudes import *
from crear_tramos import CreadorDeTramos
from Tramos import Tramo
from Itinerarios import *
from crear_tramos import *

def main():

    #Creo Archivos
    archivo_conexiones = Archivos("conexiones.csv")
    archivo_nodos=Archivos("nodos.csv")
    archivo_solicitudes=Archivos("solicitudes.csv")

    #Solicitud
    creador = CreadorDeTramos(archivo_conexiones)
    tramos_creados = creador.crear_tramos()

    for tramo in tramos_creados:
        print(f"Tramo: {tramo.origen} a {tramo.destino}, Tipo: {tramo.tipo}, Distancia: {tramo.distancia_km} km")
        if tramo.restriccion:
            print(f"  Restricción: {tramo.restriccion}, Valor: {tramo.valor_restriccion}")   


main()

