import pygame
from settings import *

class InGameMenu:
    def __init__(self, menu_items):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.menu_items = menu_items
        self.menu_item_names = list(menu_items.keys())
        self.height = self.display_surface.get_size()[1] // (len(self.menu_items) + 1)
        self.width = self.display_surface.get_size()[0] * 0.6
        self.create_menu(menu_items)
        
        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True
        
    def input(self):
        if not self.can_move: return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selection_index = (self.selection_index - 1) % len(self.menu_items)
        elif keys[pygame.K_DOWN]:
            self.selection_index = (self.selection_index + 1) % len(self.menu_items)
        if keys[pygame.K_SPACE]:# or keys[pygame.K_ENTER]:
            # print(f"[Selection Index]:{self.selection_index}")
            print(f"[Selected Item]:{self.menu_items[self.menu_item_names[self.selection_index]]}")
            self.item_list[self.selection_index].trigger(
                self.menu_items[self.menu_item_names[self.selection_index]]['function'],
                self.menu_items[self.menu_item_names[self.selection_index]]['args']
            )
        
        self.can_move = False
        self.selection_time = pygame.time.get_ticks()
    
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

    def display(self):
        self.input()
        self.selection_cooldown()
        for index,item in enumerate(self.item_list):
            name = self.menu_items[self.menu_item_names[index]]['text']
            item.display(self.display_surface,self.selection_index,name)

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
    def __init__(self):
        pass
        #create values needed to display and adjust volume settings
    
    def input(self):
        pass
        #create controls for up/down sound selector, right/left level adjustment
    
    def selection_cooldown(self):
        pass
        #same cooldown functionality as above
    
    def create_items(self):
        pass
        #create AudioMenuItems similar to as done above
    
    def display(self):
        pass
        #dispay one large menu, with each menu item appearing in vertical stack

class AudioMenuItem:
    def __init__(self,l,t,w,h,index,font):
        pass
        #create values needed to display and adjust volume setting
    
    def display_names(self,surface,name,value,text_color):
        pass
        #display volume category name and current value
    
    def display_bar(self,surface,value,color):
        pass
        #display horizontal scale bar and vertical position bar
    
    def trigger(self):
        pass
        #on right/left keypress, move vertical position bar and adjust volume settings value by 0.1(+-)
    
    def display(self,surface,selection_num,name,value):
        pass
        #display AudioMenuItem on the AudioMenu

class MessagePane:
    def __init__(self):
        pass
        #create values needed to display a wall of text_color
        
    def input(self):
        pass
        #create controls for SPACE to bring user back to main menu
    
    def display(self):
        pass
        #display a text pane with text