import pygame
from settings import *
from debug import *
from random import randint
from audio import AudioController

class MagicPlayer:
    def __init__(self,animation_player):
        self.animation_player = animation_player
        self.audio_controller = AudioController()
        self.sounds = {
            'heal' : pygame.mixer.Sound('../audio/heal.wav'),
            'flame' : pygame.mixer.Sound('../audio/Fire.wav')
        }
        self.sounds['flame'].set_volume(self.audio_controller.get_total_volume('player_attacks'))
        self.sounds['heal'].set_volume(self.audio_controller.get_total_volume('player_spells'))
    
    def heal(self, player, strength, cost, groups):
        if player.energy < cost: return
        player.health += strength
        player.energy -= cost
        
        if player.health >= player.stats['health']:
            player.health = player.stats['health']
        self.animation_player.create_particles('aura',player.hitbox.center,groups)
        self.animation_player.create_particles('heal',player.hitbox.center + pygame.math.Vector2(0,-50),groups)
        self.sounds['heal'].play()
    
    def flame(self, player, cost, groups):
        if player.energy < cost: return
        player.energy -= cost
        
        face = player.status.split("_")[0]
        #placement
        if face == 'right': direction = pygame.math.Vector2(1,0)
        elif face == 'left': direction = pygame.math.Vector2(-1,0)
        elif face == 'up': direction = pygame.math.Vector2(0,-1)
        else: direction = pygame.math.Vector2(0,1)
        
        for i in range(1,6):
            offset_x = 0
            offset_y = 0
            if direction.x: #horizontal
                offset_x = (direction.x * i) * TILESIZE
            else: #vertical
                offset_y = (direction.y * i) * TILESIZE

            x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
            y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
            self.animation_player.create_particles('flame',(x,y),groups)
            self.sounds['flame'].play()
            
        