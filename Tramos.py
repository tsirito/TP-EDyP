class Tramo():
    def __init__(self, origen, destino, tipo, distancia_km):
        self.origen = origen
        self.destino = destino
        self.tipo = tipo
        self.distancia_km = distancia_km
        self.restriccion = restriccion
        self.valor_restriccion = valor_restriccion
    pass

# Acá podemos hacer en vez de cada Tramo una clase, podemos hacer por ejemplo TramoAereo(Tramo):, TramoAutos(Tramo)... y asi... Que todas hereden de la propiedad Tramo, pero cada tipo de Tramo tiene sus propiedades únicas (Reestricción, Valor Reestricción, Cálculo de Costos)

class BsasZarate(Tramo):
    pass

class BsasJunin(Tramo):
    pass

class BsasAzul(Tramo):
    pass

class BsasMdp(Tramo):
    pass

class ZarateJunin(Tramo):
    pass

class JuninAzul(Tramo):
    pass

class AzulMdp(Tramo):
    pass