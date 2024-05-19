import pygame
import time
import random

from statClass import player_health, player_mana, player_status
import char_stats
import enemies 

from allSprites import all_sprites

click_cooldown = 0.5
last_click_time = 0
current_click_time = 0

class battle_sprite(all_sprites):
    def __init__(self, name, coordinates, player_status, test_surf):
        super().__init__(coordinates, test_surf)
        self.type = name
        self.image.fill("Brown")

        #variables to update
        self.player_status = player_status
        self.player_health = player_status.health
        self.player_mana = player_status.mana

    def player_input(self, player_status):
        global current_click_time
        global last_click_time

        self.player_status = player_status
        self.player_health = player_status.health
        self.player_mana = player_status.mana

        operation = ""

        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse[0]:
            current_click_time = time.time()
            if self.rect.collidepoint(mouse_pos) and current_click_time - last_click_time >= click_cooldown:
                last_click_time = current_click_time
                if self.type == "attack":
                    operation = self.type
                elif self.type == "magic":
                    print('clicked')
                    operation = self.type
                elif self.type == "defend":
                    print('clicked') 
                    operation = self.type
                elif self.type == "escape":
                    print('clicked')
                    operation = self.type
                return (1, operation) #store if the sprite is clicked, and type of operation
        return (0, operation)
    
def attack_enemy(player_status, enemy, string_to_print):
    damage_dealt = round(player_status.attack * 0.1)
    enemy.deduct_hp(damage_dealt)
    string_to_print = "You dealt {} damage.".format(damage_dealt)
    return string_to_print
    