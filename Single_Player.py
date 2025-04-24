import pygame
import random
import sys
from Clases import Jugador, Enemigo, Ovni, Bala, Explosion, Bloque #Importamos las Clases desde el archivo de clases

def juego_single_player():
    pygame.init()
    #Definimo el tamaño de la pantalla y el nombre de esta
    Pantalla = pygame.display.set_mode((930, 600))
    pygame.display.set_caption("Space Invaders")
    
    #Definimo el fondo
    Fondo_Juego = pygame.image.load("Fondos/Juego.png")
    Fondo_Juego = pygame.transform.scale(Fondo_Juego, (930, 600))
    
    #Definimo las Funtes de los textos
    Informacion = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 15)
    Mensajes = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 40)
    
    #Cargo las diferentes imagenes que uso durante el juego y los transformo en la escala requerida
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
    
    #Defino la musica de fondo del juego
    Fondo = pygame.mixer.Sound("Sonidos/Fondo.mp3")
    
    #Defino la forma de los bloques de defensa
    Defensa =  [
        '  xxxxxxx  ',
        ' xxxxxxxxx ',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxx     xxx',
        'xx       xx'
    ]

    #Defino la formacion de los niveles, representando cada letra un tipo de alien "C" al Crab, "S" al squid y "O" para el Octopus
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
    
    #Definimos la funcion para cargar a los enemigos desde las matrices
    def Crear_Enemigos(Nivel):
        Enemigos = []
        #Creao un diccionario donde cargamos las imagenes de cada tipo de alien y su valor al ser eleminados
        Tipo_enemigo = {
            "C": (Crab_1, Crab_2, Crab_dead, 10),
            "O": (Octopus_1, Octopus_2, Octopus_dead, 30),
            "S": (Squid_1, Squid_2, Squid_dead, 20)
        }
        #Defino variables de los espacio entre enemigos en el eje X y Y
        Espacio_x = 70
        Espacio_y = 50
        
        #Recorre cada fila del nivel, y cada columna de esa fila
        for indice_fila, Fila in enumerate(Nivel):
            for indice_columna, Tipo in enumerate(Fila):
                if Tipo in Tipo_enemigo:
                     #Calcula la posición del enemigo según su fila y columna
                    x = 100 + indice_columna * Espacio_x
                    y = 50 + indice_fila * Espacio_y
                    img1, img2, img_dead, puntaje = Tipo_enemigo[Tipo] # Obtenemos imágenes y puntaje del tipo de enemigo
                    #Crea el enemigo
                    enemigo = Enemigo(x, y, img1, img2, img_dead, Tipo)
                    enemigo.puntaje = puntaje
                    Enemigos.append(Enemigo(x, y, img1, img2, img_dead, puntaje)) # Agrega el enemigo a la lista
        return Enemigos
    
    def verificar_bordes(Enemigos):
        #Recorre todos los enemigos y verifica si alguno tocó el borde de la pantalla
        for enemigo in Enemigos:
            if enemigo.rect.right >= Ancho or enemigo.rect.left <= 0:
                return True
        return False
    
    #Defino algunos coloeres que usare en el codigo
    Blanco = (255, 255, 255)
    Rojo = (255, 0, 0)
    
    #Defini varibles que usare durante el juego
    Ancho = 898
    Alto = 506
    Nivel_actual = 0
    direccion_enemigos = 1
    reloj = pygame.time.Clock()
    ovni = Ovni(Ovni_1, Ovni_2, Ovni_dead)
    nave = Jugador()
    balas = []
    balas_enemigas = []
    enemigos = Crear_Enemigos(Niveles[Nivel_actual])
    explosiones = []
    x_posiciones = [120,320,520,720]
    bloques = []        
    for x in x_posiciones:
        bloque = Bloque(Defensa, Rojo, 8,(x, 450))
        bloques.append(bloque)
        
    #Definimos el bulce principal del juego
    while nave.vidas > 0:
        reloj.tick(60)
        Pantalla.blit(Fondo_Juego, (0, 0))
        #Dibujo las defensas
        for bloque in bloques:
            bloque.dibujar(Pantalla)
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        #Defino los controles del juego
        teclas = pygame.key.get_pressed()
        nave.mover(teclas)
        if nave.disparar(teclas):
            balas.append(Bala(nave.rect.centerx - 12, nave.rect.top, -8, Bala_img))
            
        #Dibujo y muevo las balas de la Nave
        for bala in balas[:]:
            bala.mover()
            if bala.rect.bottom < 0:
                balas.remove(bala)
        
        #Defino los movimientos de los enemigos y disparos
        if verificar_bordes(enemigos):
            direccion_enemigos *= -1
            for enemigo in enemigos:
                enemigo.rect.y += 35
        for enemigo in enemigos:
            enemigo.mover(direccion_enemigos)
            if random.randint(0, 800) == 1 and not enemigo.muerto:
                balas_enemigas.append(Bala(enemigo.rect.centerx + 2, enemigo.rect.bottom, 6, Bala_alien))
            if enemigo.rect.colliderect(nave.rect):  # Si el enemigo toca al nave
                nave.vidas = 0  # El nave pierde todas las vidas
                break
            else:
                for bloque in bloques:
                        if bloque.daño(enemigo.rect):
                            break
                            
        #Defino movimiento de balas enemigas y verificar colisiones con el borde inferior
        for bala in balas_enemigas[:]:
            bala.mover() 
            if bala.rect.top > Alto:
                balas_enemigas.remove(bala)
    
        #Defino la detección de colisiones entre balas de la nave y enemigos/ovni
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.rect.colliderect(enemigo.rect) and not enemigo.muerto:
                    balas.remove(bala)
                    enemigo.muerto = True
                    enemigo.tiempo_muerte = pygame.time.get_ticks()
                    nave.puntaje += enemigo.tipo
                    break
                if bala.rect.colliderect(ovni.rect) and not ovni.muerto:
                    balas.remove(bala)
                    ovni.muerto = True
                    ovni.tiempo_muerte = pygame.time.get_ticks()
                    nave.puntaje += 50
        ovni.dibujar()
        ovni.mover()
        
        #Defino las colisiones entre balas enemigas y la nave/bloques
        for bala in balas_enemigas[:]:
            if bala.rect.colliderect(nave.rect):
                balas_enemigas.remove(bala)
                nave.vidas -= 1
                explosiones.append(Explosion(nave.rect.x, nave.rect.y))
                break
            else:
                for bloque in bloques:
                    if bloque.daño(bala.rect):
                        balas_enemigas.remove(bala)
                        break
        
        #Dibujo a la nave y enemigos
        nave.dibujar()
        for enemigo in enemigos[:]:
            if not enemigo.dibujar():
                enemigos.remove(enemigo)
        
        #Dibujo las balas y explosiones
        for bala in balas:
            bala.dibujar()
        for bala in balas_enemigas:
            bala.dibujar()
        for explosion in explosiones[:]:
            explosion.dibujar()
            if explosion.tiempo <= 0:  
                explosiones.remove(explosion)
    
        #Muestro información en pantalla: puntaje, vidas y nivel
        Puntaje = Informacion.render(f"Puntaje: {nave.puntaje}", True, Blanco)
        Vidas = Informacion.render(f"Vidas: {nave.vidas}", True, Blanco)
        Nivel = Informacion.render(f"Nivel: {Nivel_actual + 1}", True, Blanco)
        Pantalla.blit(Puntaje, (10, 10))
        Pantalla.blit(Vidas, (800, 10))
        Pantalla.blit(Nivel,(10,40))
        pygame.display.flip()
    
        #Defino el cambio de nivel si no quedan enemigos y el fin del juego si no quedan niveles
        if not enemigos:
            Nivel_actual += 1
            if Nivel_actual < len(Niveles):
                texto_nivel = Mensajes.render(f"Nivel {Nivel_actual + 1} comenzando...", True, Blanco)
                Pantalla.blit(Fondo_Juego, (0, 0))
                Pantalla.blit(texto_nivel, (60,250))
                pygame.display.flip()
                pygame.time.delay(2000)
                enemigos = Crear_Enemigos(Niveles[Nivel_actual])
            else:
                texto_final = Mensajes.render("Ganaste!", True, Blanco)
                Pantalla.blit(Fondo_Juego, (0, 0))
                Pantalla.blit(texto_final, (60,250))
                pygame.display.flip()
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()
juego_single_player()