import pygame
import time

from homeSprites import last_click_time, current_click_time

def display_text(screen, to_display, coordinates):
    font_selected = pygame.font.Font(None, 30)
    text_surface = font_selected.render(to_display, True, 'Black')
    text_rect = text_surface.get_rect(topleft = coordinates)
    screen.blit(text_surface, text_rect)

def if_open_dialog(box_sprite, choice_1 = 0, choice_2 = 0, options_exist = False):
    print("function called!!!")
    player_input = box_sprite.player_input()
    print("player_input: ", player_input)
    if player_input == 1 and not options_exist:
        return False
    elif options_exist and (choice_1 == 1 or choice_2 == 1):
        return False
    else:
        return True
    
class option_sprite(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super().__init__()
        self.location = coordinates
        test_surf = pygame.Surface((100,30))
        self.image = test_surf
        self.image.fill('Brown')
        self.rect = self.image.get_rect(topleft = self.location)

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
                print('option clicked')
                return 1
            else:
                return 0
            
    def draw_sprite(self, screen, text_to_draw):
        screen.blit(self.image, self.rect)
        display_text(screen, text_to_draw, self.location)

    def update(self):
        self.player_input()

option_1 = option_sprite((800,500))
option_2 = option_sprite((800,550))

class box_sprite(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super().__init__()
        self.location = coordinates
        test_surf = pygame.Surface((750,100))
        self.image = test_surf
        self.image.fill('White')
        self.rect = self.image.get_rect(topleft = self.location)

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
                print('box clicked!!!')
                return 1
            else:
                return 0
        return 0

    def update(self):
        self.player_input()

dialog_box = box_sprite((150,500))
