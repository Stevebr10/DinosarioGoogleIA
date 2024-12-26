import pygame
import os
import random

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
    Y_POS= 310
    Y_POS_DUCK = 350
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

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800,1000)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50,100)
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, SCRREN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y=325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y=300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y=250
        self.index = 0
    
    def draw(self, SCRREN):
        if self.index >= 9:
            self.index=0
        SCREEN.blit(self.image[self.index //5], self.rect)
        self.index +=1



        


# Función MAIN
def main():
    try:
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles
        run = True  # Mientras run sea true el programa seguirá ejecutándose
        clock = pygame.time.Clock()  # Se crea un objeto reloj para controlar la velocidad del juego (FPS)
        # Creación del Main loop
        player = Dinosaur()  # Instancia de la clase Dinosaurio
        cloud = Cloud()
        game_speed=14
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        font = pygame.font.Font('freesansbold.ttf',20)
        obstacles= []
        death_count=0

        #Puntuacion 
        def score():
            global points, game_speed
            points += 1
            if points % 100 == 0:
                game_speed += 1
            
            text = font.render("Puntos: "+ str(points), True, (0,0,0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)

        #Backgound
        def background():
            global x_pos_bg, y_pos_bg
            image_width = BG.get_width()
            SCREEN.blit(BG,(x_pos_bg, y_pos_bg))
            SCREEN.blit(BG,(image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(BG, (image_width+x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed

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

            #Obstaculos
            if len(obstacles) == 0:
                if random.randint(0,2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0,2)==1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0,2)==2:
                    obstacles.append(Bird(BIRD))
            
            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    #pygame.draw.rect(SCREEN, (255,0,0), player.dino_rect, 2)
                    pygame.time.delay(2000)
                    death_count +=1
                    menu(death_count)

            #backgound
            background()

            #Puntuacion
            score()

            #Dibujo de la Nube
            cloud.draw(SCREEN)
            cloud.update()

            # Actualizar la pantalla
            pygame.display.update()

            # Controlar los FPS
            clock.tick(30)

    except Exception as e:
        print("Se ha producido un error:", e)
    finally:
        pygame.quit()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255,255,255))
        font = pygame.font.Font('freesansbold.ttf',30)

        if death_count==0:
            text = font.render("Presiona cualquier tecla para empezar", True, (0,0,0))
        elif death_count >0:
            text= font.render("Presiona cualquier tecla para reiniciar", True, (0,0,0))
            score= font.render("Tú Puntuación "+str(points),True,(0,0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 -140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
                #if __name__ == "__main__":
                 #   main()


menu(death_count=0)

#if __name__ == "__main__":
 #   main()

