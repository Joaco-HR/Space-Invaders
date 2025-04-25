import pygame
import sys
import json
from Single_Player import juego_single_player

# Inicializar Pygame y sus módulos  
pygame.init()

# Colores
Blanco = (255, 255, 255)
Dorado = (255, 215, 0)
Plata = (192, 192, 192)
Cobre = (205, 127, 50)

# Configuración de la pantalla
Pantalla = pygame.display.set_mode((898, 506))
pygame.display.set_caption("Space Invaders")

# Cargar Fondos y escalas
Fondo_Menu = pygame.image.load("Fondos/Space Invaderes.png")
Fondo_Menu = pygame.transform.scale(Fondo_Menu, (898, 506))
Fondo_Seleccion = pygame.image.load("Fondos/Seleccion.png")
Fondo_Seleccion = pygame.transform.scale(Fondo_Seleccion, (898, 506))
Fondo_muliplayer = pygame.image.load("Fondos/Multiplayer.png")
Fondo_muliplayer = pygame.transform.scale(Fondo_muliplayer, (898, 506))
Fondo_Highscore = pygame.image.load("Fondos/Highscore.png")  # Cambié nombre a Fondo_Highscore
Fondo_Highscore = pygame.transform.scale(Fondo_Highscore, (898, 506))  # Para ajustar al tamaño
Fondo_Inicio = Fondo_Menu

Boton_return = pygame.image.load("Skin/Boton Return.png")
Boton_return = pygame.transform.scale(Boton_return, (120, 120))
Boton_return_o = pygame.image.load("Skin/Boton Return Oscuro.png")
Boton_return_o = pygame.transform.scale(Boton_return_o, (120, 120))
Rectan = Boton_return.get_rect(topleft=(0, 0))

# Fuente
Fuente = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 30)
Fuente2 = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 20)

Opciones = ["New Game", "Highscore", "Quit Game"]
Posiciones = [(453.1, 249.9), (450.7, 318.4), (450.7, 389.5)]
Seleccion = 0 
Inicio = ["Start", "Start", Boton_return]
Posiciones_2 = [(210, 200.9), (210, 380),]

#Defino la garga del top
def cargar_highscores():
    try:
        with open("puntajes.json", "r") as file:
            contenido = file.read().strip()
            if not contenido:
                return []  # Archivo vacío
            data = json.loads(contenido)
            # Si es una lista directa (como tu archivo), simplemente ordenamos
            if isinstance(data, list):
                puntajes_ordenados = sorted(data, key=lambda x: x["puntaje"], reverse=True)
                return puntajes_ordenados[:5]  # Top 5
            elif isinstance(data, dict) and "puntajes" in data:
                puntajes_ordenados = sorted(data["puntajes"], key=lambda x: x["puntaje"], reverse=True)
                return puntajes_ordenados[:5]  # Top 5
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []

#Definomos como se muestra el top
def mostrar_highscores(puntajes):
    # Título
    titulo = Fuente2.render("Mejores Puntajes", True, Blanco)
    Pantalla.blit(titulo, (70,160))
    
    # Mostrar los 5 puntajes con formato y color
    y_offset = 210
    for i, puntaje in enumerate(puntajes):
        nombre = puntaje["nombre"]
        score = puntaje["puntaje"]

        # Elegir color por posición
        if i == 0:
            color = Dorado
        elif i == 1:
            color = Plata
        elif i == 2:
            color = Cobre
        else:
            color = Blanco

        # Formato visual
        texto = f"{i + 1}- {nombre.ljust(10, '.')} {str(score)}"
        renderizado = Fuente2.render(texto, True, color)
        Pantalla.blit(renderizado, (40, y_offset + i * 40))  # 40 px de separación


# Bucle principal
subpantalla = None
while True:
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
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if Seleccion == 0:
                        Fondo_Inicio = Fondo_Seleccion
                        subpantalla = "start"  # Definir que estamos en el menú de inicio
                    elif Seleccion == 1:
                        puntajes = cargar_highscores()
                        Fondo_Inicio = Fondo_Highscore  # Aquí se cambia el fondo a Highscore
                        subpantalla = "highscores"  # Definir que estamos viendo los puntajes
                    elif Seleccion == 2:
                        pygame.quit()
                        sys.exit()
        elif Fondo_Inicio == Fondo_Highscore:
            mostrar_highscores(puntajes)
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:  # Si se presiona [Enter]
                    Fondo_Inicio = Fondo_Menu        
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
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if Seleccion == 0:
                        juego_single_player()
                    elif Seleccion == 1:
                        Fondo_Inicio = Fondo_muliplayer
                    elif Seleccion == 2:
                        Fondo_Inicio = Fondo_Menu
                        
    Pantalla.blit(Fondo_Inicio, (0, 0))
    
    if Fondo_Inicio == Fondo_Menu:
        for i, texto in enumerate(Opciones):
            if i == Seleccion:
                texto_modificado = f">> {texto} <<"
            else:
                texto_modificado = texto
            Texto = Fuente.render(texto_modificado, True, Blanco)
            Recuadro = Texto.get_rect(center=Posiciones[i])
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
    elif Fondo_Inicio == Fondo_Highscore:
        mostrar_highscores(puntajes)
        salir = Fuente2.render("Presiona [Enter] para volver",True,Blanco)
        Pantalla.blit(salir, (180,460))
    elif Fondo_Inicio == Fondo_muliplayer:
        salir = Fuente2.render("Presiona [Enter] para volver",True,Blanco)
        Pantalla.blit(salir, (180,320))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:  # Si se presiona [Enter]
                    Fondo_Inicio = Fondo_Menu
    pygame.display.flip()