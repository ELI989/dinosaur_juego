import pygame

# Configuración de pantalla
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Activos del juego
BG = pygame.image.load("assets/imagenes/calle.png")

# Velocidad inicial
game_speed = 20

# Obstáculos
obstacles = []
