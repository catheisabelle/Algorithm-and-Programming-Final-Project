import pygame

flying = False
game_over = False
screen_width = 600
screen_height = 500
pipe_gap = 150
ground_scroll = 0
scroll_speed = 4
pipe_frequency = 1200 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency #so pipes immediately show at same intervals
score = 0
pass_pipe = False

def set_flying(state):
    global flying
    flying = state

def set_game_over(state):
    global game_over
    game_over = state