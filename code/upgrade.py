import pygame
from code.settings import *

class Upgrade:
    def __init__(self,player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        #item creation
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // (self.attribute_number + 1)
        self.create_items()
        
        #selection system
        self.selection_index = 0
        self.selection_time = 0
        self.can_move = True
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.can_move: return
        if keys[pygame.K_RIGHT]:
            self.selection_index += 1
            if self.selection_index >= self.attribute_number: self.selection_index = 0
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        elif keys[pygame.K_LEFT]:
            self.selection_index -= 1
            if self.selection_index < 0: self.selection_index = self.attribute_number - 1
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.can_move = False
            self.selection_time = pygame.time.get_ticks()
            self.item_list[self.selection_index].trigger(self.player)
            # print(f'[0 : {self.attribute_number}]')
            # print(f'Selected Index : {self.selection_index}')
            # print(f'Selected Stat : {self.attribute_names[self.selection_index]}')
            # print(f'Selected Stat Values :\nMax {self.max_values[self.selection_index]}\nValue {self.player.get_stat_value_by_index(self.selection_index)}\nCost {self.player.get_stat_cost_by_index(self.selection_index)}')
    
    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 200:
                self.can_move = True
    
    def create_items(self):
        self.item_list = []
        
        for item,index in enumerate(range(self.attribute_number)):
            #horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2
            #vertical
            top = self.display_surface.get_size()[1] * 0.1
            #create object
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)
    
    def display(self):
        self.input()
        self.selection_cooldown()
        for index,item in enumerate(self.item_list):
            #get attributes
            name = self.attribute_names[index]
            value = self.player.get_stat_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_stat_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)
        
        text = "Arrow Keys To Move, SPACE or ENTER to Select, TAB to return to the game"
        for index,line in enumerate(text.split("\n")):
            text_surf = self.font.render(line,False,"orange")
            text_rect = text_surf.get_rect(midtop = self.display_surface.get_rect().midtop + pygame.math.Vector2(0,30+(index*20)))
            self.display_surface.blit(text_surf, text_rect)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
        
        
    def display_names(self,surface,name,cost,text_color):
        #title
        title_surf = self.font.render(name,False,text_color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        #cost
        cost_surf = self.font.render(f'Cost: {int(cost)}',False,text_color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0,-20))
        #draw
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)
    
    def display_bar(self,surface,value,max_value,color):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        width = 30
        height = 10
        value_rect = pygame.Rect((top[0] - (width / 2)),bottom[1] - relative_number,width,height)
        
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)
        
    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        if player.stats[upgrade_attribute] >= player.max_stats[upgrade_attribute]: return
        if player.exp >= player.upgrade_cost[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4
        if player.stats[upgrade_attribute] >= player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]
        
    
    def display(self,surface,selection_num,name,value,max_value,cost):
        selected = True if self.index == selection_num else False
        bg_color = UPGRADE_BG_COLOR_SELECTED if selected else UI_BG_COLOR
        border_color = UI_BORDER_COLOR_ACTIVE if selected else UI_BORDER_COLOR
        text_color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        bar_color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        pygame.draw.rect(surface,bg_color,self.rect)
        pygame.draw.rect(surface,border_color,self.rect,3)
        self.display_names(surface,name,cost,text_color)
        self.display_bar(surface,value,max_value,bar_color)
        