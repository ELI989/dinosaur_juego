import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir las dimensiones de la pantalla
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino AI Game")

# Velocidad de los obstáculos
OBSTACLE_SPEED = 5

# Cargar imágenes de los obstáculos (cactus)
SMALL_CACTUS = [pygame.image.load("assets/imagenes/cactuspequeño1.png"),
                pygame.image.load("assets/imagenes/cactuspequeño2.png"),
                pygame.image.load("assets/imagenes/cactuspequeño3.png")]
LARGE_CACTUS = [pygame.image.load("assets/imagenes/Cactus1.png"),
                pygame.image.load("assets/imagenes/Cactus2.png"),
                pygame.image.load("assets/imagenes/Cactus3.png")]

# Clase para los obstáculos
class Obstacle:
    def __init__(self, x, y, obstacle_type):
        self.x = x
        self.y = y
        self.type = obstacle_type
        if self.type == "small":
            self.image = random.choice(SMALL_CACTUS)
        else:
            self.image = random.choice(LARGE_CACTUS)
        self.rect = self.image.get_rect()  # Obtener el rectángulo de la imagen
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Dibujar la imagen del obstáculo en la pantalla

    def move(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.x < 0:  # Si el obstáculo sale de la pantalla, lo reinicia
            self.rect.x = SCREEN_WIDTH + random.randint(100, 500)  # Reinicia en una posición aleatoria
            self.rect.y = random.randint(300, 450)  # Ajustar altura aleatoria de los obstáculos dentro de un rango razonable

# Crear el reloj de juego
clock = pygame.time.Clock()

# Lista de obstáculos
obstacles = [Obstacle(SCREEN_WIDTH + random.randint(100, 500), SCREEN_HEIGHT - 150, random.choice(["small", "large"]))]

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Llenar la pantalla con un color blanco
    SCREEN.fill((255, 255, 255))

    # Mover y dibujar obstáculos
    for obstacle in obstacles:
        obstacle.move()
        obstacle.draw(SCREEN)

    # Asegurarse de que nuevos obstáculos se generen aleatoriamente
    if random.randint(0, 100) < 2:  # Probabilidad baja de crear un nuevo obstáculo
        obstacles.append(Obstacle(SCREEN_WIDTH + random.randint(100, 500), SCREEN_HEIGHT - 150, random.choice(["small", "large"])))

    # Actualizar la pantalla
    pygame.display.update()

    clock.tick(60)

# Salir de Pygame
pygame.quit()
