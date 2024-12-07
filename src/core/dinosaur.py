import pygame

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    GRAVITY = 0.8

    def __init__(self):
        self.duck_img = [
            pygame.image.load("assets/imagenes/DinoDuck1.png"),
            pygame.image.load("assets/imagenes/DinoDuck2.png")
        ]
        self.run_img = [
            pygame.image.load("assets/imagenes/DinoRun1.png"),
            pygame.image.load("assets/imagenes/DinoRun2.png")
        ]
        self.jump_img = pygame.image.load("assets/imagenes/DinoJump.png")

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

def game_loop():
    pygame.init()
    SCREEN = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Dinosaur Game")

    clock = pygame.time.Clock()

    dinosaur = Dinosaur()

    running = True
    while running:
        SCREEN.fill((255, 255, 255))  # Fondo blanco

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    dinosaur.dino_duck = True
                    dinosaur.dino_run = False
                if event.key == pygame.K_SPACE and not dinosaur.dino_jump:
                    dinosaur.dino_jump = True
                    dinosaur.dino_run = False
                    dinosaur.dino_duck = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dinosaur.dino_duck = False
                    dinosaur.dino_run = True

        # Actualiza el dinosaurio
        dinosaur.update()

        # Dibuja el dinosaurio
        dinosaur.draw(SCREEN)

        pygame.display.update()
        clock.tick(30)  # Limita la velocidad de fotogramas a 30

    pygame.quit()

if __name__ == "__main__":
    game_loop()
