import random

common = {"Potions": ("Healing Herb", "Fruit"), "Gold": (10,50)}
uncommon = {"Gold": (50,90)}
rare = {"Potions": ("Healing Potion", "Energy Potion"), "Gold": (100,120)}
epic = {"Potions": ("Magic Potion", "Magic Potion")}
legendary = {"Potions": ("Elf Elixir", "Elf Elixir")}

sequence = ["None", common, uncommon, rare, epic, legendary]
rates = [0.3, 0.33, 0.19, 0.1, 0.06, 0.02]

def investigate_reward(inv_list):
    string_to_print = ""

    item_got = ""
    item_type = ""
    item_rarity = random.choices(sequence, weights = rates)[0]
    if item_rarity == "None":
        string_to_print = "You didn't find anything."
        print(string_to_print)
        return string_to_print
    else:
        item_type = random.choice(list(item_rarity.keys()))
    
    if item_type == "Gold":
        item_got = random.randint(*item_rarity[item_type])
        string_to_print = "You found {} gold.".format(item_got)
        print(string_to_print)
        inv_list.append_inventory("Gold", item_got)
        return string_to_print
    else:
        item_got = random.choice(list(item_rarity[item_type]))
        string_to_print = "You found {}.".format(item_got)
        print(string_to_print)
        inv_list.append_inventory(item_got)
        return string_to_print
