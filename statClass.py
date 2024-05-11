from char_stats import step, max_hp, min_hp, max_energy, min_energy, max_mana, min_mana, base_attack, base_defense
from itemList import common, uncommon, rare, epic, legendary

#Status of health and energy at home page
class status:
    def __init__(self, player_health, player_energy, player_step, player_mana, base_attack, base_defense):
        self.health = player_health
        self.energy = player_energy
        self.step = player_step
        self.mana = player_mana
        self.attack = base_attack
        self.defense = base_defense


    def update(self, player_health, player_energy, player_step, player_mana):
        self.hp = player_health
        self.energy = player_energy
        self.step = player_step
        self.mana = player_mana

class health:
    def __init__(self, min_hp, max_hp):
        self.hp = max_hp
        self.max_hp = max_hp
        self.min_hp = min_hp

    def deduct_hp(self, amount, battle = False):
        if not battle:
            self.hp -= amount
        else:
            self.hp = 50
        if self.hp < 0:
            self.hp = 0

    def recover_hp(self, amount, battle = False):
        if not battle:
            self.hp += amount
        else:
            self.hp = self.hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class energy:
    def __init__(self, min_energy, max_energy):
        self.energy = max_energy
        self.max_energy = max_energy
        self.min_energy = min_energy

    def deduct_energy(self, amount):
        self.energy -= amount
        if self.energy < self.min_energy:
            self.energy = self.min_energy

    def recover_energy(self, amount):
        self.energy += amount
        if self.energy > self.max_energy:
            self.energy = self.max_energy

class mana:
    def __init__(self, min_mana, max_mana):
        self.mana = max_mana
        self.max_mana = max_mana
        self.min_mana = min_mana

    def deduct_mana(self, amount):
        self.mana -= amount
        if self.mana < self.min_mana:
            self.mana = self.min_mana

    def recover_mana(self, amount):
        self.energy += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana

class attack:
    def __init__(self, base_attack):
        self.attack = base_attack

    def change_attack(self, amount):
        self.attack += amount
        if self.attack < 0:
            self.attack = 0

class defense:
    def __init__(self, base_defense):
        self.defense = base_defense

    def change_defense(self, amount):
        self.defense += amount
        if self.defense < 0:
            self.defense = 0

class gamestep:
    def __init__(self, step):
        self.step = step
    
    def add_step(self):
        self.step += 1

player_health = health(min_hp, max_hp)
player_energy = energy(min_energy, max_energy)
player_step = gamestep(step)
player_mana = mana(min_mana, max_mana)
player_attack = attack(base_attack)
player_defense = defense(base_defense)
player_status = status(player_health, player_energy, player_step, player_mana, base_attack, base_defense)

def use_item(item_to_use, player_status):
    search_list = [common, uncommon, rare, epic, legendary]
    if item_to_use == "Healing Herb":
        player_status.hp.recover_hp(15)
    if item_to_use == "Fruit":
        player_status.energy.recover_energy(10)
    if item_to_use == "Healing Potion":
        player_status.hp.recover_hp(50)
    if item_to_use == "Energy Potion":
        player_status.energy.recover_energy(30)
    if item_to_use == "Elf Elixir":
        player_status.hp.recover_hp(max_hp)
    if item_to_use == "Magic Potion":
        player_status.mana.recover_mana(30)