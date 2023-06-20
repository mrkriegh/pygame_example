import pygame
from settings import *

class InGameMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        self.height = self.display_surface.get_size()[1] // 5
        