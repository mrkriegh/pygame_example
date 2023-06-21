import pygame, sys
from settings import *
from debug import debug
from level import Level
from menu import InGameMenu

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('One Shot Test')
        self.clock = pygame.time.Clock()
        self.in_game = False
        
        self.level = Level(self.toggle_in_game)
        self.main_menu = InGameMenu(self.level.run)
        
        self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
        self.main_sound.set_volume(min(VOLUME['master'],VOLUME['music']))
        self.main_sound.play(loops = -1)
    
    def toggle_in_game(self):
        self.in_game = not self.in_game

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Received Quit Event")
                    pygame.quit()
                    sys.exit()

            self.screen.fill(WATER_COLOR)
            self.main_sound.set_volume(min(VOLUME['master'],VOLUME['music']))
            
            #debug(f"[In Game]:{self.in_game}")
            if not self.in_game: self.main_menu.display()
            else: self.level.run()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
