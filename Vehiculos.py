import random
from leer_archivos import Archivos

class CreadordeVehiculos:
    """
    Clase encargada de crear vehiculos de transporte entre ciudades a partir de un archivo csv.
    """

    def __init__(self, nombre_archivo):
        """
        Inicializa una instancia del creador de vehiculos.
        """
        self.nombre_archivo = nombre_archivo
        self.archivos = Archivos(nombre_archivo)

    def crear_vehiculos(self):
        """
        Crea objetos de tipo Vehiculo en base a los datos del archivo y devuelve una lista de vehiculos creados, según el tipo de transporte.
        """
        lineas_de_vehiculos = self.archivos.leer_archivo()
        vehiculos = []
        for fila in lineas_de_vehiculos:
            try:
                modo = fila[0]
                velocidad = float(fila[1])
                capacidadKg = float(fila[2])
                costoFijo = float(fila[3])
                costoKm = float(fila[4])
                costoKg = float(fila[5])
                autonomia = float(fila[6])
                
                if modo == "Aereo":
                    vehiculos.append(Aereo(velocidad, capacidadKg, costoFijo, costoKm, costoKg, autonomia))
                elif modo == "Automotor":
                    vehiculos.append(Automotor(velocidad,capacidadKg,costoFijo,costoKm,costoKg,autonomia))
                elif modo == "Maritimo":
                    vehiculos.append(Maritimo(velocidad,capacidadKg,costoFijo,costoKm,costoKg,autonomia))
                elif modo == "Ferroviario":
                    vehiculos.append(Ferroviario(velocidad,capacidadKg,costoFijo,costoKm,costoKg,autonomia))
                else:
                    print(f"Advertencia: Tipo de transporte desconocido '{modo}' en la fila: {fila}")
    
            except (ValueError, IndexError) as e:
                print(f"Error procesando la fila de conexión: {fila}. Error: {e}")
        return vehiculos


class Vehiculo:
    def __init__(self, velocidad,carga,costoFijo,costoKm,costoKg, autonomia):
         self.velocidad = velocidad
         self.carga = carga
         self.costoFijo = costoFijo
         self.costoKm = costoKm
         self.costoKg = costoKg
         self.autonomia = autonomia
    
    def procesar_tramo(self, tramo, peso, vehiculos_necesarios):
        velocidad = self.velocidad
        costo_fijo = self.costoFijo
        costo_km = self.costoKm
        restricciones_aplicadas = []
        invalido = False

        if tramo.restriccion == "velocidad_max":
            velocidad = min(tramo.valor_restriccion, self.velocidad)
            restricciones_aplicadas.append(("velocidad_max", tramo.valor_restriccion))

        if tramo.restriccion == "peso_max":
            peso_por_veh = peso / vehiculos_necesarios
            if peso_por_veh > tramo.valor_restriccion:
                invalido = True
                restricciones_aplicadas.append(("peso_max", tramo.valor_restriccion))

        velocidad, costo_km, costo_fijo, adicionales, nuevas_restricciones = self.restricciones_especificas(
            tramo, peso, velocidad, costo_km, costo_fijo
        )
        restricciones_aplicadas.extend(nuevas_restricciones)

        return velocidad, costo_fijo, costo_km, invalido, restricciones_aplicadas, adicionales

class Ferroviario(Vehiculo):
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg, autonomia):
        super().__init__(velocidad, carga, costoFijo, costoKm, costoKg,autonomia)
    
    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_fijo):
        nuevas_restricciones = []
        if tramo.distancia_km <= self.autonomia and tramo.distancia_km >= 200:
            costo_km = 0.75 * self.costoKm
            nuevas_restricciones.append(("descuento_por_distancia", 0.75))
        return velocidad, costo_km, costo_fijo, 0, nuevas_restricciones
        
class Aereo(Vehiculo):
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg,autonomia):
        super().__init__(velocidad, carga, costoFijo, costoKm, costoKg,autonomia)

    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_fijo):
        nuevas_restricciones = []
        if tramo.restriccion == "prob_mal_tiempo":
            if random.random() < tramo.valor_restriccion:
                velocidad = 400
                nuevas_restricciones.append(("mal_tiempo", tramo.valor_restriccion))
        return velocidad, costo_km, costo_fijo, 0, nuevas_restricciones
    
class Automotor(Vehiculo):
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg, autonomia):
        super().__init__(velocidad, carga, costoFijo, costoKm, costoKg, autonomia)

    def calculo_adicional(self, peso):
        autos_llenos = peso // self.carga
        extra = 0
        if autos_llenos >= 1:
            extra += autos_llenos * 2 * self.carga
            restante = peso - (self.carga * autos_llenos)
            extra += restante if restante < 15000 else 2 * restante
        else:
            extra += peso
        return extra

    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_fijo):
        adicional = self.calculo_adicional(peso)
        nuevas_restricciones = [("costo_extra_peso", adicional)]

        if tramo.distancia_km >= self.autonomia:
            nuevas_restricciones.append(("fuera_autonomia", tramo.distancia_km))

        return velocidad, costo_km, costo_fijo, adicional, nuevas_restricciones

class Maritimo(Vehiculo):
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg,autonomia):
        super().__init__(velocidad, carga, costoFijo, costoKm, costoKg,autonomia)

    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_fijo):
        nuevas_restricciones = []
        if tramo.restriccion == "tipo" and tramo.valor_restriccion == "maritimo":
            costo_fijo = 1500
            nuevas_restricciones.append(("costo_fijo_maritimo", 1500))
        return velocidad, costo_km, costo_fijo, 0, nuevas_restricciones
    
