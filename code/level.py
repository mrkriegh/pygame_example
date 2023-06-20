import pygame
from settings import *
from debug import *
from pytmx.util_pygame import load_pygame
from random import choice, randint
from tile import *
from player import Player
from enemy import Enemy
from weapon import Weapon
from ui import UI
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        #sprite group setup
        #### THIS MEANS Drawing Layers! Change this to be the 3D layers:
        ####   Hidden, Map, Player, Obstacle, Overhead, Skybox
        self.tmx_data = load_pygame('../data/tmx/testmap.tmx')
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        self.map_sprites = MapLayerCameraGroup(self.tmx_data.get_layer_by_name('Base Map'))
        self.structure_sprites = MapLayerCameraGroup(self.tmx_data.get_layer_by_name('Structures'))
#        self.spawner_sprites = MapLayerCameraGroup(self.tmx_data.get_layer_by_name('Entities'))
        self.current_attack = None
        self.spawners = {}
        #self.sprite_group = pygame.sprite.Group()
        #sprite setup
        self.create_map()

        #user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        
        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        for layer in self.tmx_data.layers:
            if hasattr(layer,'data'):
                if layer.name == 'Base Map' or layer.name == 'Structures':
                    groups = self.map_sprites
                elif layer.name == 'Obstacles':
                    groups = self.obstacle_sprites
 #               elif layer.name == 'Entities':
 #                   self.spawn_entities(layer)
 #                   continue
                else:
                    groups = self.visible_sprites
                for x,y,surf in layer.tiles():
                    pos = (x * TILESIZE, y * TILESIZE)
                    Tile(pos = pos, surface = surf, groups = groups, sprite_type = 'object')
        objlayer = self.tmx_data.get_layer_by_name("Entity_Spawners")
        for obj in objlayer:
            if obj.name.split("_")[0] == "Spawn":
                if obj.name == "Spawn_Player":
                    self.player = Player(
                        (obj.x, obj.y),
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        self.create_attack,
                        self.destroy_attack,
                        self.create_magic,
                        )
                else:
                    monster_name = obj.name.split("_")[1].lower()
                    Enemy(
                        monster_name,
                        (obj.x, obj.y),
                        [self.visible_sprites,self.attackable_sprites],
                        self.obstacle_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.add_exp)
        
    
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites,self.attack_sprites])
   
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        # if target_sprite.sprite_type == 'grass':
                            # target_sprite.kill()
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])
    
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
        
    def add_exp(self, amount):
        self.player.exp += amount
        
    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        #self.visible_sprites.draw()
        self.map_sprites.custom_draw(self.player)
        #self.sprite_group.draw(self.display_surface)
        self.structure_sprites.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        
        if self.game_paused:
            self.upgrade.display()
            #display upgrade menu
        else:
            #run the game
            self.map_sprites.update()
            #self.sprite_group.update()
            self.structure_sprites.update()
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            
        


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
 
    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
    
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

class MapLayerCameraGroup(pygame.sprite.Group):
    def __init__(self, tmx_layer):
        #genral setup
        super().__init__()
        self.tmx_layer = tmx_layer
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        #for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
        for x,y,surf in self.tmx_layer.tiles(): # get all the map tiles
            offset_pos = (x * TILESIZE ,y * TILESIZE) - self.offset#surf.get_rect().topleft - self.offset
            self.display_surface.blit(surf,offset_pos)
