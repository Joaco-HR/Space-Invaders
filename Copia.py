import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 898, 506
Pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders Full Mejorado")
clock = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 30)

# Cargar imágenes
fondo = pygame.image.load("Fondos/Juego.png")
nave_img = pygame.transform.scale(pygame.image.load("Skin/Ship.png"), (50, 40))
alien_img = pygame.transform.scale(pygame.image.load("Skin/Crab.png"), (40, 30))
bala_img = pygame.transform.scale(pygame.image.load("Skin/Bala.png"), (10, 10))
bala_alien_img = pygame.transform.scale(pygame.image.load("Skin/Bala Alien.png"), (10, 10))
explosion_img = pygame.transform.scale(pygame.image.load("Skin/Explocion.png"), (40, 40))

# Cargar sonidos
pygame.mixer.music.load("Sonidos/Fondo.mp3")
pygame.mixer.music.play(-1)
disparo_sonido = pygame.mixer.Sound("Sonidos/Blast.wav")
explosion_sonido = pygame.mixer.Sound("Sonidos/Explotion.wav")

# Colores
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Clases
class Jugador:
    def __init__(self):
        self.rect = pygame.Rect(375, 460, 50, 40)
        self.vidas = 3
        self.puntaje = 0
        self.vel = 5

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.vel

    def dibujar(self):
        Pantalla.blit(nave_img, self.rect.topleft)

class Enemigo:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.direccion = 1

    def mover(self):
        self.rect.x += self.direccion
        if self.rect.right >= ANCHO or self.rect.left <= 0:
            self.direccion *= -1
            self.rect.y += 10

    def dibujar(self):
        Pantalla.blit(alien_img, self.rect.topleft)

class Bala:
    def __init__(self, x, y, vel, imagen):
        self.rect = pygame.Rect(x, y, 4, 10)
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

class Bloque:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 40)
        self.resistencia = 6  # Se destruye con 3 impactos
    def dibujar(self):
        r = max(0, min(255, 100 * self.resistencia))
        g = max(0, min(255, 255 - self.resistencia * 80))
        color = (r, g, 100)
        pygame.draw.rect(Pantalla, color, self.rect)


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
    bloques = []

    filas, columnas = 4, 8
    espacio_x, espacio_y = 60, 50

    for fila in range(filas):
        for col in range(columnas):
            enemigos.append(Enemigo(100 + col * espacio_x, 50 + fila * espacio_y))

    for i in range(4):
        bloques.append(Bloque(100 + i * 180, 390))

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
                disparo_sonido.play()
                balas.append(Bala(jugador.rect.centerx - 2, jugador.rect.top, -7, bala_img))

        for bala in balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                balas.remove(bala)

        for enemigo in enemigos:
            enemigo.mover()
            if random.randint(0, 500) == 1:  # Menor probabilidad de disparo
                balas_enemigas.append(Bala(enemigo.rect.centerx, enemigo.rect.bottom, 5, bala_alien_img))

        for bala in balas_enemigas[:]:
            bala.mover()
            if bala.rect.top > ALTO:
                balas_enemigas.remove(bala)

        # Colisión de balas con enemigos
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.rect.colliderect(enemigo.rect):
                    explosion_sonido.play()
                    balas.remove(bala)
                    enemigos.remove(enemigo)
                    explosiones.append(Explosion(enemigo.rect.x, enemigo.rect.y))
                    jugador.puntaje += 10
                    break

        # Colisión de balas enemigas con jugador
        for bala in balas_enemigas[:]:
            if bala.rect.colliderect(jugador.rect):
                explosion_sonido.play()
                balas_enemigas.remove(bala)
                jugador.vidas -= 1
                explosiones.append(Explosion(jugador.rect.x, jugador.rect.y))

        # Colisión de balas (ambas) con bloques
        for bloque in bloques[:]:
            for bala in balas[:]:
                if bala.rect.colliderect(bloque.rect):
                    balas.remove(bala)
                    bloque.resistencia -= 1
            for bala in balas_enemigas[:]:
                if bala.rect.colliderect(bloque.rect):
                    balas_enemigas.remove(bala)
                    bloque.resistencia -= 1
            if bloque.resistencia <= 0:
                bloques.remove(bloque)

        # Dibujar todo
        jugador.dibujar()
        for enemigo in enemigos:
            enemigo.dibujar()
        for bala in balas:
            bala.dibujar()
        for bala in balas_enemigas:
            bala.dibujar()
        for explosion in explosiones[:]:
            explosion.dibujar()
            if explosion.tiempo <= 0:
                explosiones.remove(explosion)
        for bloque in bloques:
            bloque.dibujar()

        mostrar_texto(f"Puntaje: {jugador.puntaje}", 10, 10)
        mostrar_texto(f"Vidas: {jugador.vidas}", 750, 10)

        pygame.display.flip()

    pantalla_game_over(jugador.puntaje)