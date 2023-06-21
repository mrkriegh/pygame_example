import pygame
pygame.init()
font = pygame.font.Font(None,30)

def debug(info,y = 10, x = 1100):
    display_surface = pygame.display.get_surface()
    (x) = display_surface.get_size()[0] - 10
    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topright = (x,y))
    pygame.draw.rect(display_surface,'Black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)
