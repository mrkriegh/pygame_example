import pygame
from settings import *
from debug import *
from audio import AudioController
from score import ScoreController

class InGameMenu:
    def __init__(self, initialize_level):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.menu_items = {
            'new_game': {
                'text': "New Game",
                'function': initialize_level,
                'args': 'tutorial'
            },
            'audio': {
                'text': "Audio",
                'function': self.toggle_sub_menu,
                'args': "audio"
            },
            'story': {
                'text': "Story",
                'function': self.toggle_sub_menu,
                'args': "story"
            },
            'quit': {
                'text': "Quit",
                'function': pygame.event.post,
                'args': pygame.event.Event(pygame.QUIT)
            }
        }
        self.menu_item_names = list(self.menu_items.keys())
        self.height = self.display_surface.get_size()[1] // (len(self.menu_items) + 1)
        self.width = self.display_surface.get_size()[0] * 0.6
        self.create_menu(self.menu_items)
        self.create_story_pane()
        self.create_audio_menu()
        self.score = ScoreController()
        
        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True
        
        self.display_sub_menu = False
        
    def input(self):
        if not self.can_move: return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selection_index = (self.selection_index - 1) % len(self.menu_items)
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        elif keys[pygame.K_DOWN]:
            self.selection_index = (self.selection_index + 1) % len(self.menu_items)
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.item_list[self.selection_index].trigger(
                self.menu_items[self.menu_item_names[self.selection_index]]['function'],
                self.menu_items[self.menu_item_names[self.selection_index]]['args']
            )
        
    
    def selection_cooldown(self):
        if self.can_move: return
        current_time = pygame.time.get_ticks()
        if current_time - self.selection_time >= 100: self.can_move = True
    
    def create_menu(self, menu_items):
        self.item_list = []
        
        for index,item in enumerate(self.menu_items):
            full_height = self.display_surface.get_size()[1]
            increment = full_height // len(self.menu_items)
            top = (index * increment) + (increment - self.height) // 2
            left = self.display_surface.get_size()[0] * 0.2
            item = VertMenuItem(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)
            
    def create_audio_menu(self):
        self.audio_menu = AudioMenu(self.toggle_sub_menu)
    
    def create_story_pane(self):
        text = "Welcome to the arena. You have been chosen to see\n just how far you can make it through wave after wave of\n opponents. You have been allowed to keep your weapons and\n your spells. Good Luck, and fight until you cannot fight\n anymore."
        self.story_pane = MessagePane(text, self.toggle_sub_menu)

    def toggle_sub_menu(self, type):
        self.display_sub_menu = not self.display_sub_menu
        self.can_move = False
        self.selection_time = pygame.time.get_ticks()
        if type == "story": self.story_pane.toggle()
        if type == "audio": self.audio_menu.toggle()
        #toggle displaying one of the submenus or the main menu

    def display(self):
        if self.display_sub_menu:
            self.story_pane.display()
            self.audio_menu.display()
        else: 
            self.input()
            self.selection_cooldown()
            for index,item in enumerate(self.item_list):
                name = self.menu_items[self.menu_item_names[index]]['text']
                item.display(self.display_surface,self.selection_index,name)
            debug(f"High Score: {self.score.get_top_kill_count()}")

class VertMenuItem:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
    
    def display_names(self,surface,name,text_color):
        title_surf = self.font.render(name,False,text_color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,60))
        surface.blit(title_surf,title_rect)
    
    def trigger(self, function, arguments):
        # print(f"[Function]:{function}")
        # print(f"[Arguments]:{arguments}")
        if arguments: function(arguments)
        else: function()
    
    def display(self,surface,selection_num,name):
        selected = True if self.index == selection_num else False
        bg_color = UPGRADE_BG_COLOR_SELECTED if selected else UI_BG_COLOR
        border_color = UI_BORDER_COLOR_ACTIVE if selected else UI_BORDER_COLOR
        text_color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        pygame.draw.rect(surface,bg_color,self.rect)
        pygame.draw.rect(surface,border_color,self.rect,3)
        self.display_names(surface,name,text_color)
        

class AudioMenu:
    def __init__(self, toggle_sub_menu):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.active = False
        self.toggle_sub_menu = toggle_sub_menu
        self.audio_controller = AudioController()
        
        self.audio_number = len(self.audio_controller.get_volume_dict())
        self.audio_names = list(self.audio_controller.get_volume_dict().keys())
        (self.width,self.height) = self.display_surface.get_size()
        self.width = self.width // (self.audio_number + 1)
        self.height *= 0.8
        self.create_items()
        
        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True
    
    def input(self):
        if not self.can_move: return
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            selected_item = self.item_list[self.selection_index].trigger(self.audio_names[self.selection_index],'up')
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        if keys[pygame.K_DOWN]:
            self.item_list[self.selection_index].trigger(self.audio_names[self.selection_index],'down')
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        if keys[pygame.K_LEFT]:
            self.selection_index = (self.selection_index - 1) % self.audio_number
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        if keys[pygame.K_RIGHT]:
            self.selection_index = (self.selection_index + 1) % self.audio_number
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        if keys[pygame.K_ESCAPE]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.toggle_sub_menu("audio")
    
    def selection_cooldown(self):
        if self.can_move: return
        current_time = pygame.time.get_ticks()
        if current_time - self.selection_time >= 200: self.can_move = True
    
    def toggle(self):
        self.active = not self.active
        self.can_move = False
        self.selection_time = pygame.time.get_ticks()
    
    def create_items(self):
        self.item_list = []
        
        for item,index in enumerate(range(self.audio_number)):
            (full_width,top) = self.display_surface.get_size()
            increment = full_width // self.audio_number
            left = (item * increment) + (increment - self.width) // 2
            top = top * 0.1
            item = AudioMenuItem(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)
    
    def display(self):
        if not self.active: return
        self.input()
        self.selection_cooldown()
        for index,item in enumerate(self.item_list):
            name = self.audio_names[index]
            value = list(self.audio_controller.get_volume_dict().values())[index]
            item.display(self.display_surface,self.selection_index,name,value)

class AudioMenuItem:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
        self.audio_controller = AudioController()
    
    def display_names(self,surface,name,value,text_color):
        #title
        title_surf = self.font.render(name,False,text_color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        #value
        value_surf = self.font.render(f'Value: {int(value * 100)}',False,text_color)
        value_rect = value_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0,-20))
        #draw
        surface.blit(title_surf,title_rect)
        surface.blit(value_surf,value_rect)
    
    def display_bar(self,surface,value,color):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        
        full_height = bottom[1] - top[1]
        relative_number = value * full_height
        width = 30
        height = 10
        value_rect = pygame.Rect((top[0] - (width / 2)),bottom[1] - relative_number,width,height)
        
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)
    
    def trigger(self,key,direction):
        if direction == "up": value = 0.1
        elif direction == "down": value = -0.1
        else: value = 0
        self.audio_controller.adjust_volume(key, value)
    
    def display(self,surface,selection_num,name,value):
        selected = True if self.index == selection_num else False
        bg_color = UPGRADE_BG_COLOR_SELECTED if selected else UI_BG_COLOR
        border_color = UI_BORDER_COLOR_ACTIVE if selected else UI_BORDER_COLOR
        text_color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        bar_color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        pygame.draw.rect(surface,bg_color,self.rect)
        pygame.draw.rect(surface,border_color,self.rect,3)
        self.display_names(surface,name,value,text_color)
        self.display_bar(surface,value,bar_color)

class MessagePane:
    def __init__(self, text, toggle_sub_menu):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.text = text.split("\n")
        self.active = False
        self.toggle_sub_menu = toggle_sub_menu
        
        (w,h) = self.display_surface.get_size()
        w *= 0.8
        h *= 0.8
        l = w * 0.1
        t = h * 0.1
        self.rect = pygame.Rect(l,t,w,h)
        
        self.selection_time = 0
        self.can_move = True
        
    def input(self):
        if not self.can_move: return
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.toggle_sub_menu("story")
    
    def selection_cooldown(self):
        if self.can_move: return
        current_time = pygame.time.get_ticks()
        if current_time - self.selection_time >= 100: self.can_move = True
    
    def toggle(self):
        self.active = not self.active
        self.can_move = False
        self.selection_time = pygame.time.get_ticks()
    
    def display(self):
        if not self.active: return
        self.input()
        self.selection_cooldown()
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,self.rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,self.rect,3)
        for index,line in enumerate(self.text):
            text_surf = self.font.render(line,False,TEXT_COLOR)
            text_rect = text_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,30 + (index * 30)))
            self.display_surface.blit(text_surf,text_rect)