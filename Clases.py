import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 898, 506
Pantalla = pygame.display.set_mode((898, 506))
pygame.display.set_caption("Space Invaders Full")
clock = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 30)

# Cargar Las imagenes y sonidos utilizados en el juego
Nave = pygame.image.load("Skin/Ship.png")
Nave = pygame.transform.scale(Nave, (110, 100))
Crab_1 = pygame.image.load("Skin/Alien/Crab 1.png")
Crab_1 = pygame.transform.scale(Crab_1, (100, 100))
Crab_2 = pygame.image.load("Skin/Alien/Crab 2.png")
Crab_2 = pygame.transform.scale(Crab_2, (100, 100))
Crab_dead = pygame.image.load("Skin/Alien/Crab dead.png")
Crab_dead = pygame.transform.scale(Crab_dead, (100, 100))
Octopus_1 = pygame.image.load("Skin/Alien/Octopus 1.png")
Octopus_1 = pygame.transform.scale(Octopus_1, (100, 100))
Octopus_2 = pygame.image.load("Skin/Alien/Octopus 2.png")
Octopus_2 = pygame.transform.scale(Octopus_2, (100, 100))
Octopus_dead = pygame.image.load("Skin/Alien/Octopus dead.png")
Octopus_dead = pygame.transform.scale(Octopus_dead, (100, 100))
Squid_1 = pygame.image.load("Skin/Alien/Squid 1.png")
Squid_1 = pygame.transform.scale(Squid_1, (100, 100))
Squid_2 = pygame.image.load("Skin/Alien/Squid 2.png")
Squid_2 = pygame.transform.scale(Squid_2, (100, 100))
Squid_dead = pygame.image.load("Skin/Alien/Squid dead.png")
Squid_dead = pygame.transform.scale(Squid_dead, (100, 100))
Ovni_1 = pygame.image.load("Skin/Alien/Ovni 1.png")
Ovni_1 = pygame.transform.scale(Ovni_1, (100, 100))
Ovni_2 = pygame.image.load("Skin/Alien/Ovni 2.png")
Ovni_2 = pygame.transform.scale(Ovni_2, (100, 100))
Ovni_dead = pygame.image.load("Skin/Alien/Ovni dead.png")
Ovni_dead = pygame.transform.scale(Ovni_dead, (100, 100))
bala_img = pygame.image.load("Skin/Bala.png")
bala_img = pygame.transform.scale(bala_img, (80, 80))
bala_alien= pygame.image.load("Skin/Bala Alien.png")
bala_alien = pygame.transform.scale(bala_alien, (80, 80))
explosion_img = pygame.image.load("Skin/Explocion.png")
explosion_img = pygame.transform.scale(explosion_img, (40, 40))
Blast = pygame.mixer.Sound("Sonidos/Blast.wav")
Dead = pygame.mixer.Sound("Sonidos/Dead-Alien.wav")
Explotion = pygame.mixer.Sound("Sonidos/Explotion.wav")

# Clases
class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(375, 500, 60, 50)
        self.vidas = 3
        self.puntaje = 0
        self.vel = 5
        self.ultimo_disparo = 0 
        self.intervalo_disparo = 500 
    def mover(self, precionar):
        if precionar[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if precionar[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.vel
    def disparar(self, teclas):
        tiempo_actual = pygame.time.get_ticks()
        if teclas[pygame.K_SPACE] and tiempo_actual - self.ultimo_disparo >= self.intervalo_disparo:
            Blast.play()
            self.ultimo_disparo = tiempo_actual  
            return True 
    def dibujar(self):
        Pantalla.blit(Nave, self.rect.topleft)

class Enemigo:
    def __init__(self, x, y, imagen_1, imagen_2, imagen_3,  tipo):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direccion = 1
        self.imagenes = [imagen_1, imagen_2]
        self.dead = imagen_3
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()
        self.muerto = False
        self.tiempo_muerte = 0
        self.tipo = tipo  # 'C', 'S', 'O'

    def obtener_puntos(self):
        """Devuelve los puntos según el tipo de enemigo."""
        if self.tipo == 'C':
            return 10  # Crab
        elif self.tipo == 'S':
            return 20  # Squid
        elif self.tipo == 'O':
            return 30  # Octopus
        return 0
    def mover(self):
        if not self.muerto:
            self.rect.x += self.direccion
            if self.rect.right >= ANCHO or self.rect.left <= 0:
                self.direccion *= -1
                self.rect.y += 35
    def dibujar(self):
        tiempo_actual = pygame.time.get_ticks()
        if self.muerto:
            Pantalla.blit(self.dead, self.rect.topleft)
            Dead.play()
            if tiempo_actual - self.tiempo_muerte >= 300:
                return False
        else:
            if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.ultimo_cambio = tiempo_actual
            imagen_actual = self.imagenes[self.indice_imagen]
            Pantalla.blit(imagen_actual, self.rect.topleft)
        return True

class Ovni:
    def __init__(self, imagen1, imagen2, imagen_muerte):
        self.imagenes = [imagen1, imagen2]
        self.dead = imagen_muerte
        self.rect = imagen1.get_rect()
        self.rect.y = 10
        self.velocidad = 4
        self.direccion = 1  # 1: izquierda a derecha, -1: derecha a izquierda
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()
        self.muerto = False
        self.sonido_reproducido = False
        self.tiempo_muerte = 0
        self.tiempo_reaparicion = 0
        self.fuera_pantalla = False
        self.tiempo_fuera = 0
        self.reiniciar_posicion()

    def reiniciar_posicion(self):
        if self.direccion == 1:
            self.rect.x = -self.rect.width
        else:
            self.rect.x = 898
        self.muerto = False
        self.sonido_reproducido = False
        self.tiempo_muerte = 0
        self.tiempo_reaparicion = 0
        self.fuera_pantalla = False
        self.tiempo_fuera = 0
    def revivir(self, direccion):
        self.muerto = False
        self.direccion = direccion
        if direccion == "derecha":
            self.rect.x = -self.rect.width
        else:
            self.rect.x = 930
    def mover(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.muerto:
            # Esperar 3 segundos mostrando imagen de muerte
            if tiempo_actual - self.tiempo_muerte >= 1000:
                self.rect.x = -2000  # ocultar de pantalla
                if self.tiempo_reaparicion == 0:
                    self.tiempo_reaparicion = tiempo_actual
            # Después de 10 segundos reaparece
            elif self.tiempo_reaparicion and tiempo_actual - self.tiempo_reaparicion >= 5000:
                self.direccion *= -1
                self.reiniciar_posicion()

        elif self.fuera_pantalla:
            # Salió de la pantalla: espera 10 segundos para reaparecer
            if tiempo_actual - self.tiempo_fuera >= 10000:
                self.direccion *= -1
                self.reiniciar_posicion()

        else:
            self.rect.x += self.velocidad * self.direccion
            if self.rect.right < 0 or self.rect.left > 898:
                if not self.fuera_pantalla:
                    self.fuera_pantalla = True
                    self.tiempo_fuera = tiempo_actual

    def dibujar(self):
        tiempo_actual = pygame.time.get_ticks()
        if self.muerto:
            Pantalla.blit(self.dead, self.rect.topleft)
            if not self.sonido_reproducido:
                Dead.play()
                self.sonido_reproducido = True
            return True
        else:
            if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.ultimo_cambio = tiempo_actual
            imagen_actual = self.imagenes[self.indice_imagen]
            Pantalla.blit(imagen_actual, self.rect.topleft)
            return True

    def morir(self):
        if not self.muerto:
            self.muerto = True
            self.tiempo_muerte = pygame.time.get_ticks()
            self.tiempo_reaparicion = 0
            self.sonido_reproducido = False

class Bloque(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class BloqueCreacion:
    def __init__(self, block_size):
        self.block_size = block_size
        self.blocks = pygame.sprite.Group()
        self.shape = [
            '  xxxxxxx',
            ' xxxxxxxxx',
            'xxxxxxxxxxx',
            'xxxxxxxxxxx',
            'xxxxxxxxxxx',
            'xxx     xxx',
            'xx       xx'
        ]
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Bloque(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)
    def create_multiple_obstacles(self, *offsets, x_start, y_start):
        for offset_x in offsets:
            self.create_obstacle(x_start, y_start, offset_x)
            
class Bala:
    def __init__(self, x, y, vel, imagen, ):
        self.rect = pygame.Rect(x, y, 14, 10)
        self.vel = vel
        self.imagen = imagen
    def mover(self):
        self.rect.y += self.vel
    def dibujar(self):
        Pantalla.blit(self.imagen, self.rect.topleft)

class Explosion:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.tiempo = 15

    def dibujar(self):
        Pantalla.blit(explosion_img, self.rect.topleft)
        Explotion.play()
        self.tiempo -= 1