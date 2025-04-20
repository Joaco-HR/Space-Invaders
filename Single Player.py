import pygame
import random
import sys
from Clases import Jugador
from Clases import Enemigo
from Clases import Ovni
from Clases import Bala
from Clases import Explosion
from Clases import Bloque
from Clases import BloqueCreacion

# Datos de inicio
pygame.init()

#Cargamos datos de la pantalla
Pantalla = pygame.display.set_mode((898, 506))
pygame.display.set_caption("Space Invaders")

#Defino el fondo
Fondo_Juego = pygame.image.load("Fondos/Juego.png")
Fondo_Juego = pygame.transform.scale(Fondo_Juego, (898, 506))

#Defino la fuente
Fuente = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 15)

# Cargar Las imagene de el juego
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

#Definimos los sonidos del juego
Blast = pygame.mixer.Sound("Sonidos/Blast.wav")
Dead = pygame.mixer.Sound("Sonidos/Dead-Alien.wav")
Explotion = pygame.mixer.Sound("Sonidos/Explotion.wav")
        
#Definimos variables que utilizaremos en diferentes puntos
Blanco = (255, 255, 255)
ANCHO, ALTO = 898, 506
obstaculos = BloqueCreacion  (block_size=6)
obstaculos.create_multiple_obstacles(-150, 0, 150, x_start=300, y_start=500)

while True:
    ovni = Ovni(Ovni_1, Ovni_2, Ovni_dead)
    reloj = pygame.time.Clock()
    jugador = Jugador()
    balas = []
    balas_enemigas = []
    enemigos = []
    explosiones = []
    filas, columnas = 4, 8
    espacio_x, espacio_y = 70, 70
    for fila in range(filas):
        for col in range(columnas):
            enemigos.append(Enemigo(100 + col * espacio_x, 50 + fila * espacio_y, Octopus_1, Octopus_2, Octopus_dead))
    
    while jugador.vidas > 0:
        reloj.tick(60)
        # Dibujar fondo
        Pantalla.blit(Fondo_Juego, (0, 0))
        
        # **Dibujar obstáculos**
        obstaculos.blocks.draw(Pantalla)
        
        # Mover y dibujar OVNI
        ovni.mover()
        ovni.dibujar()
        
        # Colisión de balas con el OVNI
        if not ovni.muerto:
            for bala in balas[:]:
                if bala.rect.colliderect(ovni.rect):
                    balas.remove(bala)
                    ovni.morir()
                    jugador.puntaje += 50  # OVNI da 50 puntos
                    break
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
        
        # Disparo del jugador
        if jugador.disparar(teclas):
            if len(balas) < 5:  # Evitar más de 5 balas en pantalla
                balas.append(Bala(jugador.rect.centerx - 2, jugador.rect.top, -7, bala_img))
        
        # Movimiento y eliminación de las balas del jugador
        for bala in balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                balas.remove(bala)
        
        # Movimiento de enemigos y disparos
        for enemigo in enemigos:
            enemigo.mover()
            if random.randint(0, 300) == 1 and not enemigo.muerto:
                balas_enemigas.append(Bala(enemigo.rect.centerx, enemigo.rect.bottom, 5, bala_alien))
        
        for bala in balas_enemigas[:]:
            bala.mover()
            if bala.rect.top > ALTO:
                balas_enemigas.remove(bala)
        
        # Colisiones entre balas del jugador y enemigos
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.rect.colliderect(enemigo.rect) and not enemigo.muerto:
                    balas.remove(bala)
                    enemigo.muerto = True
                    enemigo.tiempo_muerte = pygame.time.get_ticks()
                    jugador.puntaje += 10
                    break
        
        # Colisiones entre balas enemigas y el jugador
        for bala in balas_enemigas[:]:
            if bala.rect.colliderect(jugador.rect):
                balas_enemigas.remove(bala)
                jugador.vidas -= 1
                explosiones.append(Explosion(jugador.rect.x, jugador.rect.y))
                break
        
        # Dibujar jugador, enemigos, balas, explosiones
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
        
        # Mostrar puntaje y vidas en pantalla
        Puntaje = Fuente.render(f"Puntaje: {jugador.puntaje}", True, Blanco)
        Vidas = Fuente.render(f"Vidas: {jugador.vidas}", True, Blanco)
        Pantalla.blit(Puntaje, (10, 10))
        Pantalla.blit(Vidas, (750, 10))
        pygame.display.flip()