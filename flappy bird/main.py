import pygame
from pygame.locals import *
from bird import * #import bird.py file
import settings
from pipe import *
import random

pygame.init()

screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption('flappy bird')

#define text
font = pygame.font.SysFont('Arial Bold', 60)
white = (255, 255, 255)

#make text
def draw_text(text, font, text_color, x, y, center_x=False):
    img = font.render(text, True, text_color)
    #center the text
    if center_x:
        x = x - img.get_width() // 2 #adjust x to center the text
    screen.blit(img, (x, y))

#reset game
def reset_game():
    pipe_group.empty()
    bird_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = settings.screen_height // 2
    bird_group.add(flappy)
    settings.score = 0 
    return settings.score

#make timer/set frame rate
clock = pygame.time.Clock()
fps = 60

#load start page assets
title_image = pygame.image.load('images/title.png')
title_image = pygame.transform.scale(title_image, (300, 66))

start_button_image = pygame.image.load('images/start.png')
start_button_image = pygame.transform.scale(start_button_image, (100, 35))

#load game assets
background = pygame.image.load('images/background.png')
image_rect = background.get_rect()

land = pygame.image.load('images/land.png')
image_rect2 = land.get_rect()

restart = pygame.image.load('images/restart.png')
scaled_restart = pygame.transform.scale(restart, (100, 35))

game_over_text = pygame.image.load('images/game_over.png')
scaled_game_over_text = pygame.transform.scale(game_over_text, (300, 66))

#calculate scale factor for bg pic to fit
scale_factor = settings.screen_width / image_rect.width
new_height = int(image_rect.height * scale_factor)

#scale and center the bg pic
scaled_image = pygame.transform.scale(background, (settings.screen_width, new_height))

#calculate scale factor for ground pic to fit
scale_factor2 = settings.screen_width / image_rect2.width
new_height2 = int(image_rect2.height * scale_factor2)

#scale and center the ground pic
scaled_image2 = pygame.transform.scale(land, (settings.screen_width, new_height2))

#ground position
ground_y_position = settings.screen_height - new_height2

#keeps track of all sprites added
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

#instance of bird class to show on screen
flappy = Bird(100, settings.screen_height // 2)
bird_group.add(flappy)

#pipe variables
bottom_pipe = Pipe(300, settings.screen_height // 2, -1)
top_pipe = Pipe(300, settings.screen_height // 2, 1)
pipe_group.add(bottom_pipe)
pipe_group.add(top_pipe)

class Button():
    def __init__(self, x, y, image, hover_effect=True):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) #define position
        self.hover_effect = hover_effect

    def draw(self):
        action = False
        #get mouse position
        position = pygame.mouse.get_pos()
        #check if mouse is over button
        if self.rect.collidepoint(position):
            #if mouse is hovering over the button, increase button size
            if self.hover_effect:
                hovered_image = pygame.transform.scale(self.image, (int(self.rect.width * 1.1), int(self.rect.height * 1.1)))
                screen.blit(hovered_image, (self.rect.x - (hovered_image.get_width() - self.rect.width) // 2, self.rect.y - (hovered_image.get_height() - self.rect.height) // 2))
            else:
                screen.blit(self.image, (self.rect.x, self.rect.y))

            #if button pressed go restart game
            if pygame.mouse.get_pressed()[0] == 1: #if left mouse button is pressed 
                action = True
        #draw button
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

#game over image & restart button
restart_button = Button(settings.screen_width // 2 - 50, settings.screen_height // 2, scaled_restart, hover_effect=True)
game_over = Button(settings.screen_width // 2 - 150, settings.screen_height // 2 - 80, scaled_game_over_text, hover_effect=False)

#start button
start_button = Button(settings.screen_width // 2 - 50, settings.screen_height // 2, start_button_image)
title = Button(settings.screen_width // 2 - 150, settings.screen_height // 2 - 80, title_image)

#game loop
run = True
game_active = False #tracks whether the game is active or not after the landing page

while run:

    #slow down the scroll speed
    clock.tick(fps)

    #landing page logic
    if not game_active:
        screen.blit(scaled_image, (0, 0))
        screen.blit(title_image, (settings.screen_width // 2 - 150, settings.screen_height // 2 - 80))
        if start_button.draw():
            game_active = True  #transition to the game

            #reset pipe group and score when game starts
            pipe_group.empty()  #clear all pipes
            settings.score = 0  #reset score

    else:
        #display the scaled bg pic
        screen.blit(scaled_image, (0, 0))

        #reset ground position if it goes off screen
        if settings.ground_scroll <= -settings.screen_width:
            settings.ground_scroll = 0

        #display pipe
        pipe_group.draw(screen)

        #update and display bird
        bird_group.update()
        bird_group.draw(screen)

    if game_active:
        draw_text(str(settings.score), font, white, settings.screen_width // 2, 20, center_x=True) #draw score onto screen

    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.centerx > pipe_group.sprites()[0].rect.centerx and not settings.pass_pipe: #check if the bird's center has passed the pipe's center
            settings.pass_pipe = True  #set pass_pipe to true when the bird passes the pipe
            settings.score += 1  #add the score
        elif bird_group.sprites()[0].rect.centerx < pipe_group.sprites()[0].rect.centerx: #reset pass_pipe when the bird is back to the left of the pipe
            settings.pass_pipe = False

    #bird collison with ground
    if flappy.rect.bottom >= 400:
        settings.set_game_over(True)
        settings.set_flying(False)

    #bird collision with pipe or top of screen
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0: #when they collide don't delete it & when it reaches top of screen
        settings.game_over = True


    #display ground & new pipes
    if settings.game_over == False and settings.flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()  # get time now
        if time_now - settings.last_pipe > settings.pipe_frequency: #check if enough time has passed
            pipe_height = random.randint(-150, 50) #pick random number from -100 to 100
            bottom_pipe = Pipe(settings.screen_width, (settings.screen_height // 2) + pipe_height, -1)
            top_pipe = Pipe(settings.screen_width, (settings.screen_height // 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            settings.last_pipe = time_now #update last pipe time so intervals are equal

        #scroll the ground
        screen.blit(scaled_image2,(settings.ground_scroll, ground_y_position))
        screen.blit(scaled_image2, (settings.ground_scroll + settings.screen_width, ground_y_position)) #loop ground appearance
        settings.ground_scroll -= settings.scroll_speed

        #update pipes
        pipe_group.update()
    else:
        screen.blit(scaled_image2,(0,  ground_y_position)) #display still ground

    #check for game over and reset (restart button)
    if settings.game_over == True:
        game_over.draw() #draw game over text
        if restart_button.draw() == True:
            settings.game_over = False #draw restart button if game over
            settings.score = reset_game()

    # quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #if spacebar pressed, bird should fly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and settings.flying == False and settings.game_over == False and game_active == True:
                settings.set_flying(True)

    pygame.display.update() #update display

pygame.quit()
