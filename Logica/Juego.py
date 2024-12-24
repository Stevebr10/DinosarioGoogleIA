import pygame
import os

#Inicializacion del pygame

pygame.init()

#Constanttes globales
#Contantes para la configuracion de la ventana
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Ruta base de los recursos (donde se encuentra el script actual)
BASE_PATH = os.path.dirname(__file__)
# Función para construir rutas absolutas
def resource_path(relative_path):
    return os.path.join(BASE_PATH, relative_path)



#Carga de las imagnes para la animacion del dinosaurio

RUNNING = [pygame.image.load(resource_path("Images/Dino/DinoRun1.png")),
           pygame.image.load(resource_path("Images/Dino/DinoRun2.png"))]

JUMMPING = pygame.image.load(resource_path("Images/Dino/DinoJump.png"))
DUCKING = [pygame.image.load(resource_path("Images/Dino/DinoDuck1.png")),
           pygame.image.load(resource_path("Images/Dino/DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(resource_path("Images/Cactus/SmallCactus1.png")),
                pygame.image.load(resource_path("Images/Cactus/SmallCactus2.png")),
                pygame.image.load(resource_path("Images/Cactus/SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(resource_path("Images/Cactus/LargeCactus1.png")),
                pygame.image.load(resource_path("Images/Cactus/LargeCactus2.png")),
                pygame.image.load(resource_path("Images/Cactus/LargeCactus3.png"))]

BIRD = [pygame.image.load(resource_path("Images/Bird/Bird1.png")),
        pygame.image.load(resource_path("Images/Bird/Bird2.png"))]

CLOUD = pygame.image.load(resource_path("Images/Other/Cloud.png"))
BG = pygame.image.load(resource_path("Images/Other/Track.png"))

#Clase dinosaurio
class Dinosaur:
    #Posicion del dinosaurio
    X_POS= 80
    Y_POS= 230
    Y_POS_DUCK = 270
    JUMP_VEL = 8.5

    def __init__(self):
        #Animacion del dinosaurio
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMMPING

        #Atributos del dinosaurio
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        #Animacion del dinosaurio
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
    
    #Funcion para actualizar el dinosaurio
    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index=0
        
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck=False
            self.dino_run=False
            self.dino_jump=True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck=True
            self.dino_run=False
            self.dino_jump=False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck=False
            self.dino_run=True
            self.dino_jump=False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index +=1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index +=1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel *4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))



# Función MAIN
def main():
    try:
        global game_speed
        run = True  # Mientras run sea true el programa seguirá ejecutándose
        clock = pygame.time.Clock()  # Se crea un objeto reloj para controlar la velocidad del juego (FPS)
        # Creación del Main loop
        player = Dinosaur()  # Instancia de la clase Dinosaurio
        game_speed=14

        while run:
            # Manejo de eventos
            for event in pygame.event.get():  # Se itera sobre una lista de eventos
                if event.type == pygame.QUIT:  # Detectar clic en el botón de cierre
                    run = False

            # Limpiamos la pantalla
            SCREEN.fill((255, 255, 255))

            # Entrada del usuario
            userInput = pygame.key.get_pressed()

            # Dibujar y actualizar al dinosaurio
            player.draw(SCREEN)
            player.update(userInput)

            # Actualizar la pantalla
            pygame.display.update()

            # Controlar los FPS
            clock.tick(30)

    except Exception as e:
        print("Se ha producido un error:", e)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()

