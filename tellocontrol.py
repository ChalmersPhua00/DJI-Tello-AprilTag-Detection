import pygame

def init():
    pygame.init()

# Returns True if control_key is pressed on the keyboard at the instance getKey() gets called
def getKey(control_key):
    result = False
    for i in pygame.event.get(): pass
    # user_input_key contains all the key pressed on the keyboard at the instance getKey() gets called
    user_input_key = pygame.key.get_pressed()
    if user_input_key[getattr(pygame, 'K_{}'.format(control_key))]:
        result = True
    return result