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
    def __init__(self, unit_name, keywords, movement, toughness, save, invuln, wounds, leadership, objective_control, fnp, abilities, weapons, loadouts, default_squad):
        self.name = unit_name
        self.keywords = keywords
        self.movement = movement
        self.toughness = toughness
        self.save = save
        self.invuln = invuln
        self.wounds = wounds
        self.leadership = leadership
        self.oc = objective_control
        self.fnp = fnp
        self.abilities = abilities
        self.weapons = [Weapon(**weapon) for weapon in weapons]
        self.loadouts = [Loadout(**loadout) for loadout in loadouts]
        self.default_squad = SquadConfig(**default_squad)
        self.selected_weapon = []

    def clear_selected(self):
        self.selected_weapon.clear()

class Weapon:
    def __init__(self, name, attacks, skill, range_, type_, strength, ap, damage, quantity=1):
        self.name = name
        self.attacks = attacks
        self.skill = skill
        self.range = range_
        self.keywords = type_
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
    return [random.randint(1,6) for _ in range(qty)]

def roll_d3(qty=1):
    return [random.randint(1,3) for _ in range(qty)]

def ensure_list(val):
    return val if isinstance(val, list) else [val]

def parse_dice(value):
    value = value.upper()
    if value.isdigit():
        return int(value)
    
    if 'D' in value:
        parts = value.split('D')
        num_dice = int(parts[0]) if parts[0] else 1

        if '+' in parts[1]:
            dice_part, modifier = parts[1].split('+')
            modifier = int(modifier)
        else:
            dice_part, modifier = parts[1], 0
        
        dice_type = int(dice_part)

        if dice_type == 6:
            return sum(ensure_list(roll_d6(num_dice))) + modifier
        elif dice_type == 3: 
            return sum(ensure_list(roll_d3(num_dice))) + modifier
        else:
            raise ValueError(f"Unsupported dice type: d{dice_type}")
    
    raise ValueError(f"Invalid dice notation: {value}")

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
    #planned update to squad inc to not reset squad to default loadouts, not yet implemented, do not use
    pass

def squad_pop(squad, qty=1):
    #planned update to squadn dec to not reset squad to default loadouts, not yet implemented, do not use
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
    if isinstance(weapon_name, Weapon):
        return weapon_name
    for weapon in unit.weapons:
        if weapon.name == weapon_name:
            return weapon
    return None

def get_loadout(unit, loadout_name):
    for loadout in unit.loadouts:
        if loadout.name == loadout_name:
            return loadout
    return None  

def convert_data(id, unit, loadout):
    return {"id": id, "unit": unit, "loadout": loadout}

def build_full_loadout(unit_name, faction, loadout_name):
    unit = faction.get_unit(unit_name)
    loadout = get_loadout(unit, loadout_name)
    for i in range(len(loadout.weapons)):
        weapon_ref = loadout.weapons[i]
        if isinstance(weapon_ref, str):
            weapon_obj = get_weapon_stats(unit, loadout.weapons[i])
            if weapon_obj is None:
                print(f"[ERROR] Could not find weapon stats for '{weapon_ref}' in unit '{unit.name}")
            loadout.weapons[i] = weapon_obj
       
    return loadout

def select_ranged(range, loadout):
    raw, pistols, non, valid = [], [], [], []
    for weapon in loadout.weapons:
        if weapon.range == 0:
            continue
        elif weapon.range >= range:
            raw.append(weapon)
    pistols = [weapon for weapon in raw if "Pistol" in weapon.keywords]
    non = [weapon for weapon in raw if "Pistol" not in weapon.keywords]
    if range == 0 and pistols:
        return pistols.copy()
    elif range == 0 and not pistols:
        return None
    if non and range > 0:
        valid = non.copy()
    if not valid and pistols:
        valid = pistols.copy()
    return valid if valid else None

def select_melee(range, loadout):
    if range > 0:
        return None
    valid, extra = [], []
    melee = [weapon for weapon in loadout.weapons if weapon.range == 0]
    if len(melee) == 1: 
        return melee
    for weapon in melee:
        if "Extra Attacks" in weapon.keywords:
            extra.append(weapon)
        elif not valid:
            valid.append(weapon)
        elif int(weapon.attacks) > int(valid[0].attacks):
            valid[0] = weapon
    return valid + extra if valid else None

def determine_wound_threshold(weapon, target):
    if weapon.strength >= (2 * target.toughness):
        return 2  # Wound on 2+
    elif weapon.strength > target.toughness:
        return 3  # Wound on 3+
    elif weapon.strength == target.toughness:
        return 4  # Wound on 4+
    elif weapon.strength < target.toughness:
        return 5  # Wound on 5+
    else:
        return 6  # Wound on 6+ (S is half or less of T)



def twin_linked(wound_rolls, goal, crit):
    result = []
    for roll in wound_rolls:
        if isinstance(roll, list):
            roll = roll[0]
        if roll >= goal or roll >= crit:
            result.append(roll)
        else:
            new_roll = roll_d6()[0]
            result.append(new_roll)
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

def dev_wounds(weapon, rolls, crit):
    mortal_wounds = []
    if not rolls:
        return []
    for dice in rolls:
        if dice == 6 or dice >= crit:
            if isinstance(weapon.damage, int) or weapon.damage.isdigit():
                mortal_wounds.append(int(weapon.damage))
            elif isinstance(weapon.damage, str) and 'D' in weapon.damage.upper():
                dam_split = weapon.damage.upper().split("+")
                mod = int(dam_split[1]) if len(dam_split) > 1 else 0
                dice_count = dam_split[0].split('D')
                num_dice = int(dice_count[0]) if dice_count[0] else 1
                dice_type = int(dice_count[1])
                if dice_type == 3:
                    dam_roll = sum(roll_d3(num_dice)) + mod
                elif dice_type == 6:
                    dam_roll = sum(roll_d6(num_dice)) + mod
                else:
                    raise ValueError(f"Unsupported dice type: d{dice_type}")
                mortal_wounds.append(dam_roll)
    return mortal_wounds

def extract_weapon_keywords(weapon):
    pass

def melta_damage(weapon, range):
    if range < (weapon.range // 2):
        melta_kw = [kw for kw in weapon.keywords if "Melta" in kw]
        if melta_kw:
            kw_list = melta_kw[0].split()
            melta_val = int(kw_list[1])
            return melta_val + weapon.damage
        return weapon.damage

def torrent(weapon):
    attacks = weapon.attacks
    if "+" in attacks:
        mod_split = attacks.split("+")
        base_part = mod_split[0]
        mod = int(mod_split[1])
    else:
        base_part = attacks
        mod = 0
    dice_count = int(base_part[0])
    return sum(roll_d6(dice_count)) + mod

def detect_hits(rolls, skill, weapon, moved, was_indirect, stealth):
    if not rolls:
        return []
    hit_threshold = skill
    if "Heavy" in weapon.keywords and not moved:
        hit_threshold = max(2, hit_threshold - 1)
    if "Indirect" in weapon.keywords and was_indirect:
        hit_threshold = max(4, hit_threshold + 1)
    if stealth and not ("Indirect" in weapon.keywords and was_indirect):
        hit_threshold += 1
#make seperate helper function for melee????? this one is loaded with ranged keywords and im not sure i want to add more....
    return [roll for roll in rolls if roll >= hit_threshold]

def detect_wounds(rolls, threshold, crit):
    if not rolls or not threshold or not crit:
        raise ValueError("something wasn't provided to detect_wounds")
    result = []
    for roll in rolls: 
        if roll >= threshold or roll >= crit: 
            result.append(roll)
    return result

def calculate_damage(wounds, weapon):
    damage = []
    for _ in wounds:
        if isinstance(weapon.damage, int) or weapon.damage.isdigit():
            damage.append(int(weapon.damage))
        elif isinstance(weapon.damage, str) and 'D' in weapon.damage.upper():
            dam_split = weapon.damage.upper().split("+")
            mod = int(dam_split[1]) if len(dam_split) > 1 else 0
            dice_split = dam_split[0].split('D')
            num_dice = int(dice_split[0]) if dice_split[0] else 1
            dice_type = int(dice_split[1])
            if dice_type == 3:
                dam_roll = sum(roll_d3(num_dice)) + mod
            elif dice_type == 6:
                dam_roll = sum(roll_d6(num_dice)) + mod
            else:
                raise ValueError(f"Unsupported dice type: d{dice_type}")
            damage.append(dam_roll)
    return damage

def save(attacks, weapon, defender, cover):
    final_attacks = []
    if cover and ((defender.save > 3) or weapon.ap > 0):
        cov_bonus = 1
    else:
        cov_bonus = 0
    if defender.invuln and defender.invuln < (defender.save + weapon.ap - cov_bonus):
            effective_save = defender.invuln
    else:
            effective_save = (defender.save + weapon.ap) - cov_bonus
    for attack in attacks:
        defense = roll_d6()
        if defense[0] < effective_save:
            final_attacks.append(attack)
    return final_attacks

def feel_no_pain(dam_list, FNP):
    final_damage = []
    for damage in dam_list:
        dam_val = damage
        for _ in range(damage):
            if roll_d6() >= FNP:
                dam_val = max(0, dam_val - 1)
        if dam_val > 0:
            final_damage.append(dam_val)
    return final_damage

