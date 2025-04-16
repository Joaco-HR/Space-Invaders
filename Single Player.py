import pygame
import random
import sys
pygame.init()

# Configuración de la pantalla
Pantalla = pygame.display.set_mode((898, 506))
pygame.display.set_caption("Space Invaders")

#Defino el fondo
Fondo_Juegos = pygame.image.load("Fondos/Juego.png")
Fondo_Juegos = pygame.transform.scale(Fondo_Juegos, (898, 506))

while True:
    reloj = pygame.time.Clock()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    Pantalla.blit(Fondo_Juegos , (0, 0))
    reloj.tick(60)
    pygame.display.flip()