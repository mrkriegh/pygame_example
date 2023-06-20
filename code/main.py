import pygame, sys
from settings import *
from debug import debug
from level import Level

class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('One Shot Test')
        self.clock = pygame.time.Clock()
        
        self.level = Level()
        
        self.main_sound = pygame.mixer.Sound('../audio/main.ogg')
        self.main_sound.set_volume(min(VOLUME['master'],VOLUME['music']))
        self.main_sound.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.main_sound.set_volume(min(VOLUME['master'],VOLUME['music']))
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
