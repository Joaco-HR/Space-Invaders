import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
Pantalla = pygame.display.set_mode((898, 506))
pygame.display.set_caption("Space Invaders Full")
clock = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 30)

# Cargar imágenes
fondo = pygame.image.load("Fondos/Juego.png")
nave_img = pygame.image.load("Skin/Ship.png")
nave_img = pygame.transform.scale(nave_img, (50, 40))

alien_img = pygame.image.load("Skin/Crab.png")
alien_img = pygame.transform.scale(alien_img, (40, 30))

bala_img = pygame.image.load("Skin/Bala.png")
bala_img = pygame.transform.scale(bala_img, (10, 10))
bala_alien_img = pygame.image.load("Skin/Bala Alien.png")
bala_alien_img = pygame.transform.scale(bala_alien_img, (10, 10))

explosion_img = pygame.image.load("Skin/Explocion.png")
explosion_img = pygame.transform.scale(explosion_img, (40, 40))

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
        self.rect = pygame.Rect(375, 450, 50, 40)

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
            enemigos.append(Enemigo(100 + col * espacio_x, 50 + fila * espacio_y))

    # Loop de juego
    while jugador.vidas > 0:
        clock.tick(60)
        Pantalla.blit(fondo, (0, 0))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento jugador
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
        if teclas[pygame.K_SPACE]:
            if len(balas) < 5:
                disparo_sonido.play()
                balas.append(Bala(jugador.rect.centerx - 2, jugador.rect.top, -7, bala_img))

        # Movimiento balas
        for bala in balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                balas.remove(bala)

        # Movimiento enemigos y disparos enemigos
        for enemigo in enemigos:
            enemigo.mover()
            if random.randint(0, 300) == 1:
                balas_enemigas.append(Bala(enemigo.rect.centerx, enemigo.rect.bottom, 5, bala_alien_img))

        # Movimiento balas enemigas
        for bala in balas_enemigas[:]:
            bala.mover()
            if bala.rect.top > ALTO:
                balas_enemigas.remove(bala)

        # Colisiones balas jugador con enemigos
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.rect.colliderect(enemigo.rect):
                    explosion_sonido.play()
                    balas.remove(bala)
                    enemigos.remove(enemigo)
                    explosiones.append(Explosion(enemigo.rect.x, enemigo.rect.y))
                    jugador.puntaje += 10
                    break

        # Colisiones balas enemigas con jugador
        for bala in balas_enemigas[:]:
            if bala.rect.colliderect(jugador.rect):
                explosion_sonido.play()
                balas_enemigas.remove(bala)
                jugador.vidas -= 1
                explosiones.append(Explosion(jugador.rect.x, jugador.rect.y))
                break

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

        mostrar_texto(f"Puntaje: {jugador.puntaje}", 10, 10)
        mostrar_texto(f"Vidas: {jugador.vidas}", 680, 10)

        pygame.display.flip()

    pantalla_game_over(jugador.puntaje)
