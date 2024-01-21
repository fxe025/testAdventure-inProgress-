import pygame
import random

class square_sprite(pygame.sprite.Sprite):
    def __init__(self, colour):
        super().__init__()
        test_surf = pygame.Surface((150,150))
        self.image = test_surf
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft = (450,200))
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
    output_enemy = globals()[enemy_chosen](enemy_colour)
    return output_enemy

