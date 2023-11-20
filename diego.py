import random
import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class Usuario:
    def __init__(self, user_id):
        self.id = user_id
        self.amigos = set()
    
    def agregar_amigo(self, amigo_id):
        self.amigos.add(amigo_id)

class RedSocial:
    def __init__(self):
        self.usuarios = {}
        self.historial_comunicaciones = []
        self.matriz_adyacencia = None

    def agregar_usuario(self, user_id):
        if user_id not in self.usuarios:
            nombre_usuario = fake.name()
            self.usuarios[user_id] = Usuario(nombre_usuario)

    def agregar_amistad(self, user_id1, user_id2):
        if user_id1 in self.usuarios and user_id2 in self.usuarios:
            self.usuarios[user_id1].agregar_amigo(user_id2)
            self.usuarios[user_id2].agregar_amigo(user_id1)

    def agregar_mensaje(self, id_emisor, id_receptor, mensaje, fecha_envio, hora_envio):
        mensaje_info = {
            "id_emisor": id_emisor,
            "id_receptor": id_receptor,
            "mensaje": mensaje,
            "fecha_envio": fecha_envio,
            "hora_envio": hora_envio
        }
        self.historial_comunicaciones.append(mensaje_info)

    def guardar_historial_comunicaciones(self, nombre_archivo):
        with open(nombre_archivo, "w") as archivo_json:
            json.dump(self.historial_comunicaciones, archivo_json, indent=2)

    def leer_archivo_json(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            datos_json = json.load(archivo)
            for datos_persona in datos_json:
                id_emisor = datos_persona['id_emisor']
                id_receptor = datos_persona['id_receptor']
                mensaje = datos_persona['mensaje']
                fecha_envio = datos_persona['fecha_envio']
                hora_envio = datos_persona['hora_envio']
                self.agregar_usuario(id_emisor)
                self.agregar_usuario(id_receptor)
                self.agregar_amistad(id_emisor, id_receptor)
                self.agregar_mensaje(id_emisor, id_receptor, mensaje, fecha_envio, hora_envio)

    def obtener_hora_mensajes(self, id_emisor, id_receptor):
        horas_mensajes = []
        for mensaje in self.historial_comunicaciones:
            if mensaje['id_emisor'] == id_emisor and mensaje['id_receptor'] == id_receptor:
                horas_mensajes.append(mensaje['hora_envio'])
        return horas_mensajes

    def personas_mas_amigas(self):
        max_amigos = 0
        personas_mas_amigas = []

        for usuario_id, usuario in self.usuarios.items():
            if len(usuario.amigos) > max_amigos:
                max_amigos = len(usuario.amigos)
                personas_mas_amigas = [usuario.id]
            elif len(usuario.amigos) == max_amigos:
                personas_mas_amigas.append(usuario.id)

        return personas_mas_amigas

    def persona_con_mas_amigos(self):
        max_amigos = 0
        persona_con_mas_amigos = None

        for usuario_id, usuario in self.usuarios.items():
            if len(usuario.amigos) > max_amigos:
                max_amigos = len(usuario.amigos)
                persona_con_mas_amigos = usuario.id

        return persona_con_mas_amigos

    def relacion_mas_fuerte(self):
        max_relacion = 0
        relacion_mas_fuerte = None

        for usuario_id, usuario in self.usuarios.items():
            for amigo_id in usuario.amigos:
                if amigo_id in self.usuarios:
                    relacion_actual = len(self.usuarios[usuario_id].amigos.intersection(self.usuarios[amigo_id].amigos))
                    if relacion_actual > max_relacion:
                        max_relacion = relacion_actual
                        relacion_mas_fuerte = (usuario.id, amigo_id)

        return relacion_mas_fuerte

    def generar_matriz_adyacencia(self):
        num_usuarios = len(self.usuarios)
        self.matriz_adyacencia = [[0] * num_usuarios for _ in range(num_usuarios)]
        for usuario_id, usuario in self.usuarios.items():
            for amigo_id in usuario.amigos:
                self.matriz_adyacencia[usuario_id][amigo_id] = 1
            for otro_usuario_id, otro_usuario in self.usuarios.items():
                if usuario_id != otro_usuario_id and otro_usuario_id not in usuario.amigos:
                    self.matriz_adyacencia[usuario_id][otro_usuario_id] = random.randint(0, 1)

def generar_relacion(id_emisor, id_receptor):
    mensaje = fake.sentence()

    fecha_envio_aleatoria = datetime.now() - timedelta(days=random.randint(0, 365))
    hora_envio_aleatoria = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))

    fecha_hora_envio_aleatoria = fecha_envio_aleatoria + hora_envio_aleatoria
    fecha_envio_aleatoria = fecha_hora_envio_aleatoria.strftime("%Y-%m-%d")
    hora_envio_aleatoria = fecha_hora_envio_aleatoria.strftime("%H:%M:%S")

    relacion = {
        "id_emisor": id_emisor,
        "id_receptor": id_receptor,
        "mensaje": mensaje,
        "fecha_envio": fecha_envio_aleatoria,
        "hora_envio": hora_envio_aleatoria
    }
    return relacion

def main(cantidad):
    n = cantidad
    relaciones = []
    for _ in range(n):
        id_emisor = random.randint(0, 13)
        id_receptor = random.randint(0, 13)
        while id_emisor == id_receptor:
            id_receptor = random.randint(0, 13)
        relacion = generar_relacion(id_emisor, id_receptor)
        relaciones.append(relacion)

    with open('historial_comunicaciones.json', "w") as archivo_json:
        json.dump(relaciones, archivo_json, indent=2)

    red_social = RedSocial()
    red_social.leer_archivo_json('historial_comunicaciones.json')

    personas_mas_amigas = red_social.personas_mas_amigas()
    print(f"Personas más amigas: {', '.join([f'{persona}' for persona in personas_mas_amigas])}")

    persona_con_mas_amigos = red_social.persona_con_mas_amigos()
    print(f"Persona con más amigos: {persona_con_mas_amigos}")

    relacion_mas_fuerte = red_social.relacion_mas_fuerte()
    if relacion_mas_fuerte:
        print(f"Relación más fuerte:{relacion_mas_fuerte[0]} y {relacion_mas_fuerte[1]}")
    else:
        print("No se encontró ninguna relación fuerte en la red social.")

    red_social.generar_matriz_adyacencia()
    print("Matriz de adyacencia:")
    for fila in red_social.matriz_adyacencia:
        print(fila)

if __name__ == '__main__':
    main(int(input("¿Cuántos datos desea generar?: ")))
