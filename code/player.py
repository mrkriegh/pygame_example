import pygame
from settings import *
from debug import debug
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10,HITBOX_OFFSET['player'])
        #graphics setup
        self.import_player_assets()
        self.status = 'down'
        #movement
        self.obstacle_sprites = obstacle_sprites
        #action timer
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.vulnerable = True
        self.hit_time = 0
        self.hit_cooldown = 500

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.changing_weapon = False
        self.changing_weapon_time = 0
        self.changing_weapon_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.changing_magic = False
        self.changing_magic_time = 0
        self.changing_magic_cooldown = 200

        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100, 'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 1500
        self.speed = self.stats['speed']
        
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(min(VOLUME['master'],VOLUME['player_attacks']))

    def import_player_assets(self):
        character_path = "../graphics/player/"
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle': [],'left_idle': [],'up_idle': [],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)

    def input(self):
        if self.attacking: return
        keys = pygame.key.get_pressed()
        
        #move up/down
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0
        #move left/right
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        else:
            self.direction.x = 0

        #attack input
        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            self.weapon_attack_sound.play()
        #magic input
        if keys[pygame.K_LCTRL]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            style = list(magic_data.keys())[self.magic_index]
            strength = magic_data[self.magic]['strength'] + self.stats['magic']
            cost = magic_data[self.magic]['cost']
            self.create_magic(style,strength,cost)

        #change weapon input
        if keys[pygame.K_q] and not self.changing_weapon:
            self.changing_weapon = True
            self.changing_weapon_time = pygame.time.get_ticks()
            self.weapon_index = (self.weapon_index + 1) % len(weapon_data.keys())
            self.weapon = list(weapon_data.keys())[self.weapon_index]
            self.attack_cooldown = weapon_data[self.weapon]['cooldown']

        #change magic input
        if keys[pygame.K_e] and not self.changing_magic:
            self.changing_magic = True
            self.changing_magic_time = pygame.time.get_ticks()
            self.magic_index = (self.magic_index +1 ) % len(magic_data.keys())
            self.magic = list(magic_data.keys())[self.magic_index]
            self.spell_cooldown = 400
    
    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status:
                self.status = self.status.split("_")[0] + '_idle'
        if self.attacking == True:
            self.status = self.status.split("_")[0] + '_attack'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        if self.changing_weapon:
            if current_time - self.changing_weapon_time >= self.changing_weapon_cooldown:
                self.changing_weapon = False
        if self.changing_magic:
            if current_time - self.changing_magic_time >= self.changing_magic_cooldown:
                self.changing_magic = False
        if not self.vulnerable:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.vulnerable = True

    def get_full_weapon_damage(self):
        return self.stats['attack'] + weapon_data[self.weapon]['damage']

    def get_full_magic_damage(self):
        return self.stats['magic'] + magic_data[self.magic]['strength']

    def get_weapon_cooldown(self):
        return weapon_data[self.weapon]['cooldown']


    def get_stat_value_by_index(self, index):
        return list(self.stats.values())[index]
        
    def get_stat_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]


    def animate(self):
        animation = self.animations[self.status]
        
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
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

    def energy_recovery(self):
        if self.energy == self.stats['energy']:return
        self.energy += 0.01 * self.stats['magic']
        if self.energy > self.stats['energy']:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.weapon_attack_sound.set_volume(min(VOLUME['master'],VOLUME['player_attacks']))
        self.move(self.stats['speed'])
        #debug(self.status)
        self.energy_recovery()