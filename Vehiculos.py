import random
from leer_archivos import Archivos

contador_global = {"valor": 1}
print("Vehiculos.py fue ejecutado")

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
        
        vehiculos_por_tipo = {
            "Aereo": [],
            "Automotor": [],
            "Maritimo": [],
            "Ferroviario": []
        }

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
                    vehiculos_por_tipo["Aereo"].append(Aereo(velocidad, capacidadKg, costoFijo, costoKm, costoKg, autonomia))
                elif modo == "Automotor":
                    vehiculos_por_tipo["Automotor"].append(Automotor(velocidad, capacidadKg, costoFijo, costoKm, costoKg, autonomia))
                elif modo == "Maritimo":
                    vehiculos_por_tipo["Maritimo"].append(Maritimo(velocidad, capacidadKg, costoFijo, costoKm, costoKg, autonomia))
                elif modo == "Ferroviario":
                    vehiculos_por_tipo["Ferroviario"].append(Ferroviario(velocidad, capacidadKg, costoFijo, costoKm, costoKg, autonomia))
                else:
                    print(f"Advertencia: Tipo de transporte desconocido '{modo}' en la fila: {fila}")
                
            except (ValueError, IndexError) as e:
                print(f"Error procesando la fila de conexión: {fila}. Error: {e}")

        return vehiculos_por_tipo

class Vehiculo:
    contador_id = 1

    def __init__(self, velocidad,carga,costoFijo,costoKm,costoKg, autonomia):
         self.id = contador_global["valor"]
         contador_global["valor"] += 1
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
        costo_Kg = self.costoKg
        restricciones_aplicadas = []
        invalido = False

        if tramo.restriccion == "velocidad_max":
            velocidad = min(tramo.valor_restriccion, self.velocidad)
            restricciones_aplicadas.append(("velocidad max", tramo.valor_restriccion))

        if tramo.restriccion == "peso_max":
            peso_por_veh = peso / vehiculos_necesarios
            if peso_por_veh > tramo.valor_restriccion:
                invalido = True
                restricciones_aplicadas.append(("peso max", tramo.valor_restriccion))

        velocidad, costo_km, costo_Kg, costo_fijo, adicionales, nuevas_restricciones, invalido = self.restricciones_especificas(
            tramo, peso, velocidad, costo_km, costo_Kg, costo_fijo, invalido
        )
        restricciones_aplicadas.extend(nuevas_restricciones)

        return velocidad, costo_fijo, costo_km, costo_Kg, invalido, restricciones_aplicadas, adicionales

class Ferroviario(Vehiculo):
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg, autonomia):
        super().__init__(velocidad, carga, costoFijo, costoKm, costoKg,autonomia)
    
    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_Kg, costo_fijo, invalido):
        nuevas_restricciones = []
        if tramo.distancia_km <= self.autonomia:
            if tramo.distancia_km >= 200:
                costo_km = 0.75 * self.costoKm
                nuevas_restricciones.append(("descuento por distancia", 0.75))
        else:
            invalido = True
            nuevas_restricciones.append(("Supero la autonomia", tramo.distancia_km))
        return velocidad, costo_km, costo_fijo, 0, nuevas_restricciones, invalido
        
class Aereo(Vehiculo):
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg,autonomia):
        super().__init__(velocidad, carga, costoFijo, costoKm, costoKg,autonomia)

    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_fijo, invalido):
        nuevas_restricciones = []
        if tramo.distancia_km <= self.autonomia:
            if tramo.restriccion == "prob_mal_tiempo":
                if random.random() < tramo.valor_restriccion:
                    velocidad = 400
                    nuevas_restricciones.append(("mal tiempo", tramo.valor_restriccion))
        else:
            invalido = True
            nuevas_restricciones.append(("Supero la autonomia", tramo.distancia_km))
        return velocidad, costo_km, costo_fijo, 0, nuevas_restricciones, invalido
    
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

    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_fijo, invalido):
        adicional = self.calculo_adicional(peso)
        nuevas_restricciones = [("costo_extra_peso", adicional)]

        if tramo.distancia_km >= self.autonomia:
            invalido = True
            nuevas_restricciones.append(("Supero la autonomia", tramo.distancia_km))

        return velocidad, costo_km, costo_fijo, adicional, nuevas_restricciones, invalido

class Maritimo(Vehiculo):
    def __init__(self, velocidad, carga, costoFijo, costoKm, costoKg,autonomia):
        super().__init__(velocidad, carga, costoFijo, costoKm, costoKg,autonomia)

    def restricciones_especificas(self, tramo, peso, velocidad, costo_km, costo_fijo, invalido):
        nuevas_restricciones = []

        if tramo.distancia_km <= self.autonomia:
            if tramo.restriccion == "tipo" and tramo.valor_restriccion == "maritimo":
                costo_fijo = 1500
                nuevas_restricciones.append(("costo_fijo_maritimo", 1500))
        else:
            nuevas_restricciones.append(("Supero la autonomia", tramo.distancia_km))
            invalido = True
        return velocidad, costo_km, costo_fijo, 0, nuevas_restricciones, invalido
    
