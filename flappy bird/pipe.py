import pygame
import settings

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self) #inherit sprite functions
        self.image = pygame.image.load('images/pipe.png')
        self.image = pygame.transform.scale(self.image, (43, 259))
        self.rect = self.image.get_rect() #creates rectangle boundary on image
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #flips on y axis, not x axis
            self.rect.bottomleft = [x, y - settings.pipe_gap // 2] #aligns pipe just above the gap
        if position == -1:
            self.rect.topleft = [x, y + settings.pipe_gap // 2] #aligns pipe just below the gap

    def update(self):
        self.rect.x -= settings.scroll_speed
        if self.rect.right < 0:
            self.kill() #remove pipe when it goes off screen