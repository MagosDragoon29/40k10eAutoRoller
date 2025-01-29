import os
import json
import random
import tkinter as tk
from tkinter import ttk

# Line intentionall Left Blank
#Classes

class Faction:
    def __init__(self, name):
        self.name = name
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit)

    def list_units(self):
        return [unit.name for unit in self.units]

    def get_unit(self, unit_name):
        for unit in self.units:
            if unit.name == unit_name:
                return unit
        raise ValueError(f"unit '{unit_name}' not found in faction '{self.name}")
    
class Unit:
    def __init__(self, unit_name, keywords, movement, toughness, save, invuln, wounds, leadership, objective_control, abilities, weapons, loadouts, default_squad):
        self.name = unit_name
        self.keywords = keywords
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.invuln = invuln
        self.wounds = wounds
        self.leadership = leadership
        self.oc = objective_control
        self.abilities = abilities
        self.weapons = [Weapon(**weapon) for weapon in weapons]
        self.loadouts = [Loadout(**loadout) for loadout in loadouts]
        self.default_squad = SquadConfig(**default_squad)
        self.selected_weapon = []

class Weapon:
    def __init__(self, name, attacks, skill, range_, type_, strength, ap, damage, quantity=1):
        self.name = name
        self.attacks = attacks
        self.skill = skill
        self.range = range_
        self.type = type_
        self.strength = strength
        self.ap = ap
        self.damage = damage
        self.quantity = quantity

class Squad:
    def __init__(self, name):
        self.name = name
        self.models = []

    def add_model(self, model):
        self.models.append(model)

    def total_models(self):
        return len(self.models)
    
class Loadout:
    def __init__(self, name, description, weapons, equipment=[], additional_abilities=[]):
        self.name = name
        self.description = description
        self.weapons = weapons
        self.equipment = equipment
        self.additional_abilities = additional_abilities
        
    def __str__(self):
        return f"Loadout: {self.name} with weapons {', '.join(self.weapons)}"
    
class SquadConfig:
    def __init__(self, models, loadout, sizes):
        self.models = models
        self.loadout = loadout
        self.sizes = sizes

    def is_valid_size(self, size):
        return size in self.sizes
    
    def __str__(self):
        return f"Default squad of {self.models} models, using {self.loadout}, allowed sizes: {self.sizes}"

#Functions

def roll_d6(qty=1):
    if qty == 1:
        return random.randint(1, 6)
    return [random.randint(1,6) for _ in range(qty)]

def roll_d3(qty=1):
    if qty == 1:
        return random.randint(1,3)
    return [random.randint(1,3) for _ in range(qty)]

def load_factions(folder_path):
    factions = {}
    for faction_name in os.listdir(folder_path):
        faction_path = os.path.join(folder_path, faction_name)
        if os.path.isdir(faction_path):
            faction = Faction(name=faction_name)
            for unit_file in os.listdir(faction_path):
                if unit_file.endswith(".json"):
                    with open(os.path.join(faction_path, unit_file), "r") as file:
                              unit_data = json.load(file)
                              unit = Unit(**unit_data)
                              faction.add_unit(unit)
            factions[faction_name] = faction
    return factions

def build_squad(size, default_loadout):
    return [{"model_id": i, "loadout": default_loadout} for i in range(1, size+1)]

def rebuild_squad(squad, size, default_loadout, frames, loadout_frame, unit, alignment, column):
    squad.clear()
    squad.extend(build_squad(size, default_loadout))
    update_model_loadouts(squad, frames, loadout_frame, unit, alignment=alignment, column=column)

def set_model_loadout(model, new_loadout):
    model["loadout"] = new_loadout
    print(f"Model {model['model_id']} loadout updated to: {new_loadout}")

def update_model_loadouts(squad, frames, loadout_frame, unit, alignment="left", column=0):
    for widget in frames:
        widget.destroy()
    frames.clear()

    for row, model in enumerate(squad):
        frame = ttk.Frame(loadout_frame, padding="5")
        frame.grid(row=row + 1, column=column, sticky="ew", pady=2)
        frames.append(frame)
        
        label = ttk.Label(frame, text=f"Model {model['model_id']}:")
        label.grid(row=0, column=0, sticky=alignment)

        selected_loadout = tk.StringVar(value=model["loadout"])
        dropdown = ttk.Combobox(frame, textvariable=selected_loadout, state="readonly")
        dropdown["values"] = [loadout.name for loadout in unit.loadouts]
        dropdown.grid(row=0, column=1, padx=10)

        

        dropdown.bind("<<ComboboxSelected>>", lambda event, m=model, var=selected_loadout: set_model_loadout(m, var.get()))

def squad_append(squad, default):
    #planned update to squad inc to not reset squad to default loadouts
    pass

def squad_pop(squad, qty=1):
    #planned update to squadn dec to not reset squad to default loadouts
    pass

def update_squad_size(squad_var, delta, max_size):
    new_size = int(squad_var.get()) + delta
    new_size = max(1, min(new_size, max_size))
    squad_var.set(new_size)
    return new_size

def get_max_size(unit):
    return max(unit.default_squad.sizes)

def get_min_size(unit):
    return min(unit.default_squad.sizes)

def get_blast(target_squad):
    if not target_squad:
        return 0
    return len(target_squad) // 5

def get_weapon_stats(unit, weapon_name):
    for weapon in unit.weapons:
        if weapon.name == weapon_name:
            return weapon
    return None

def get_loadout(unit, loadout_name):
    for loadout in unit.loadouts:
        if loadout.name == loadout_name:
            return loadout
    return None  

def select_ranged(unit, range):
    pass

def select_melee(unit):
    pass

def twin_linked(wound_rolls, goal):
    result = []
    for roll in wound_rolls:
        if roll >= goal:
            result.append(roll)
        else:
            result.append(roll_d6())
    return result
    

def sustained_hits(shots, keyword, crit=6):
    kw_split = keyword.split()
    sustained = 0
    if kw_split[2].isdigit():
        value = int(kw_split[2])
        for hit in shots:
            if hit == crit:
                sustained += value
    else:
        if kw_split[2] == "d3":
            for hit in shots:
                if hit == crit:
                    sustained += roll_d3()
    return sustained

def lethal_hits(shots, crit=6):
    lethal = 0
    for hit in shots:
        if hit == crit:
            lethal += 1
    return lethal

def dev_wounds():
    pass

def weapon_keywords():
    pass

def melta_damage(weapon, range):
    if range < (weapon.range // 2):
        melta_kw = [kw for kw in weapon.type if "Melta" in kw]
        if melta_kw:
            kw_list = melta_kw[0].split()
            melta_val = int(kw_list[1])
            return melta_val + weapon.damage
        return weapon.damage

