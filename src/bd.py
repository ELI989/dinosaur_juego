
import pygame
import random
import time
from datetime import datetime
import sqlite3  # Importar sqlite3 para manejar la base de datos

pygame.init()

# Conectar a la base de datos SQLite (se creará si no existe)
conn = sqlite3.connect('juego_dino.db')
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora TEXT,
    tiempo_perdido INTEGER
)
''')
conn.commit()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino AI Game")

RUNNING = [pygame.image.load("assets/imagenes/DinoRun1.png"),
           pygame.image.load("assets/imagenes/DinoRun2.png")]
JUMPING = pygame.image.load("assets/imagenes/DinoJump.png")
DUCKING = [pygame.image.load("assets/imagenes/DinoDuck1.png"),
           pygame.image.load("assets/imagenes/DinoDuck2.png")]

SMALL_CACTUS = [pygame.image.load("assets/imagenes/cactuspequeño1.png"),
                pygame.image.load("assets/imagenes/cactuspequeño2.png"),
                pygame.image.load("assets/imagenes/cactuspequeño3.png")]
LARGE_CACTUS = [pygame.image.load("assets/imagenes/Cactus1.png"),
                pygame.image.load("assets/imagenes/Cactus2.png"),
                pygame.image.load("assets/imagenes/Cactus3.png")]

BIRD = [pygame.image.load("assets/imagenes/pajaro1.png"),
        pygame.image.load("assets/imagenes/pajaro2.png")]

BG = pygame.image.load("assets/imagenes/calle.png")
GAME_OVER_IMG = pygame.image.load("assets/imagenes/gameover.png")

pygame.mixer.init()
LOSE_SOUND = "assets/musica/musi.mp3"


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    GRAVITY = 0.8

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.duck_time = 0

    def update(self):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        self.duck_time += 1
        if self.duck_time > 3:
            self.dino_duck = False
            self.dino_run = True
            self.duck_time = 0

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= self.GRAVITY
        if self.dino_rect.y >= self.Y_POS:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice([250, 300])
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def show_menu(start_time, elapsed_time):
    pygame.mixer.music.stop()  
    menu_run = True
    while menu_run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text1 = font.render("Game Over", True, (0, 0, 0))
        text2 = font.render("Presiona R para volver a jugar o Q para salir", True, (0, 0, 0))
        
        # Obtener la fecha y hora de inicio
        start_datetime = datetime.fromtimestamp(start_time)
        start_date = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        # Mostrar fecha, hora y tiempo perdido
        text3 = font.render(f"Inicio: {start_date}", True, (0, 0, 0))
        text4 = font.render(f"Tiempo perdido: {int(elapsed_time)}s", True, (0, 0, 0))
        
        SCREEN.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, SCREEN_HEIGHT//3))
        SCREEN.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, SCREEN_HEIGHT//2))
        SCREEN.blit(text3, (SCREEN_WIDTH//2 - text3.get_width()//2, SCREEN_HEIGHT//2 + 30))
        SCREEN.blit(text4, (SCREEN_WIDTH//2 - text4.get_width()//2, SCREEN_HEIGHT//2 + 60))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    menu_run = False
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()


def save_result(start_time, elapsed_time):
    # Guardar el resultado en la base de datos
    fecha_hora = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO resultados (fecha_hora, tiempo_perdido) VALUES (?, ?)', (fecha_hora, int(elapsed_time)))
    conn.commit()


def main():
    global game_speed, obstacles
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 20
    obstacles = []
    x_pos_bg = 0
    run = True
    start_time = time.time()  # Guardar el tiempo de inicio
    last_speed_increase = start_time

    def background():
        nonlocal x_pos_bg
        SCREEN.blit(BG, (x_pos_bg, 380))
        SCREEN.blit(BG, (x_pos_bg + BG.get_width(), 380))
        if x_pos_bg <= -BG.get_width():
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if time.time() - last_speed_increase > 15:
            game_speed += 2
            last_speed_increase = time.time()

        SCREEN.fill((255, 255, 255))
        background()

        if len(obstacles) == 0 or obstacles[-1].rect.x < SCREEN_WIDTH // 2:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)

        if obstacles:
            obstacle = obstacles[0]
            if isinstance(obstacle, Bird):
                if obstacle.rect.y == 250 and obstacle.rect.x - player.dino_rect.x < 150:
                    player.dino_duck = True
                    player.dino_run = False
                    player.dino_jump = False
                else:
                    if obstacle.rect.x - player.dino_rect.x < 150:
                        if player.dino_rect.y == player.Y_POS:
                            player.dino_duck = False
                            player.dino_run = False
                            player.dino_jump = True
            elif isinstance(obstacle, SmallCactus) or isinstance(obstacle, LargeCactus):
                if obstacle.rect.x - player.dino_rect.x < 150:
                    if player.dino_rect.y == player.Y_POS:
                        player.dino_duck = False
                        player.dino_run = False
                        player.dino_jump = True

        player.update()
        player.draw(SCREEN)

        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Tiempo: {int(elapsed_time)}s", True, (0, 0, 0))
        SCREEN.blit(time_text, (10, 10))

        for obstacle in obstacles:
            if player.dino_rect.colliderect(obstacle.rect):
                SCREEN.fill((255, 0, 0))  
                player.draw(SCREEN) 
                obstacle.draw(SCREEN)  
                pygame.display.update()

                time.sleep(2)

                pygame.mixer.music.load(LOSE_SOUND)
                pygame.mixer.music.play()

                time.sleep(1)
                
                # Guardar el resultado antes de mostrar el menú
                save_result(start_time, elapsed_time)
                
                show_menu(start_time, elapsed_time)  # Pasar el tiempo de inicio y el tiempo perdido al menú

        pygame.display.update()
        clock.tick(30)
import sqlite3

def mostrar_resultados():
    """Muestra todos los resultados guardados en la base de datos."""
    # Establece conexión con la base de datos
    connection = sqlite3.connect("juego.db")
    cursor = connection.cursor()
    
    # Ejecuta la consulta para obtener todos los resultados
    cursor.execute('SELECT * FROM resultados')
    resultados = cursor.fetchall()
    
    # Imprime cada resultado
    for resultado in resultados:
        print(f'ID: {resultado[0]}, Fecha y Hora: {resultado[3]}, Tiempo Perdido: {resultado[4]} segundos')
    
    # Cierra la conexión
    connection.close()

# Cerrar la conexión a la base de datos al finalizar

def close_connection():
    conn.close()

main()
close_connection()  # Asegurarse de cerrar la conexión al final
if __name__ == "__main__":
    mostrar_resultados()
