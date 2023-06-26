import pygame, sys
from code.settings import *
from code.debug import debug
from code.level import Level
from code.menu import InGameMenu
from code.audio import AudioController

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('One Shot Test')
        self.clock = pygame.time.Clock()
        self.in_game = False
        
        self.level = Level(self.toggle_in_game, self.get_in_game)
        self.main_menu = InGameMenu(self.level.initialize_level)
        
        self.audio_controller = AudioController()
        self.main_sound = pygame.mixer.Sound('audio\\main.ogg')
        self.main_sound.set_volume(self.audio_controller.get_total_volume('music'))
        self.main_sound.play(loops = -1)
    
    def toggle_in_game(self):
        self.in_game = not self.in_game
        
    def get_in_game(self):
        return self.in_game

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Received Quit Event")
                    pygame.quit()
                    sys.exit()

            self.screen.fill(WATER_COLOR)
            self.main_sound.set_volume(self.audio_controller.get_total_volume('music'))
            
            if not self.in_game: self.main_menu.display()
            else: self.level.run()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
