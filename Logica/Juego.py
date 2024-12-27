import pygame
import os
import random
import numpy as np

from RedNeuronal import NeuralNetwork

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
"""
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

    #Conectamos la red neuronal con el Dinosaurio
    def __init__(self, brain=None):
        # Inicializa el cerebro (red neuronal)
        self.brain = brain if brain else NeuralNetwork(3, 10, 3)  # 3 entradas, 10 ocultas, 3 salidas

    def think(self, inputs):
        # Calcula la acción según los inputs del entorno
        decision = self.brain.forward(inputs)
        return np.argmax(decision)  # Retorna la acción con mayor probabilidad
"""

class Dinosaur:
    # Posiciones y configuraciones iniciales
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 350
    JUMP_VEL = 8.5

    def __init__(self, brain=None):
        # Animaciones del dinosaurio
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMMPING

        # Atributos del dinosaurio
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        # Red neuronal opcional
        self.brain = brain if brain else NeuralNetwork(3, 10, 3)

    def think(self, inputs):
        decision = self.brain.forward(inputs)
        return np.argmax(decision)

    def update(self, action):
        if action == 1:  # Saltar
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif action == 2:  # Agacharse
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        else:  # Correr
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

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
        self.rect.inflate_ip(-5, -5)  # Ajuste del rectángulo

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y=300
        self.rect.inflate_ip(-10, -10)  # Ajuste del rectángulo

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y=265
        #self.rect.y = random.choice([250, 300])
        self.index = 0
    
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index=0
        SCREEN.blit(self.image[self.index //5], self.rect)
        self.index +=1
   

# Función MAIN
"""
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
                game_speed += 2
            
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
                if player.dino_rect.colliderect(obstacle.rect.inflate(-25,-25)):  #obstacle.rect
                    #pygame.draw.rect(SCREEN, (255,0,0), player.dino_rect, 2)
                    pygame.time.delay(2000)
                    death_count +=1
                    menu(death_count)

            #backgound
            background()

            #Puntuacion
            score()

             # Verificar si el jugador gana
            if points >= 1000:
                # Mostrar mensaje de victoria y salir del juego
                text = font.render("¡Has ganado! Puntos: 2500", True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                SCREEN.blit(text, textRect)
                pygame.display.update()
                pygame.time.delay(2000)
                run = False  # Detener el juego

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
"""
        
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 2
        text = font.render("Puntos: " + str(points), True, (0, 0, 0))
        SCREEN.blit(text, (1000, 40))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))

        if obstacles:
            first_obstacle = obstacles[0]
            obstacle_distance = first_obstacle.rect.x - player.dino_rect.x
            obstacle_height = first_obstacle.rect.height
        else:
            obstacle_distance = SCREEN_WIDTH
            obstacle_height = 0

        inputs = np.array([obstacle_distance / SCREEN_WIDTH, obstacle_height / SCREEN_HEIGHT, game_speed / 20])
        action = player.think(inputs)
        player.update(action)

        player.draw(SCREEN)

        if not obstacles or obstacles[0].rect.x < -50:
            obstacle_type = random.choice([SmallCactus, LargeCactus, Bird])
            obstacles.append(obstacle_type(SMALL_CACTUS if obstacle_type != Bird else BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                run = False

        background()
        score()
        cloud.draw(SCREEN)
        cloud.update()

        pygame.display.update()
        clock.tick(30)

    pygame.quit()


#if __name__ == "__main__":
 #   main()

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
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()
                #if __name__ == "__main__":
                 #   main()


menu(death_count=0)

#if __name__ == "__main__":
 #   main()

