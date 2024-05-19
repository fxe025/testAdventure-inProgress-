#this is a new command test git
import pygame
from sys import exit
import random
import pickle
import time

from statClass import player_status

from homeSprites import interaction_sprite, openInventory_sprite
from homeSprites import menu_sprites_1, menu_sprites_2, inv_list
from homeSprites import previous_page, next_page, close_menu
from homeSprites import add_inventory

from battleSprites import battle_sprite
from battleSprites import attack_enemy

from dialogbox import dialog_box, option_1, option_2
from dialogbox import display_text, if_open_dialog

from statClass import use_item

from enemies import enemy_list, enemy_to_appear

from itemList import investigate_reward

pygame.init()

original_resolution = (1000,600)
display_info = pygame.display.Info()
fullscreen_resolution = (display_info.current_w,display_info.current_h)
screen = pygame.display.set_mode(original_resolution)
#test_surface = pygame.image.load('cross-tabs-summary-screenshot.png').convert()
test_surface = pygame.Surface(original_resolution)
test_surface.fill("Bisque")
clock = pygame.time.Clock()

interactions = pygame.sprite.Group()
home_display = [("investigate", "Red", (200,500)), ("heal", "Blue", (700,500)),  \
                ("rest", "Yellow", (200,550)), ("proceed", "Green", (700,550))]

battle_sprites = pygame.sprite.Group()
battle_display = [("attack", (200,500)), ("defend", (700,500)), ("magic", (200,550)), \
                  ("escape", (700,550))]

for (home_action, home_colour, home_location), (battle_action, battle_location) in \
    zip(home_display, battle_display):
    interactions.add(interaction_sprite(name=home_action, colour=home_colour, coordinates=home_location, player_status=player_status, test_surf=pygame.Surface((100,30))))
    battle_sprites.add(battle_sprite(battle_action, battle_location, player_status))


inventory_sprite = openInventory_sprite((800,50), pygame.Surface((100,30)))

menu_surface = pygame.Surface((600,450))
menu_surface.fill("Purple")

print('hp', player_status.health.hp)
print('energy', player_status.energy.energy)
print('step', player_status.step.step)    

game_state = {"running": True, "game_active": True, \
              "open_dialog": False, "has_options": False, \
              "battle_starts": False, "player_turn": True, \
              "open_menu": False, "is_first_page": True}

item_to_use = ""
string_to_print = ""
home_options = [("Investigate", (210,510)), ("Heal", (710,510)), ("Rest", (210,560)),  \
                ("Proceed", (710,560)), ("Inventory", (810,60))]
while game_state["running"]:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                screen = pygame.display.set_mode((original_resolution))
            elif event.key == pygame.K_f:
                screen = pygame.display.set_mode(fullscreen_resolution)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game_state["game_active"] = player_status.health.hp != 0

    if game_state["game_active"]:
        screen.blit(test_surface,(0,0))

        #player_status.update()
        health_string = "Health: {}".format(player_status.health.hp)
        energy_string = "Energy: {}".format(player_status.energy.energy)
        mana_string = "Mana: {}".format(player_status.mana.mana)
        step_string = "Step: {}".format(player_status.step.step)
        strings = [health_string, energy_string, mana_string, step_string]
        locations = [(20,20), (20,50), (20,80), (20,110)]
        for string, location in zip(strings, locations):
            display_text(screen, string, location)

        if_use_item = (False, "") #store whether an item is used, and item's name

        if game_state["open_menu"]:
            screen.blit(inventory_sprite.image, inventory_sprite.rect)
            interactions.draw(screen)
            for action, location in home_options:
                display_text(screen, action, location)
            screen.blit(menu_surface,(200,50))
            gold_string = "Gold: {}".format(inv_list.gold)
            display_text(screen, gold_string, (220,430))
            previous_page.draw_triangle([(0,15),(30,0),(30,30)])
            next_page.draw_triangle([(30,15),(0,0),(0,30)])
            close_menu.fill_colour()
            buttons = [previous_page, next_page, close_menu]
            if game_state["open_dialog"] and game_state["has_options"]:
                for button in buttons:
                    screen.blit(button.image, button.rect)
                if game_state["is_first_page"]:
                    menu_sprites_1.draw(screen)
                    for sprite in menu_sprites_1:
                        sprite.draw_text(screen)
                else:
                    menu_sprites_2.draw(screen)
                    for sprite in menu_sprites_2:
                        sprite.draw_text(screen)
                screen.blit(dialog_box.image, dialog_box.rect)
                option_1.draw_sprite(screen, "Yes")
                option_2.draw_sprite(screen, "No")
                display_text(screen, 'Use "' + item_to_use + '"?', (160,510))
                choice_1 = option_1.player_input()
                choice_2 = option_2.player_input()
                if choice_1 == 1:
                    use_item(item_to_use, player_status)
                    inv_list.inventory_list.remove(item_to_use)
                    menu_sprites_1.empty()
                    menu_sprites_2.empty()
                    add_inventory(inv_list.inventory_list, menu_sprites_1, menu_sprites_2)
                game_state["open_dialog"] = if_open_dialog(dialog_box, choice_1, choice_2, True)
            else:
                if game_state["is_first_page"]:
                    menu_sprites_1.draw(screen)
                    for sprite in menu_sprites_1:
                        temp = sprite.update(screen) #returns player input
                        if temp[0]:
                            if_use_item = temp
                else:
                    menu_sprites_2.draw(screen)
                    for sprite in menu_sprites_2:
                        temp = sprite.update(screen) #returns player input
                        if temp[0]:
                            if_use_item = temp

            if if_use_item[0]:
                game_state["open_dialog"] = True
                game_state["has_options"] = True
                item_to_use = if_use_item[1]
            if previous_page.update(screen) == 1:
                game_state["is_first_page"] = True
            if next_page.update(screen) == 1:
                game_state["is_first_page"] = False
            game_state["open_menu"] = close_menu.update(screen) != 1
        else:
            screen.blit(inventory_sprite.image, inventory_sprite.rect)
            display_text(screen, "Inventory", (810,60))
            open_inventory = inventory_sprite.player_input()
            if game_state["battle_starts"]:
                screen.blit(enemy_appeared.image, enemy_appeared.rect)
                if game_state["open_dialog"]:
                    screen.blit(dialog_box.image, dialog_box.rect)
                    display_text(screen, string_to_print, (160,510))
                    game_state["open_dialog"] = if_open_dialog(dialog_box)
                    if not game_state["open_dialog"]:
                        pygame.time.delay(100)
                else:
                    battle_sprites.draw(screen)
                    to_print = [("Attack", (210,510)), ("Defend", (710,510)), ("Magic", (210,560)), \
                                ("Escape", (710,560))]
                    for action, location in to_print:
                        display_text(screen, action, location)
                    if not game_state["player_turn"]:
                        print("enemy attacks!")
                        enemy_appeared.attack(player_status)
                        game_state["player_turn"] = True
                    else:
                        for sprite in battle_sprites:
                            temp = sprite.player_input(player_status)
                            if temp[0] == 1:
                                if temp[1] == "attack":
                                    string_to_print = attack_enemy(player_status, enemy_appeared, string_to_print)
                                if temp[1] == "escape":
                                    game_state["battle_starts"] = False if random.random() <= 0.2 else True
                                    string_to_print = "You attempted to escape, but failed." if game_state["battle_starts"] \
                                    else "You escaped."
                                game_state["open_dialog"] = True
                                game_state["player_turn"] = False
                                pygame.time.delay(100)
                                break
                game_state["open_menu"] = open_inventory == 1
                if enemy_appeared.health == 0:
                    game_state["battle_starts"] = False
                    game_state["open_dialog"]
                    reward_string = investigate_reward(inv_list)
                    menu_sprites_1.empty()
                    menu_sprites_2.empty()
                    add_inventory(inv_list.inventory_list, menu_sprites_1, menu_sprites_2)
                    string_to_print = "you win!\n" + reward_string
                    print(string_to_print)
                    del enemy_appeared

            else:
                if game_state["open_dialog"]:
                    screen.blit(dialog_box.image, dialog_box.rect)
                    display_text(screen, string_to_print, (160,510))
                    game_state["open_dialog"] = if_open_dialog(dialog_box)
                    if not game_state["open_dialog"]:
                        pygame.time.delay(100)
                else:
                    interactions.draw(screen)
                    for action, location in home_options:
                        display_text(screen, action, location)
                    for sprite in interactions:
                        temp = sprite.player_input(player_status, inv_list, menu_sprites_1, menu_sprites_2)
                        if type(temp) is tuple and temp[0] == 1:
                            print(temp)
                            game_state["open_dialog"] = True
                            game_state["has_options"] = False
                            print("Condition met", sprite.player_energy.energy)
                            string_to_print = temp[1]
                            print("String to print: ", string_to_print)
                            pygame.time.delay(200)
                        elif temp == 1 and random.random() <= 0.3:
                            game_state["battle_starts"] = True
                            game_state["open_dialog"] = True
                            game_state["has_options"] = False
                            enemy_appeared = enemy_to_appear(enemy_list)
                            string_to_print = "{} appears!".format(enemy_appeared.name)
                            pygame.time.delay(200)
                        player_status = sprite.return_status()
                game_state["open_menu"] = open_inventory == 1
                game_state["is_first_page"] = True if game_state["open_menu"] else False

    else:
        screen.fill('Grey')

    pygame.display.update()
    clock.tick(60)
    
