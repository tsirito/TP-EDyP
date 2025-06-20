# TP-EDyP
TP-EDyP
Este proyecto se enfoca en la resolución de solicitudes de transporte de carga. Su objetivo principal es encontrar las rutas más eficientes (en costo y tiempo) para una carga, considerando diferentes tipos de vehículos y restricciones específicas de cada tramo.

¿Cómo Funciona?
Lectura de Datos: El programa lee información de archivos CSV sobre ciudades, conexiones entre ellas (tramos) y solicitudes de carga.
Creación de Redes: A partir de los tramos, se construyen redes de transporte separadas para cada tipo de vehículo: ferroviario, automotor, aéreo y fluvial.
Búsqueda de Rutas: Para cada solicitud de carga, el sistema busca todos los caminos posibles desde el origen al destino en cada red de transporte.
Cálculo y Optimización: Se calculan el tiempo y el costo de cada ruta, aplicando las restricciones de los tramos y vehículos. Luego, se identifica la opción más barata y la más rápida entre todas las redes disponibles.
Visualización: Finalmente, se generan gráficos que muestran la distancia acumulada vs. tiempo acumulado y costo acumulado vs. distancia acumulada para el itinerario óptimo.

Características Clave
Manejo de Datos: Procesa archivos CSV para ciudades, conexiones y solicitudes.
Validaciones: Incluye validaciones para asegurar la integridad de los datos de entrada.
Múltiples Transportes: Soporta transporte ferroviario, automotor, aéreo y fluvial de una red a la vez (sin cambios de vehiculo entre caminos)
Restricciones: Considera restricciones como velocidad máxima, peso máximo y condiciones climáticas (para aéreo).
Algoritmo de Búsqueda: Utiliza un algoritmo recursivo DFS para encontrar caminos.
Reporte de Soluciones: Muestra los caminos posibles, sus costos y tiempos, destacando el más barato y el más rápido.