import matplotlib.pyplot as plt

def graficar_itinerario(camino, vehiculo, peso):
    dist_acum = [0]
    tiempo_acum = [0]
    costo_acum = [0]

    vehiculos_necesarios = int((peso + vehiculo.carga - 1) // vehiculo.carga)
    
    total_dist = 0
    total_tiempo = 0
    total_costo = 0
    
    for tramo in camino:
        distancia = tramo.distancia_km
        velocidad = vehiculo.velocidad
        costoFijo = vehiculo.costoFijo
        costo_por_km = vehiculo.costoKm
        costo_kg = vehiculo.costoKg
        
        # Calculo tiempo tramo
        tiempo_tramo = distancia / velocidad
        total_tiempo += tiempo_tramo
        
        # Calculo costo tramo
        costo_tramo = (costoFijo * vehiculos_necesarios) + (costo_por_km * distancia * vehiculos_necesarios) + (costo_kg * peso)
        total_costo += costo_tramo
        
        total_dist += distancia
        
        dist_acum.append(total_dist)
        tiempo_acum.append(total_tiempo)
        costo_acum.append(total_costo)
        
    # Gráfico 1: Distancia acumulada vs Tiempo acumulado
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(tiempo_acum, dist_acum, marker='o')
    plt.title('Distancia Acumulada vs Tiempo Acumulado')
    plt.xlabel('Tiempo acumulado (horas)')
    plt.ylabel('Distancia acumulada (km)')
    plt.grid(True)

    # Gráfico 2: Costo acumulado vs Distancia acumulada
    plt.subplot(1, 2, 2)
    plt.plot(dist_acum, costo_acum, marker='o', color='orange')
    plt.title('Costo Acumulado vs Distancia Acumulada')
    plt.xlabel('Distancia acumulada (km)')
    plt.ylabel('Costo acumulado ($)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
