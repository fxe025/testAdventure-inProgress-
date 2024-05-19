import pygame
import time

class all_sprites(pygame.sprite.Sprite):
    def __init__(self, coordinates, surface):
        super().__init__()
        self.click_cooldown = 0.5
        self.last_click_time = 0
        self.current_click_time = 0

        self.image = surface
        self.location = coordinates
        self.rect = self.image.get_rect(topleft = self.location)

    def update_current_click_time(self):
        self.current_click_time = time.time()

    def update_last_click_time(self):
        self.last_click_time = self.current_click_time