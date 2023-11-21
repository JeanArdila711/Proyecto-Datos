# Proyecto Final
# Juan Miguel Arriola Mazo - Jean Carlo Ardila Acevedo

# Importanciones y Paquetes
import random
import json
from datetime import datetime, timedelta
from faker import Faker


# 1. Generación de chats, Guardado en archivo JSON y Carga de datos desde archivo JSON.
class ManejoChats:
    def __init__(self):
        self.historial_comunicaciones = []

    def generar_chats(self, num_ejemplos):
        fake = Faker()

        for _ in range(num_ejemplos):
            id_emisor = random.randint(1, 10)
            id_receptor = random.randint(1, 10)
            while id_emisor == id_receptor:
                id_receptor = random.randint(1, 10)

            fecha_envio = datetime.now() - timedelta(days=random.randint(0, 365))
            chat = {
                "id_inicio": id_emisor,
                "id_persona_destino": id_receptor,
                "nombre_inicio": fake.first_name(),
                "nombre_persona_destino": fake.first_name(),
                "mensaje": fake.sentence(),
                "fecha_envio": fecha_envio.strftime("%Y-%m-%d"),
                "hora_envio": fecha_envio.strftime("%H:%M:%S"),
            }
            self.historial_comunicaciones.append(chat)

    def guardar_historial_comunicaciones(self, nombre_archivo):
        with open(nombre_archivo, "w") as archivo_json:
            json.dump(self.historial_comunicaciones, archivo_json, indent=2)


# 2. Creación del grafo.
class Persona:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.amigos = {}

    def agregar_amigo(self, amigo, peso):
        if amigo.id in self.amigos:
            self.amigos[amigo.id] += peso
        else:
            self.amigos[amigo.id] = peso


class Grafo:
    def __init__(self):
        self.personas = {}

    def agregar_persona(self, id, nombre):
        if id not in self.personas:
            self.personas[id] = Persona(id, nombre)

    def agregar_amistad(self, persona1, persona2, peso):
        persona1.agregar_amigo(persona2, peso)
        persona2.agregar_amigo(persona1, peso)

    def cargar_desde_json(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            datos_json = json.load(archivo)
            for datos_mensaje in datos_json:
                id_emisor = datos_mensaje['id_inicio']
                id_receptor = datos_mensaje['id_persona_destino']
                peso = 1
                self.agregar_persona(id_emisor, datos_mensaje['nombre_inicio'])
                self.agregar_persona(id_receptor, datos_mensaje['nombre_persona_destino'])
                self.agregar_amistad(self.personas[id_emisor], self.personas[id_receptor], peso)

    def imprimir_matriz_adyacencia(self):
        ids = sorted(self.personas.keys())
        matriz = [[0] * len(ids) for _ in range(len(ids))]

        for i, id1 in enumerate(ids):
            for j, id2 in enumerate(ids):
                if id2 in self.personas[id1].amigos:
                    matriz[i][j] = self.personas[id1].amigos[id2]

        print("Matriz de Adyacencia:")
        for fila in matriz:
            print(fila)

    def encontrar_parejas_mas_mensajes(self):
        parejas_mensajes_maximos = []
        ids = sorted(self.personas.keys())

        for i, id1 in enumerate(ids):
            for j, id2 in enumerate(ids):
                if i < j:
                    if id2 in self.personas[id1].amigos:
                        peso = self.personas[id1].amigos[id2]
                        parejas_mensajes_maximos.append(((self.personas[id1].nombre, self.personas[id2].nombre), peso))
        parejas_mensajes_maximos.sort(key=lambda x: x[1], reverse=True)

        return parejas_mensajes_maximos

    def encontrar_persona_con_mas_amigos(self):
        max_amigos_persona = max(self.personas.values(), key=lambda x: len(x.amigos))
        return max_amigos_persona

    def encontrar_relacion_mas_fuerte(self):
        max_relacion = 0
        ids = sorted(self.personas.keys())
        relacion_mas_fuerte = None

        for id1 in ids:
            for id2 in self.personas[id1].amigos:
                peso = self.personas[id1].amigos[id2]
                if peso > max_relacion:
                    max_relacion = peso
                    relacion_mas_fuerte = (self.personas[id1].nombre, self.personas[id2].nombre)

        return relacion_mas_fuerte, max_relacion


# 3. Función principal.
def main(n):
    grafo_comunicaciones = Grafo()
    manejochats = ManejoChats()
    manejochats.generar_chats(n)
    manejochats.guardar_historial_comunicaciones("historial_comunicaciones.json")
    grafo_comunicaciones.cargar_desde_json("historial_comunicaciones.json")

    # Encontrar y mostrar las parejas más amigas
    parejas_mensajes = grafo_comunicaciones.encontrar_parejas_mas_mensajes()
    print("\nParejas más amigas (por mensajes intercambiados):")
    for pareja, mensajes in parejas_mensajes:
        print(f"Pareja: {pareja}, Mensajes: {mensajes}")

    # Encontrar y mostrar la persona con más amigos
    max_amigos_persona = grafo_comunicaciones.encontrar_persona_con_mas_amigos()
    print(f"\nPersona con más amigos: {max_amigos_persona.nombre}, Cantidad de amigos: {len(max_amigos_persona.amigos)}")

    # Encontrar y mostrar la relación más fuerte
    relacion_mas_fuerte, peso_maximo = grafo_comunicaciones.encontrar_relacion_mas_fuerte()
    print(f"\nRelación más fuerte: {relacion_mas_fuerte}, Peso: {peso_maximo}")


if __name__ == '__main__':
    n = int(input("¿Cuántos datos desea generar?: "))
    main(n)
