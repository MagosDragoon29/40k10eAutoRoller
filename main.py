import tkinter as tk
from tkinter import ttk
import json

from classes import *

#Line Intentionally Left Blank

#Load Factions
faction_folder = "FACTIONS"
factions = load_factions(faction_folder)

#initialize gui
root = tk.Tk()
root.title("Squad Builder")

# Selectable Variables
a_selected_faction = tk.StringVar()
a_selected_unit = tk.StringVar()
d_selected_faction = tk.StringVar()
d_selected_unit = tk.StringVar()

# faction/unit frame
selection_frame = ttk.Frame(root, padding="10")
selection_frame.pack(fill="x", pady=5)


#faction dropdown
attacker_label = ttk.Label(selection_frame, text="Select Attacker Faction:")
attacker_label.pack(side="left", padx=5)
attacker_dropdown = ttk.Combobox(selection_frame, textvariable=a_selected_faction, state="readonly")
attacker_dropdown["values"] = list(factions.keys())
attacker_dropdown.pack(side="left", padx=5)
defender_label = ttk.Label(selection_frame, text="Select Defender Faction:")
defender_label.pack(side="right",padx=5)
defender_dropdown = ttk.Combobox(selection_frame,textvariable=d_selected_faction, state="readonly")
defender_dropdown["values"] = list(factions.keys())
defender_dropdown.pack(side="right", padx=5)

#unit dropdown
a_unit_label = ttk.Label(selection_frame, text="Select Attacking Unit:")
a_unit_label.pack(side="left", padx=5)
a_unit_dropdown = ttk.Combobox(selection_frame, textvariable=a_selected_unit, state="readonly")
a_unit_dropdown.pack(side="left", padx=5)

d_unit_label = ttk.Label(selection_frame, text="select Defending Unit:")
d_unit_label.pack(side="right", padx=5)
d_unit_dropdown = ttk.Combobox(selection_frame, textvariable=d_selected_unit, state="readonly")
d_unit_dropdown.pack(side="right", padx=5)

#squad data
a_squad = []
d_squad = []
attacker_frames = []
defender_frames = []

#update dropdown when faction is selected
def update_attacker_unit_dropdown(event):
    faction_name = a_selected_faction.get()
    if faction_name in factions:
        faction = factions[faction_name]
        a_unit_dropdown["values"] = faction.list_units()
        a_unit_dropdown.set("")
        a_selected_unit.set("")
        clear_squad_display()

def update_defender_unit_dropdown(event):
    faction_name = d_selected_faction.get()
    if faction_name in factions:
        faction = factions[faction_name]
        d_unit_dropdown["values"] = faction.list_units()
        d_unit_dropdown.set("")
        d_selected_unit.set("")
        clear_squad_display()

def clear_squad_display(frames):
    for widget in frames:
        widget.destroy()
    frames.clear()

def load_attacker_unit(event):
    faction_name = a_selected_faction.get()
    unit_name = a_selected_unit.get()
    if faction_name in factions:
        faction = factions[faction_name]
        try:
            unit = faction.get_unit(unit_name)
            global a_squad
            a_squad = build_squad(unit.default_squad.models, unit.default_squad.loadout)
            update_model_loadouts(squad, attacker_frames, root, unit)
        except ValueError as e:
            print(e)

def load_defender_unit(event):
    faction_name = d_selected_faction.get()
    unit_name = d_selected_unit.get()
    if faction_name in factions:
        faction = factions[faction_name]
        try:
            unit=faction.get_unit(unit_name)
            global d_squad
            d_squad = build_squad(unit.default_squad.models, unit.default_squad.loadout)
            update_model_loadouts(squad, defender_frames, root, unit)
        except ValueError as e:
            print(e)

a_unit_dropdown.bind("<<ComboboxSelected>>", load_attacker_unit)
d_unit_dropdown.bind("<<ComboboxSelected>>", load_defender_unit)

#run the gui

root.mainloop()