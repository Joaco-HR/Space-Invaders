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
    def mover(self, presionar):
        if presionar[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if presionar[pygame.K_RIGHT]:
            self.rect.x += self.vel
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
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
        self.imagenes = [imagen_1, imagen_2]
        self.dead = imagen_3
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()
        self.muerto = False
        self.tiempo_muerte = 0
        self.tipo = tipo
        self.balas = []
        self.intervalo_disparo = 1000
        self.ultimo_disparo = 0 
    def obtener_puntos(self):
        """Devuelve los puntos según el tipo de enemigo."""
        if self.tipo == 'C':
            return 10  # Crab
        elif self.tipo == 'S':
            return 20  # Squid
        elif self.tipo == 'O':
            return 30  # Octopus
        return 0
    def mover(self, direccion_global):
        if not self.muerto:
            self.rect.x += direccion_global
    def disparar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo >= self.intervalo_disparo:
            self.ultimo_disparo = tiempo_actual
            nueva_bala = Bala(self.rect.centerx - 7, self.rect.bottom, 5, bala_alien)
            self.balas.append(nueva_bala)
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
    def __init__(self, imagen_1, imagen_2, imagen_3):
        self.rect = pygame.Rect(10, 20, 40, 30)
        self.direccion = 4
        self.imagenes = [imagen_1, imagen_2]
        self.dead = imagen_3
        self.indice_imagen = 0
        self.intervalo_cambio = 500
        self.ultimo_cambio = pygame.time.get_ticks()
        self.muerto = False
        self.tiempo_muerte = 0
        self.esperando_reaparecer = False
        self.tiempo_reaparecer = 0
        self.delay_reaparicion = 6000
    def mover(self):
        if not self.muerto:
            self.rect.x += self.direccion
            if self.rect.right >= ANCHO + 300:  
                self.direccion *= -1  #
            elif self.rect.left <= -300:  
                self.direccion *= -1
                
    def dibujar(self):
        tiempo_actual = pygame.time.get_ticks()
        if self.muerto:
            Pantalla.blit(self.dead, self.rect.topleft)
            Dead.play()
            if tiempo_actual - self.tiempo_muerte >= 300:
                self.muerto = False
                self.esperando_reaparecer = True
                self.tiempo_reaparecer = tiempo_actual  # Marca inicio del delay
        elif self.esperando_reaparecer:
            # Espera hasta que pase el tiempo de delay para reaparecer
            if tiempo_actual - self.tiempo_reaparecer >= self.delay_reaparicion:
                self.reaparecer()
        else:
            # Animación normal del ovni
            if tiempo_actual - self.ultimo_cambio >= self.intervalo_cambio:
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.ultimo_cambio = tiempo_actual
            imagen_actual = self.imagenes[self.indice_imagen]
            Pantalla.blit(imagen_actual, self.rect.topleft)
        return True
    def reaparecer(self):
        self.esperando_reaparecer = False
        self.rect = pygame.Rect(10, 20, 40, 30)
        self.direccion = 4    
        
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
        Explotion.play()
        self.tiempo -= 1

class Bloque:
    def __init__(self, forma, color, pixel, posicion):
        self.forma = [list(fila) for fila in forma]  # Convertimos cada string en lista para poder modificar
        self.color = color
        self.pixel = pixel
        self.posicion = posicion  # (x, y)

    def dibujar(self, pantalla):
        base_x, base_y = self.posicion
        for y, fila in enumerate(self.forma):
            for x, columna in enumerate(fila):
                if columna == 'x':
                    pygame.draw.rect(
                        pantalla,
                        self.color,
                        pygame.Rect(
                            base_x + x * self.pixel,
                            base_y + y * self.pixel,
                            self.pixel,
                            self.pixel
                        )
                    )
    def daño(self, rect_objetivo):
        base_x, base_y = self.posicion
        for fila_idx, fila in enumerate(self.forma):
            for col_idx, celda in enumerate(fila):
                if celda == 'x':
                    x = base_x + col_idx * self.pixel
                    y = base_y + fila_idx * self.pixel
                    rect_celda = pygame.Rect(x, y, self.pixel, self.pixel)
                    if rect_celda.colliderect(rect_objetivo):
                        self.forma[fila_idx][col_idx] = ' '  # Eliminar pixel
                        return True  # Solo eliminamos uno por llamada
        return False