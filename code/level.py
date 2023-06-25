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
from score import ScoreController

class Level:
    def __init__(self, toggle_in_game, get_in_game):
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        self.score = ScoreController()
        self.toggle_in_game = toggle_in_game
        self.get_in_game = get_in_game
#        self.spawner_sprites = MapLayerCameraGroup(self.tmx_data.get_layer_by_name('Entities'))
        self.spawners = {}
        self.enemy_list = []
        #self.sprite_group = pygame.sprite.Group()
        
        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
    
    def initialize_level(self, level_selection):
        #game flags and stats
        self.tutorial_level = False
        self.current_attack = None
        self.can_toggle = True
        self.game_paused = False
        self.game_over = False
        self.end_game = False
        self.game_play_lock = True
        self.player_dead = False
        self.enemy_count = 0
        self.current_wave = 1
        self.wave_cap = 1 if level_selection == "tutorial" else None
        self.wave_spawn_time = 0
        self.spawning_wave = False
        
        
        self.create_map(level_selection)
        self.upgrade = Upgrade(self.player)

        #user interface
        self.ui = UI()
        self.selection_index = 0
        self.selection_time = 0
        self.end_level_time = 0
        
        if not self.get_in_game():
            self.toggle_in_game()

    def create_map(self, level_selection):
        if level_selection == "tutorial":
            self.tmx_data = load_pygame('../data/tmx/testmap.tmx')
            self.tutorial_level = True
        else: self.tmx_data = load_pygame('../data/tmx/arena_map.tmx')
        
        #sprite group setup
        #### THIS MEANS Drawing Layers! Change this to be the 3D layers:
        ####   Hidden, Map, Player, Obstacle, Overhead, Skybox
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.map_sprites = MapLayerCameraGroup(self.tmx_data.get_layer_by_name('Base Map'))
        self.structure_sprites = MapLayerCameraGroup(self.tmx_data.get_layer_by_name('Structures'))
        self.high_structure_sprites = MapLayerCameraGroup(self.tmx_data.get_layer_by_name('High_Structures'))
        
        for layer in self.tmx_data.layers:
            if hasattr(layer,'data'):
                if layer.name == 'Base Map' or layer.name == 'Structures':
                    groups = self.map_sprites
                elif layer.name == 'Obstacles':
                    groups = self.obstacle_sprites
                elif layer.name == 'High_Structures':
                    groups = self.high_structure_sprites
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
                        self.kill_player
                        )
                else:
                    monster_name = obj.name.split("_")[1].lower()
                    self.enemy_list.append(Enemy(
                        monster_name,
                        (obj.x, obj.y),
                        [self.visible_sprites,self.attackable_sprites],
                        self.obstacle_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.add_exp))
                    self.enemy_count += 1

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
    
    def kill_player(self, pos):
        self.trigger_death_particles(pos,"spirit")
        self.player_dead = True
        self.game_over = True
        self.end_level(True)
        
    def end_level_cooldown(self):
        if not self.game_over: return
        current_time = pygame.time.get_ticks()
        self.display_game_over()
        if current_time - self.end_level_time >= 2400:
            if self.end_game:
                self.game_play_lock = False
                self.toggle_in_game()
            else:
                self.initialize_level('arena')
            
    def end_level(self, end_game):
        self.end_level_time = pygame.time.get_ticks()
        self.end_game = end_game
        self.game_over = True
        self.score.update_top_kill_count()
        if not self.player_dead: self.player.kill()
        for enemy in self.enemy_list:
            enemy.kill()

    def spawn_wave(self):
        self.current_wave += 1
        objlayer = self.tmx_data.get_layer_by_name("Entity_Spawners")
        for obj in objlayer:
            if obj.name.split("_")[0] == "Spawn" and obj.name != "Spawn_Player":
                monster_name = obj.name.split("_")[1].lower()
                self.enemy_list.append(Enemy(
                    monster_name,
                    (obj.x, obj.y),
                    [self.visible_sprites,self.attackable_sprites],
                    self.obstacle_sprites,
                    self.damage_player,
                    self.trigger_death_particles,
                    self.add_exp,
                    self.current_wave))
                self.enemy_count += 1
        self.spawning_wave = False
    
    def spawn_countdown(self):
        current_time = pygame.time.get_ticks()
        self.display_incoming_wave(current_time)
        if current_time - self.wave_spawn_time >= 2400:
            self.spawn_wave()
            
    def display_incoming_wave(self, current_time):
        text = f"Another Wave Incoming In: {int((current_time - self.wave_spawn_time))}"
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        text_surf = font.render(text,False,"yellow")
        text_rect = text_surf.get_rect(midtop = self.display_surface.get_rect().midtop + pygame.math.Vector2(0,200))
        self.display_surface.blit(text_surf,text_rect)
            
    def tutorial_page_countdown(self):
        pass
    
    def display_tutorial_page(self):
        pass
    
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
    
    def add_exp(self, amount):
        self.player.exp += amount
        self.score.increase_kill_count()
        self.enemy_count -= 1
    
    def toggle_menu_cooldown(self):
        if self.can_toggle: return
        current_time = pygame.time.get_ticks()
        if current_time - self.selection_time >= 300: self.can_toggle = True
        
    def toggle_menu(self):
        if not self.can_toggle: return
        self.game_paused = not self.game_paused
        self.can_toggle = False
        self.selection_time = pygame.time.get_ticks()
        
    def display_game_over(self):
        text = "Game Over!\n"
        if self.player_dead: text += "You were defeated."
        else: text += "CONGRATULATIONS!"
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        for index,line in enumerate(text.split("\n")):
            text_surf = font.render(line,False,"yellow")
            text_rect = text_surf.get_rect(midtop = self.display_surface.get_rect().midtop + pygame.math.Vector2(0,200+(index*20)))
            self.display_surface.blit(text_surf,text_rect)

    def run(self):
        if not self.game_play_lock:
            self.game_play_lock = True
            self.toggle_in_game()
        
        #self.visible_sprites.draw()
        self.map_sprites.custom_draw(self.player)
        #self.sprite_group.draw(self.display_surface)
        self.structure_sprites.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)
        self.high_structure_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]: self.toggle_menu()
        self.toggle_menu_cooldown()
        self.end_level_cooldown()
        
        self.debug_message = f"Current Score: {self.score.get_kill_count()}"
        
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
            if self.enemy_count == 0 and not self.game_over:
                if self.wave_cap is None or self.current_wave < self.wave_cap:
                    if not self.spawning_wave:
                        self.wave_spawn_time = pygame.time.get_ticks()
                        self.spawning_wave = True
                    self.spawn_countdown()
                else:
                    self.end_level(False)
        debug(self.debug_message)
            
            
        


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
