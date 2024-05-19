import pygame
import random

from allSprites import all_sprites

class square_sprite(all_sprites):
    def __init__(self, colour, coordinates, test_surf):
        super().__init__(coordinates, test_surf)
        self.image.fill(colour)
        self.name = "Square"
        self.health = 20
        self.atk = 10

    def attack(self, player_status):
        damage_dealt = self.atk
        player_status.hp.deduct_hp(damage_dealt)

    def deduct_hp(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

enemy_list = ["square_sprite"]

def enemy_to_appear(enemy_list):
    colour_list = ["Red", "Blue", "Black", "Purple"]
    enemy_chosen = random.choice(enemy_list)
    enemy_colour = random.choice(colour_list)
    output_enemy = globals()[enemy_chosen](enemy_colour,(450,200),pygame.Surface((150,150)))
    return output_enemy

