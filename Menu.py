import pygame
import sys
import json
from Single_Player import juego_single_player

# Inicializar Pygame y sus módulos  
pygame.init()
#pygame.mixer.init()

# Colores
Blanco = (255, 255, 255)

# Configuración de la pantalla
Pantalla = pygame.display.set_mode((898, 506))
pygame.display.set_caption("Space Invaders")

# Cargar Fondos y escalas
Fondo_Menu = pygame.image.load("Fondos/Space Invaderes.png")
Fondo_Menu = pygame.transform.scale(Fondo_Menu, (898, 506))
Fondo_Seleccion = pygame.image.load("Fondos/Seleccion.png")
Fondo_Seleccion = pygame.transform.scale(Fondo_Seleccion, (898, 506))
Fondo_Highsocre = pygame.image.load("Fondos/Highscore.png")
Fondo_Highsocre = pygame.transform.scale(Fondo_Highsocre, (898, 506))
Fondo_Inicio = Fondo_Menu



Boton_return = pygame.image.load("Skin/Boton Return.png")
Boton_return = pygame.transform.scale(Boton_return, (120, 120))
Boton_return_o = pygame.image.load("Skin/Boton Return Oscuro.png")
Boton_return_o = pygame.transform.scale(Boton_return_o, (120, 120))
Rectan = Boton_return.get_rect(topleft=(0, 0))

# Fuente
Fuente = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 30)

Opciones = ["New Game", "Highscore", "Quit Game"]
Posiciones = [(453.1, 249.9), (450.7, 318.4), (450.7, 389.5)]
Seleccion = 0 
Inicio = ["Start", "Start", Boton_return]
Posiciones_2 = [(210, 200.9), (210, 380),]

def cargar_highscores():
    try:
        with open("highscores.json", "r") as file:
            data = json.load(file)
            return data["highscores"]
    except FileNotFoundError:
        return []
    
def mostrar_highscores(puntajes):
    y_offset = 100  # Posición inicial para los puntajes
    for i, puntaje in enumerate(puntajes):
        texto = f"{puntaje['name']} - {puntaje['score']}"
        renderizado = Fuente.render(texto, True, Blanco)
        Pantalla.blit(renderizado, (350, y_offset + i * 40))
# Bucle principal
while True:
    reloj = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if Fondo_Inicio == Fondo_Menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    Seleccion = (Seleccion + 1) % len(Opciones)
                elif event.key == pygame.K_UP:
                    Seleccion = (Seleccion - 1) % len(Opciones)
                elif event.key == pygame.K_RETURN:
                    if Seleccion == 0:
                        Fondo_Inicio = Fondo_Seleccion
                    elif Seleccion == 1:
                        puntajes = cargar_highscores()
                        Fondo_Inicio = Fondo_Seleccion
                    elif Seleccion == 2:
                        pygame.quit()
                        sys.exit()
        elif Fondo_Inicio == Fondo_Seleccion:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if Rectan.collidepoint(mouse_pos):
                    Fondo_Inicio = Fondo_Menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    Seleccion = (Seleccion + 1) % len(Inicio)
                elif event.key == pygame.K_UP:
                    Seleccion = (Seleccion - 1) % len(Inicio)
                elif event.key == pygame.K_RETURN:
                    if Seleccion == 0:
                        juego_single_player()
                    elif Seleccion == 1:
                        print("")
                    elif Seleccion == 2:
                        Fondo_Inicio = Fondo_Menu
                        
    Pantalla.blit(Fondo_Inicio , (0, 0))
    if Fondo_Inicio == Fondo_Menu:
        for i, texto in enumerate(Opciones):
            if i == Seleccion:
                texto_modificado = f">> {texto} <<"
            else:
                texto_modificado = texto
            Texto = Fuente.render(texto_modificado, True, Blanco)
            Recuadro = Texto.get_rect(center= Posiciones[i])
            Pantalla.blit(Texto, Recuadro.topleft)
    elif Fondo_Inicio == Fondo_Seleccion:
        for i, item in enumerate(Inicio):
            if isinstance(item, str):
                if i == Seleccion:
                    texto_modificado = f">> {item} <<"
                else:
                    texto_modificado = item
                Texto = Fuente.render(texto_modificado, True, Blanco)
                Recuadro = Texto.get_rect(center=Posiciones_2[i])
                Pantalla.blit(Texto, Recuadro.topleft)
            else:
                if i == Seleccion:
                    Pantalla.blit(Boton_return_o, Rectan)
                else:
                    Pantalla.blit(Boton_return, Rectan)
    reloj.tick(60)
    pygame.display.flip()