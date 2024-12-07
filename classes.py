import os
import json
import tkinter as tk
from tkinter import ttk

# Line intentionall Left Blank
#Classes

class Faction:
    def __init__(self, name):
        self.name = name
        self.units = []

    def add_units(self, unit):
        self.units.append(unit)

    def list_units(self):
        return [unit.name for unit in self.units]

    def get_unit(self, unit_name):
        for unit in self.units:
            if unit.name == unit_name:
                return unit
        raise ValueError(f"unit '{unit_name}' not found in faction '{self.name}")
    
class Unit:
    def __init__(self, name, keywords, movement, toughness, save, invuln, wounds, leadership, objective_control, abilities, weapons, loadouts, default_squad):
        self.name = name
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

def update_loadout(squad, model_id, selected_loadout):
    for model in squad:
        if model["model_id"] == model_id:
            model["loadout"] = selected_loadout

def update_squad_size(event, squad, squad_size_var, unit_data):
    selected_size = int(squad_size_var.get())
    squad.clear()
    squad.extend(build_squad(selected_size, unit_data["default_squad"]["loadout"]))
    update_model_louadouts()

def update_model_loadouts():
    for widget in model_frames:
        widget.destroy()
    model_frames.clear()

    for model in squad:
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill="x", pady=5)
        model_frames.append(frame)
        
        label = ttk.Label(frame, text=f"Model {model['model_id']}:")
        label.pack(side="left")

        selected_loadout = tk.StringVar(value=model["loadout"])
        dropdown = ttk.Combobox(frame, textvariable=selected_loadout, state="readonly")
        dropdown["values"] = [loadout["name"] for loadout in unit_data["loadouts"]]
        dropdown.pack(side="left", padx=10)

        def set_model_loadout(event, model_id=model["model_id"], var=selected_loadout):
            for m in squad:
                if m["model_id"] == model_id:
                    m["loadout"] = var.get()
                    print(f"Model {model_id} loadout updated to: {var.get()}")

        dropdown.bind("<<ComboboxSelected>>", set_model_loadout)