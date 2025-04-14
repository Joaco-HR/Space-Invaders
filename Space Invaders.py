import pygame

# Inicializar Pygame y sus módulos  
pygame.init()
pygame.mixer.init()

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
Fondo_Juegos = pygame.image.load("Fondos/Juego.png")
Fondo_Juegos = pygame.transform.scale(Fondo_Juegos, (898, 506))
Fondo_Inicio = Fondo_Menu


Boton_return = pygame.image.load("Boton Retorno.png")
Boton_return = pygame.transform.scale(Boton_return, (80, 80))
Boton_return_o = pygame.image.load("Boton Retorno Oscuro.png")
Boton_return_o = pygame.transform.scale(Boton_return_o, (80, 80))
Rectan = Boton_return.get_rect(topleft=(10, 15))

# Fuente
Fuente = pygame.font.Font("Tipografias/PressStart2P-Regular.ttf", 30)

Opciones = ["New Game", "Highscore", "Quit Game"]
Posiciones = [(453.1, 249.9), (450.7, 318.4), (450.7, 389.5)]
Seleccion = 0 
Inicio = ["Start", "Start"]
Posiciones_2 = [(210, 200.9), (210, 380)]

def Boton_Retorno(surface):
    if Fondo_Inicio == Fondo_Seleccion:
        Posi_mouse = pygame.mouse.get_pos()
        if Rectan.collidepoint(Posi_mouse):
            surface.blit(Boton_return_o, Rectan.topleft)
        else:
            surface.blit(Boton_return, Rectan.topleft)
    else:
        None
        
# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
                        print("")
                    elif Seleccion == 2:
                        pygame.quit()
                        exit()
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
                        Fondo_Inicio = Fondo_Juegos
                    elif Seleccion == 1:
                        print("")
    Pantalla.blit(Fondo_Inicio , (0, 0))
    Boton_Retorno(Pantalla)
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
        for i, texto in enumerate(Inicio):
            if i == Seleccion:
                texto_modificado = f">> {texto} <<"
            else:
                texto_modificado = texto
            Texto = Fuente.render(texto_modificado, True, Blanco)
            Recuadro = Texto.get_rect(center= Posiciones_2[i])
            Pantalla.blit(Texto, Recuadro.topleft)
    pygame.display.flip()