import random
from datetime import datetime, timedelta

class Usuario:
    def __init__(self, user_id, nombre):
        self.id = user_id
        self.nombre = nombre
        self.amigos = set()
        self.nodo_grafo = Nodo(nombre)  # Crear nodo para el grafo
    
    def agregar_amigo(self, amigo_id):
        self.amigos.add(amigo_id)
        
class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = set()
    
    def agregar_conexion(self, otro_nodo):
        self.conexiones.add(otro_nodo)
        otro_nodo.conexiones.add(self)
    
    def __str__(self):
        return f"{self.nombre}: {', '.join(map(lambda x: x.nombre, self.conexiones))}"

class Grafo:
    def __init__(self):
        self.nodos = set()
    
    def agregar_nodo(self, nodo):
        self.nodos.add(nodo)
    
    def __str__(self):
        return '\n'.join(map(str, self.nodos))

class RedSocial:
    def __init__(self):
        self.usuarios = {}
        self.grafo_comunicacion = {}
        self.grafo_usuarios = Grafo()  # Grafo para usuarios
    
    def agregar_usuario(self, user_id, nombre):
        if user_id not in self.usuarios:
            self.usuarios[user_id] = Usuario(user_id, nombre)
            self.grafo_comunicacion[user_id] = {}
            self.grafo_usuarios.agregar_nodo(self.usuarios[user_id].nodo_grafo)  # Agregar nodo al grafo
    
    def agregar_amistad(self, user_id1, user_id2):
        if user_id1 in self.usuarios and user_id2 in self.usuarios:
            self.usuarios[user_id1].agregar_amigo(user_id2)
            self.usuarios[user_id2].agregar_amigo(user_id1)
            
            # Establecer conexiones en el grafo de usuarios
            nodo1 = self.usuarios[user_id1].nodo_grafo
            nodo2 = self.usuarios[user_id2].nodo_grafo
            nodo1.agregar_conexion(nodo2)
    
    def agregar_mensaje(self, id_emisor, id_receptor):
        if id_emisor in self.grafo_comunicacion and id_receptor in self.grafo_comunicacion:
            if id_receptor not in self.grafo_comunicacion[id_emisor]:
                self.grafo_comunicacion[id_emisor][id_receptor] = []

            # Generar fecha aleatoria en los últimos 30 días
            fecha_aleatoria = datetime.now() - timedelta(days=random.randint(1, 30))
            hora_aleatoria = datetime.strptime(str(random.randint(0, 23)), '%H')
            fecha_hora_aleatoria = fecha_aleatoria.replace(hour=hora_aleatoria.hour,
                                                            minute=random.randint(0, 59),
                                                            second=random.randint(0, 59))
            
            mensaje = self.generar_mensaje_aleatorio()
            mensaje_con_info = {
                "De": self.usuarios[id_emisor].nombre,
                "Para": self.usuarios[id_receptor].nombre,
                "Fecha": fecha_hora_aleatoria.strftime("%Y-%m-%d %H:%M:%S"),
                "Mensaje": mensaje
            }
            self.grafo_comunicacion[id_emisor][id_receptor].append(mensaje_con_info)
            self.guardar_mensajes_en_archivo(mensaje_con_info)

    def generar_mensaje_aleatorio(self):
        mensajes = [
            "Hola, ¿cómo estás?",
            "¡Buenos días!",
            "¿Qué tal tu día?",
            "¡Hola! ¿Cómo va todo?",
            "¡Hola! ¿Qué cuentas de nuevo?",
            "¿Cómo te ha ido?",
            "Me alegra saludarte",
            "¡Qué gusto verte!",
            "¿Has escuchado las últimas noticias?",
            "¿Cuál es tu película favorita?",
            "Hace un día precioso, ¿verdad?",
            "¿Qué opinas sobre el nuevo libro de...",
            "¿Cuál es tu hobby favorito?",
            "¡Feliz día!",
            "¡Buenas tardes!",
            "¿Has visitado algún lugar interesante últimamente?",
            "¿Cómo te va en el trabajo/estudios?",
            "¿Qué planes tienes para el fin de semana?",
            "¡Hola! ¿Qué has estado haciendo?"
        ]
        return random.choice(mensajes)
    
    def guardar_mensajes_en_archivo(self, mensaje_info):
        nombre_archivo = "informacion_mensajes.txt"
        try:
            with open(nombre_archivo, 'a') as archivo:
                archivo.write(f"Información del mensaje:\n")
                for key, value in mensaje_info.items():
                    archivo.write(f"{key}: {value}\n")
                archivo.write("\n")
        except Exception as e:
            print(f"Error al guardar mensaje: {e}")
            print("Ha ocurrido un problema al guardar la información de los mensajes.")
    
    def obtener_mensajes(self, id_emisor, id_receptor):
        if id_emisor in self.grafo_comunicacion and id_receptor in self.grafo_comunicacion[id_emisor]:
            return self.grafo_comunicacion[id_emisor][id_receptor]
        return None

    def personas_mas_amigas(self):
        max_amigos = 0
        personas_mas_amigas = []

        for usuario_id, usuario in self.usuarios.items():
            if len(usuario.amigos) > max_amigos:
                max_amigos = len(usuario.amigos)
                personas_mas_amigas = [usuario.nombre]
            elif len(usuario.amigos) == max_amigos:
                personas_mas_amigas.append(usuario.nombre)

        return personas_mas_amigas

    def persona_con_mas_amigos(self):
        max_amigos = 0
        persona_con_mas_amigos = None

        for usuario_id, usuario in self.usuarios.items():
            if len(usuario.amigos) > max_amigos:
                max_amigos = len(usuario.amigos)
                persona_con_mas_amigos = usuario.nombre

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
                        relacion_mas_fuerte = (self.usuarios[usuario_id].nombre, self.usuarios[amigo_id].nombre)

        return relacion_mas_fuerte

def main():
    cantidad = int(input("¿Cuántos datos desea generar?: "))
    red_social = RedSocial()

    nombres_personas = ["Juan", "María", "Luis", "Ana", "Carlos", "Laura", "Pedro", "Sofía", "Diego", "Valeria", "Miguel", "Elena", "Pablo", "Lucía"]
    
    relaciones = []
    
    for _ in range(cantidad):
        id_emisor = random.randint(0, len(nombres_personas) - 1)
        id_receptor = random.randint(0, len(nombres_personas) - 1)
        while id_emisor == id_receptor:
            id_receptor = random.randint(0, len(nombres_personas) - 1)
        
        relacion = (id_emisor, id_receptor)
        relaciones.append(relacion)
        
        nombre_emisor = nombres_personas[id_emisor]
        nombre_receptor = nombres_personas[id_receptor]
        
        red_social.agregar_usuario(id_emisor, nombre_emisor)
        red_social.agregar_usuario(id_receptor, nombre_receptor)
        red_social.agregar_amistad(id_emisor, id_receptor)
        
        red_social.agregar_mensaje(id_emisor, id_receptor)
    
    personas_mas_amigas = red_social.personas_mas_amigas()
    print(f"Personas más amigas: {', '.join(personas_mas_amigas)}")

    persona_con_mas_amigos = red_social.persona_con_mas_amigos()
    print(f"Persona con más amigos: {persona_con_mas_amigos}")

    relacion_mas_fuerte = red_social.relacion_mas_fuerte()
    print(f"Relación más fuerte: {relacion_mas_fuerte}")

if __name__ == '__main__':
    main()
