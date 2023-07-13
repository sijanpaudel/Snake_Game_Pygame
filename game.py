import pygame
import random
import os

pygame.mixer.init()

pygame.init()

#Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
grey = (211, 211, 211)
 
#Game Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width,screen_height))

#Background Image
bgimg = pygame.image.load("background.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

#Intro image
intro = pygame.image.load("snake_start.jpg")
intro = pygame.transform.scale(intro, (screen_width, screen_height)).convert_alpha()

#GameOver Image
over = pygame.image.load("gameover.jpg")
over = pygame.transform.scale(over, (screen_width, screen_height)).convert_alpha()

#Game title
pygame.display.set_caption("Snake Game By Sijan")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((220,220,220))
        gameWindow.blit(intro,(0,0))
        text_screen("Welcome to Snakes", black, 260, 250)
        text_screen("Press Space Bar to Play", black, 230, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.load('back.mp3')
                pygame.mixer.music.play()
                if event.key == pygame.K_SPACE:
                    gameloop()
        pygame.display.update()
        clock.tick(60)

#Game Loop
def gameloop():
    #Game specific variable
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 60
    snk_list = []
    snk_length = 1
    #Check if highscore file exists
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt","w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()


    while not exit_game:
        if game_over:
              
            with open("highscore.txt", "w") as f:
                f.write(f"{highscore}")

            pygame.mixer.music.load('game_over.mp3')
            pygame.mixer.music.play()
            gameWindow.blit(over,(0,0))  
            text_screen("Press Enter to continue", grey ,150, 400)       
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q: # Cheat code
                        score += 10


            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                snk_length += 5
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                if score > int(highscore):
                    highscore = score
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0,0))
            text_screen("Score: " + str(score)+ "   Highscore: " + str(highscore), red, 5, 5)
            #pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('game_over.mp3')
                pygame.mixer.music.play()
            
            if snake_x<0:
                snake_x=screen_width
                snake_x += velocity_x
            if snake_x > screen_width:
                snake_x = 0
                snake_x += velocity_x
            if snake_y < 0:
                snake_y = screen_height
                snake_y += velocity_y
            if snake_y > screen_height:
                snake_y = 0
                snake_y += velocity_y

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()