import pygame
from code.settings import *
from code.entity import Entity
from code.support import *
from code.audio import AudioController

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player, trigger_death_particles, add_exp,current_wave = 0):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = pygame.Surface((64,64))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.obstacle_sprites = obstacle_sprites
        
        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed'] + int(3 * current_wave)
        self.attack_damage = monster_info['damage'] + int(3 * current_wave)
        self.resistance = monster_info['resistance'] + int(.5 * current_wave)
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius'] + int(30 * current_wave)
        self.attack_type = monster_info['attack_type']
        
        self.audio_controller = AudioController()
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.attack_sound.set_volume(self.audio_controller.get_total_volume('monster'))
        self.death_sound = pygame.mixer.Sound('audio\\death.wav')
        self.death_sound.set_volume(self.audio_controller.get_total_volume('monster'))
        self.hit_sound = pygame.mixer.Sound('audio\\hit.wav')
        self.hit_sound.set_volume(self.audio_controller.get_total_volume('monster'))
        
        #player interaction
        self.player_location = []
        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = 0
        self.vulnerable = True
        self.hit_time = 0
        self.hit_cooldown = 300
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
    
    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'graphics\\monsters\\{name}\\'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
    
    def get_player_location(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        delta_vec = (player_vec - enemy_vec)
        distance = delta_vec.magnitude()
        
        if distance > 0: direction = delta_vec.normalize()
        else: direction = pygame.math.Vector2()
        
        return (distance,direction)
    
    def get_status(self):
        distance = self.player_location[0]
        
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack': self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius: self.status = 'move'
        else: self.status = 'idle'
        
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.death_sound.play()
            self.add_exp(self.exp)
            self.kill()
    
    def actions(self):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.player_location[1]
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.vulnerable = True
                self.speed = self.speed / -1
    
    def get_damage(self,player,attack_type):
        if not self.vulnerable: return
        self.hit_sound.play()
        if attack_type == 'weapon':
            self.health -= player.get_full_weapon_damage()
            self.hit_cooldown = player.get_weapon_cooldown()
            self.speed = self.speed * -1
        else:
            self.health -= player.get_full_magic_damage()
            self.hit_cooldown = player.attack_cooldown
            self.speed = self.speed * -1
        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False
    
    def animate(self):
        animation = self.animations[self.status]
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        #flicker for damage
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.cooldowns()
        self.animate()
        self.attack_sound.set_volume(self.audio_controller.get_total_volume('monster'))
        self.death_sound.set_volume(self.audio_controller.get_total_volume('monster'))
        self.hit_sound.set_volume(self.audio_controller.get_total_volume('monster'))
        self.move(self.speed)

    def enemy_update(self, player):
        self.player_location = self.get_player_location(player)
        self.get_status()
        self.actions()