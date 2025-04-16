import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 898, 506
Pantalla = pygame.display.set_mode((898, 506))

#Cargamos las diferentes imágenes de los aliens, naves, etc., y las ajustamos al tamaño que queremos.
fondo = pygame.image.load("Fondos/Juego.png")
fondo = pygame.transform.scale(fondo, (898, 506))
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

# Definimos las diferentes clases que usaremos para el juego
class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(375, 400, 60, 50)
        self.vidas = 3
        self.puntaje = 0
        self.velocidad = 5
    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def dibujar(self):
        Pantalla.blit(Nave, self.rect.topleft)
        
class Crab:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direccion = 1

        self.imagenes = [Crab_1, Crab_2]
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()

        self.muerto = False
        self.tiempo_muerte = 0

    def mover(self):
        if not self.muerto:
            self.rect.x += self.direccion
            if self.rect.right >= ANCHO or self.rect.left <= 0:
                self.direccion *= -1
                self.rect.y += 10

    def dibujar(self):
        tiempo_actual = pygame.time.get_ticks()
        if self.muerto:
            Pantalla.blit(Crab_dead, self.rect.topleft)
            if tiempo_actual - self.tiempo_muerte >= 500:
                return False
        else:
            if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.ultimo_cambio = tiempo_actual
            imagen_actual = self.imagenes[self.indice_imagen]
            Pantalla.blit(imagen_actual, self.rect.topleft)
        return True
    
class Octopus:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direccion = 1

        self.imagenes = [Octopus_1, Octopus_2]
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()

        self.muerto = False
        self.tiempo_muerte = 0

    def mover(self):
        if not self.muerto:
            self.rect.x += self.direccion
            if self.rect.right >= ANCHO or self.rect.left <= 0:
                self.direccion *= -1
                self.rect.y += 10
    def dibujar(self):
        tiempo_actual = pygame.time.get_ticks()
        if self.muerto:
            Pantalla.blit(Octopus_dead, self.rect.topleft)
            if tiempo_actual - self.tiempo_muerte >= 500:
                return False
        else:
            if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.ultimo_cambio = tiempo_actual
            imagen_actual = self.imagenes[self.indice_imagen]
            Pantalla.blit(imagen_actual, self.rect.topleft)
        return True
class Squid:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direccion = 1

        self.imagenes = [Squid_1, Squid_2]
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()

        self.muerto = False
        self.tiempo_muerte = 0

    def mover(self):
        if not self.muerto:
            self.rect.x += self.direccion
            if self.rect.right >= ANCHO or self.rect.left <= 0:
                self.direccion *= -1
                self.rect.y += 10
    def dibujar(self):
        tiempo_actual = pygame.time.get_ticks()
        if self.muerto:
            Pantalla.blit(Squid_dead, self.rect.topleft)
            if tiempo_actual - self.tiempo_muerte >= 500:
                return False
        else:
            if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.ultimo_cambio = tiempo_actual
            imagen_actual = self.imagenes[self.indice_imagen]
            Pantalla.blit(imagen_actual, self.rect.topleft)
        return True
    
class Ovni:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direccion = 1

        self.imagenes = [Ovni_1, Ovni_2]
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()

        self.muerto = False
        self.tiempo_muerte = 0

    def mover(self):
        if not self.muerto:
            self.rect.x += self.direccion
            if self.rect.right >= ANCHO or self.rect.left <= 0:
                self.direccion *= -1
                self.rect.y += 10
    def dibujar(self):
        tiempo_actual = pygame.time.get_ticks()
        if self.muerto:
            Pantalla.blit(Ovni_dead, self.rect.topleft)
            if tiempo_actual - self.tiempo_muerte >= 500:
                return False
        else:
            if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.ultimo_cambio = tiempo_actual
            imagen_actual = self.imagenes[self.indice_imagen]
            Pantalla.blit(imagen_actual, self.rect.topleft)
        return True

class Bala:
    def __init__(self, x, y, vel, imagen):
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
        self.tiempo -= 1