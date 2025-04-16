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

# Cargar imágenes
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

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Clases
class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(375, 400, 60, 50)
        self.vidas = 3
        self.puntaje = 0
        self.vel = 5
    def mover(self, precionar):
        if precionar[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if precionar[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.vel
    def dibujar(self):
        Pantalla.blit(Nave, self.rect.topleft)

class Enemigo:
    def __init__(self, x, y, imagen_1, imagen_2, imagen_3):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direccion = 1
        self.imagenes = [imagen_1, imagen_2]
        self.dead = imagen_3
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
            Pantalla.blit(self.dead, self.rect.topleft)
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

# Funciones
def mostrar_texto(texto, x, y, color=BLANCO):
    render = fuente.render(texto, True, color)
    Pantalla.blit(render, (x, y))

def pantalla_inicio():
    Pantalla.blit(fondo, (0, 0))
    mostrar_texto("Presiona ESPACIO para empezar", 200, 300)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False

def pantalla_game_over(puntaje):
    Pantalla.blit(fondo, (0, 0))
    mostrar_texto("GAME OVER", 330, 250, ROJO)
    mostrar_texto(f"Puntaje: {puntaje}", 330, 300)
    mostrar_texto("Presiona ESPACIO para reiniciar", 200, 350)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False

# Juego principal
pantalla_inicio()

while True:
    jugador = Jugador()
    balas = []
    balas_enemigas = []
    enemigos = []
    explosiones = []

    filas, columnas = 4, 8
    espacio_x, espacio_y = 60, 50

    for fila in range(filas):
        for col in range(columnas):
            enemigos.append(Enemigo(100 + col * espacio_x, 50 + fila * espacio_y, Octopus_1, Octopus_2, Octopus_dead))

    while jugador.vidas > 0:
        clock.tick(60)
        Pantalla.blit(fondo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
        if teclas[pygame.K_SPACE]:
            if len(balas) < 5:
                balas.append(Bala(jugador.rect.centerx - 2, jugador.rect.top, -7, bala_img))

        for bala in balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                balas.remove(bala)

        for enemigo in enemigos:
            enemigo.mover()
            if random.randint(0, 300) == 1 and not enemigo.muerto:
                balas_enemigas.append(Bala(enemigo.rect.centerx, enemigo.rect.bottom, 5, bala_alien))

        for bala in balas_enemigas[:]:
            bala.mover()
            if bala.rect.top > ALTO:
                balas_enemigas.remove(bala)

        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.rect.colliderect(enemigo.rect) and not enemigo.muerto:
                    balas.remove(bala)
                    enemigo.muerto = True
                    enemigo.tiempo_muerte = pygame.time.get_ticks()
                    jugador.puntaje += 10
                    break

        for bala in balas_enemigas[:]:
            if bala.rect.colliderect(jugador.rect):
                balas_enemigas.remove(bala)
                jugador.vidas -= 1
                explosiones.append(Explosion(jugador.rect.x, jugador.rect.y))
                break

        jugador.dibujar()

        for enemigo in enemigos[:]:
            if not enemigo.dibujar():
                enemigos.remove(enemigo)

        for bala in balas:
            bala.dibujar()
        for bala in balas_enemigas:
            bala.dibujar()
        for explosion in explosiones[:]:
            explosion.dibujar()
            if explosion.tiempo <= 0:
                explosiones.remove(explosion)

        mostrar_texto(f"Puntaje: {jugador.puntaje}", 10, 10)
        mostrar_texto(f"Vidas: {jugador.vidas}", 680, 10)

        pygame.display.flip()

    pantalla_game_over(jugador.puntaje)