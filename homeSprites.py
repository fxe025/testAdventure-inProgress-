import pygame
from sys import exit
from random import randint, choice
import pickle
import time

import itemList
from statClass import player_mana

click_cooldown = 0.5
last_click_time = 0
current_click_time = 0

#inventory system
class inventory:
    def __init__(self):
        self.inventory_list = []
        self.max_capacity = 20
        self.gold = 0
        self.size = 0

    def append_inventory(self, item, gold_amt = 0):
        self.gold += gold_amt
        if self.size < self.max_capacity:
            if item != "Gold":
                self.inventory_list.append(item)
                self.size += 1
                sort_inventory(self.inventory_list)
        print("Gold: {}".format(self.gold))
        print(self.inventory_list)
        print("Number of items: {}".format(self.size))

class slot_sprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, text):
        super().__init__()
        self.location = coordinates
        test_surf = pygame.Surface((250,30))
        self.image = test_surf
        self.image.fill('Pink')
        self.rect = self.image.get_rect(topleft = self.location)
        self.item_name = text

    def player_input(self):
        global current_click_time
        global last_click_time
        if_use_item = (False, "") #store whether item is used and item's name
        click_cooldown = 0.5
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse[0]:
            current_click_time = time.time()
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown:
                last_click_time = current_click_time
                if_use_item = (True, self.item_name)
                print('clicked. use item!')
                print(if_use_item)
        return if_use_item

    def update(self, screen):
        self.draw_text(screen)
        return self.player_input() 

    def draw_text(self, screen):
        font_selected = pygame.font.Font(None, 30)
        text_surface = font_selected.render(self.item_name, True, 'Black')
        text_rect = text_surface.get_rect(topleft = self.location)
        screen.blit(text_surface, text_rect)

class menu_button_sprite(pygame.sprite.Sprite):
    def __init__(self, coordinates, width, height):
        super().__init__()
        self.location = coordinates
        test_surf = pygame.Surface((width,height), pygame.SRCALPHA)
        self.image = test_surf
        self.rect = self.image.get_rect(topleft = self.location)
    
    def fill_colour(self):
        self.image.fill('Red')

    def draw_triangle(self, vertices):
        pygame.draw.polygon(self.image, "Pink", vertices)

    def player_input(self):
        global current_click_time
        global last_click_time
        click_cooldown = 0.5
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse[0]:
            current_click_time = time.time()
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown:
                last_click_time = current_click_time
                print('clicked')
                return 1

    def update(self, screen):
        screen.blit(self.image,self.rect)
        return self.player_input()

previous_page = menu_button_sprite((300,460),30,30)
next_page = menu_button_sprite((650,460),30,30)
close_menu = menu_button_sprite((760,50),40,40)

def add_inventory(item_list, sprites_1, sprites_2):
    (x,y) = (240,100) #topleft/first item location
    row = 0
    for i in range(len(item_list)):
        row = int(i/2)
        if i >= 10:
            row = int((i-10)/2)
        y = 100 + row * 50
        if i % 2 == 0:
            x = 240
        else:
            x = 510
        if i < 10:
            sprites_1.add(slot_sprite((x,y), item_list[i]))
        else:
            sprites_2.add(slot_sprite((x,y), item_list[i]))

def sort_inventory(item_list):
    size = len(item_list)
    if size > 1:
        mid = size // 2
        left_half = item_list[:mid]
        right_half = item_list[mid:]
        sort_inventory(left_half)
        sort_inventory(right_half)
        m = 0
        n = 0
        k = 0
        while m < len(left_half) and n < len(right_half):
            if left_half[m][0] < right_half[n][0]:
                item_list[k] = left_half[m]
                k += 1
                m += 1
            else:
                item_list[k] = right_half[n]
                k += 1
                n += 1
        while m < len(left_half):
            item_list[k] = left_half[m]
            k += 1
            m += 1
        while n < len(right_half):
            item_list[k] = right_half[n]
            k += 1
            n += 1

inv_list = inventory()
menu_sprites_1 = pygame.sprite.Group()
menu_sprites_2 = pygame.sprite.Group()

# 4 sprites to interact at home page     
class interaction_sprite(pygame.sprite.Sprite):
    def __init__(self, name, colour, location, player_status):
        super().__init__()
        test_surf = pygame.Surface((100,30))
        self.type = name
        self.image = test_surf
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft = location)

        #variables to update
        self.player_status = player_status
        self.player_energy = player_status.energy
        self.player_health = player_status.health
        self.player_step = player_status.step

    def player_input(self, player_status, inv_list, menu_sprites_1, menu_sprites_2):
        global current_click_time
        global last_click_time

        self.player_status = player_status
        self.player_energy = player_status.energy
        self.player_health = player_status.health
        self.player_step = player_status.step

        string_to_print = ""

        energy = self.player_energy.energy
        energy_spent = 10
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse[0]:
            current_click_time = time.time()
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown and \
            energy >= energy_spent:
                if self.type == "investigate":
                    last_click_time = current_click_time
                    if inv_list.size < inv_list.max_capacity:
                        string_to_print = itemList.investigate_reward(inv_list)
                        self.player_energy.deduct_energy(energy_spent)
                        menu_sprites_1.empty()
                        menu_sprites_2.empty()
                        add_inventory(inv_list.inventory_list, menu_sprites_1, menu_sprites_2)
                    else:
                        string_to_print = "Your backpack is full!"
                        print(string_to_print)
                    print('clicked')
                    print('hp', self.player_health.hp)
                    print('energy', self.player_energy.energy)
                    print('step', self.player_status.step)
                    return (1, string_to_print) #returns if the sprite is clicked, and string to blit
                elif self.type == "heal":
                    last_click_time = current_click_time
                    self.player_health.recover_hp(50)
                    self.player_energy.deduct_energy(energy_spent)
                    print('clicked')
                    print('hp', self.player_health.hp)
                    print('energy', self.player_energy.energy)
                    print('step', self.player_status.step)
                    string_to_print = "You get healed."
                    return (1, string_to_print)
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown and \
            self.type == "rest":
                    last_click_time = current_click_time
                    energy_recovered = 30
                    self.player_energy.recover_energy(energy_recovered)
                    print('clicked') 
                    print('hp', self.player_health.hp)
                    print('energy', self.player_energy.energy)
                    print('step', self.player_step.step)
                    string_to_print = "You recovered some energy."
                    return (1, string_to_print)
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown and \
            self.type == "proceed":
                self.player_step.add_step()
                last_click_time = current_click_time
                print('clicked')
                print('hp', self.player_health.hp)
                print('energy', self.player_energy.energy)
                print('step', self.player_step.step)
                return 1
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown and \
            energy < energy_spent:
                last_click_time = current_click_time
                string_to_print = "energy not enough"
                print(string_to_print)
                return (1, string_to_print)
        return (0, string_to_print)
    
    def return_status(self):
        self.player_status.update(self.player_health, self.player_energy, self.player_step, player_mana)
        return self.player_status

#inventory sprite
class openInventory_sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        test_surf = pygame.Surface((100,30))
        self.image = test_surf
        self.image.fill('Brown')
        self.rect = self.image.get_rect(topleft = (800,50))

    def player_input(self):
        global current_click_time
        global last_click_time
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse[0]:
            current_click_time = time.time()
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown:
                last_click_time = current_click_time
                print('clicked')
                return 1