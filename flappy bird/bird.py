import pygame
from pygame.locals import *
import settings

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #calls from parent class
        self.images = [] #empty list of images
        self.index = 0 #show 1st image
        self.counter = 0 #rate of animation cycle
 
        for num in range(1,4):
            img = pygame.image.load(f'images/bird{num}.png') #load all bird images
            img = pygame.transform.scale(img, (35, 25))
            self.images.append(img) #add images to list of images
        self.image = self.images[self.index] #get first image
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0

    def update(self):
        if settings.flying == True:
            #make bird fall/gravity
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom <= 400: #stop falling when it hits ground
                self.rect.y += int(self.velocity)

        if settings.game_over == False:
        #bird jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]: #if spacebar pressed
                self.velocity = -5 #bird jumps up

            #handle the animation
            self.counter += 1 #track frame updates
            flap_cooldown = 4 #4 frames pass before switching to next image
            #makes smooth animation
            if self.counter > flap_cooldown: 
                self.counter = 0
                self.index += 1
                #reset index so it loops images
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index] #sets current animation frame

            #rotate the bird when it jumps
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -3) #gets current animation frame and rotates bird
            self.rect = self.image.get_rect(center=self.rect.center) #keep the rotation at the center of the bird
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90) #rotate bird when it falls
