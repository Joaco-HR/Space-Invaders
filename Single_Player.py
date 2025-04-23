import pygame
import random
import sys
from Clases import Jugador, Enemigo, Ovni, Bala, Explosion, Bloque, BloqueCreacion


def juego_single_player():
    pygame.init()
    Pantalla = pygame.display.set_mode((930, 600))
    pygame.display.set_caption("Space Invaders")
    
    Fondo_Juego = pygame.image.load("Fondos/Juego.png")
    Fondo_Juego = pygame.transform.scale(Fondo_Juego, (930, 600))
    Fuente = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 15)
    Mensajes = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 40)
    
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
    Bala_img = pygame.image.load("Skin/Bala.png")
    Bala_img = pygame.transform.scale(Bala_img, (80, 80))
    Bala_alien= pygame.image.load("Skin/Bala Alien.png")
    Bala_alien = pygame.transform.scale(Bala_alien, (80, 80))
    Explosion_img = pygame.image.load("Skin/Explocion.png")
    Explosion_img = pygame.transform.scale(Explosion_img, (40, 40))
    
    Blast = pygame.mixer.Sound("Sonidos/Blast.wav")
    Dead = pygame.mixer.Sound("Sonidos/Dead-Alien.wav")
    Explotion = pygame.mixer.Sound("Sonidos/Explotion.wav")
    Fondo = pygame.mixer.Sound("Sonidos/Fondo.mp3")
    
    Niveles = [
     [
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
        ],
        [
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
        ],
        [
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
        ],
        [
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
        ],
        [
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
        ],
        [
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
        ],
        [
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
        ],
        [
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
        ],
        [
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
        ],
        [
            ["O", "O", "O", "O", "O", "O", "O", "O"],
            ["S", "S", "S", "S", "S", "S", "S", "S"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
            ["C", "C", "C", "C", "C", "C", "C", "C"],
        ]
    ]
    
    def crear_enemigos_desde_nivel(nivel):
        enemigos = []
        tipo_enemigo = {
            "C": (Crab_1, Crab_2, Crab_dead, 10),
            "O": (Octopus_1, Octopus_2, Octopus_dead, 30),
            "S": (Squid_1, Squid_2, Squid_dead, 20)
        }
        espacio_x, espacio_y = 70, 70
        for fila_idx, fila in enumerate(nivel):
            for col_idx, tipo in enumerate(fila):
                if tipo in tipo_enemigo:
                    x = 100 + col_idx * espacio_x
                    y = 50 + fila_idx * espacio_y
                    img1, img2, img_dead, puntaje = tipo_enemigo[tipo]
                    enemigo = Enemigo(x, y, img1, img2, img_dead, tipo)
                    enemigo.puntaje = puntaje
                    enemigos.append(Enemigo(x, y, img1, img2, img_dead, puntaje))
        return enemigos
    
    Blanco = (255, 255, 255)
    ANCHO, ALTO = 898, 506
    obstaculos = BloqueCreacion(block_size=6)
    obstaculos.create_multiple_obstacles(-150, 0, 150, x_start=300, y_start=500)
    
    nivel_actual = 0
    ovni = Ovni(Ovni_1, Ovni_2, Ovni_dead)
    reloj = pygame.time.Clock()
    jugador = Jugador()
    balas = []
    balas_enemigas = []
    enemigos = crear_enemigos_desde_nivel(Niveles[nivel_actual])
    explosiones = []
    
    while jugador.vidas > 0:
        reloj.tick(60)
        Pantalla.blit(Fondo_Juego, (0, 0))
        obstaculos.blocks.draw(Pantalla)
        ovni.mover()
        ovni.dibujar()
        Fondo.play()
        if not ovni.muerto:
            for bala in balas[:]:
                if bala.rect.colliderect(ovni.rect):
                    balas.remove(bala)
                    ovni.morir()
                    jugador.puntaje += 50
                    break
                
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
    
        if jugador.disparar(teclas):
            if len(balas) < 5:
                balas.append(Bala(jugador.rect.centerx - 2, jugador.rect.top, -7, Bala_img))
    
        for bala in balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                balas.remove(bala)
    
        for enemigo in enemigos:
            enemigo.mover()
            if random.randint(0, 300) == 1 and not enemigo.muerto:
                balas_enemigas.append(Bala(enemigo.rect.centerx, enemigo.rect.bottom, 5, Bala_alien))
    
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
                    jugador.puntaje += enemigo.tipo
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
    
        Puntaje = Fuente.render(f"Puntaje: {jugador.puntaje}", True, Blanco)
        Vidas = Fuente.render(f"Vidas: {jugador.vidas}", True, Blanco)
        Pantalla.blit(Puntaje, (10, 10))
        Pantalla.blit(Vidas, (750, 10))
        pygame.display.flip()
    
        if not enemigos:
            nivel_actual += 1
            if nivel_actual < len(Niveles):
                texto_nivel = Mensajes.render(f"Nivel {nivel_actual + 1} comenzando...", True, Blanco)
                Pantalla.blit(Fondo_Juego, (0, 0))
                Pantalla.blit(texto_nivel, (60,250))
                pygame.display.flip()
                pygame.time.delay(2000)
                enemigos = crear_enemigos_desde_nivel(Niveles[nivel_actual])
            else:
                texto_final = Mensajes.render("\u00a1Ganaste!", True, Blanco)
                Pantalla.blit(Fondo_Juego, (0, 0))
                Pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2))
                pygame.display.flip()
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()