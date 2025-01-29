import tkinter as tk
from tkinter import ttk
import json

from classes import *

#Line Intentionally Left Blank

#Load Factions
faction_folder = "FACTIONS"
factions = load_factions(faction_folder)
for faction_name, faction in factions.items():
    problems = faction.list_units()
    print(f"Faction: {faction_name}, Units: {problems}")

#initialize gui
root = tk.Tk()
root.title("Squad Builder")
root.minsize(1400, 800)
root.geometry("1400x800")

#main container and grid config
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

main_frame.grid_columnconfigure(0, weight=1, minsize=300) #attacker side
main_frame.grid_columnconfigure(1, weight=1, minsize=300) #defender side

# Selectable Variables
a_selected_faction = tk.StringVar()
a_selected_unit = tk.StringVar()
d_selected_faction = tk.StringVar()
d_selected_unit = tk.StringVar()

# faction selection frame
selection_frame = ttk.Frame(main_frame, padding="10")
selection_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

#faction selection frame grid
selection_frame.grid_columnconfigure(0, weight=0) #attacker selector
selection_frame.grid_columnconfigure(1, weight=0) #defender selector


#faction dropdown
attacker_label = ttk.Label(selection_frame, text="Select Attacker Faction:")
attacker_label.grid(row=0, column=0, sticky="w",padx=5)
attacker_dropdown = ttk.Combobox(selection_frame, textvariable=a_selected_faction, state="readonly")
attacker_dropdown["values"] = list(factions.keys())
attacker_dropdown.grid(row=1, column=0, sticky="w", padx=5)

defender_label = ttk.Label(selection_frame, text="Select Defender Faction:")
defender_label.grid(row=0, column=1, sticky="e", padx=5)
defender_dropdown = ttk.Combobox(selection_frame,textvariable=d_selected_faction, state="readonly")
defender_dropdown["values"] = list(factions.keys())
defender_dropdown.grid(row=1, column=1, sticky="e", padx=5)

#unit dropdown
a_unit_label = ttk.Label(selection_frame, text="Select Attacking Unit:")
a_unit_label.grid(row=2, column=0, sticky="w", padx=5)
a_unit_dropdown = ttk.Combobox(selection_frame, textvariable=a_selected_unit, state="readonly")
a_unit_dropdown.grid(row=3, column=0, sticky="w", padx=5)

d_unit_label = ttk.Label(selection_frame, text="select Defending Unit:")
d_unit_label.grid(row=2, column=1, sticky="e", padx=5)
d_unit_dropdown = ttk.Combobox(selection_frame, textvariable=d_selected_unit, state="readonly")
d_unit_dropdown.grid(row=3, column=1, sticky="e", padx=5)

#squad data
a_squad = []
d_squad = []
attacker_frames = []
defender_frames = []

#squad size selector
##frame
squad_size_frame = ttk.Frame(main_frame, padding="5")
squad_size_frame.grid(row=4, column=0, columnspan=3, sticky="ew")

##variables
a_squad_size_var = tk.StringVar(value="1")
a_max_size = 10 #replace later
d_squad_size_var = tk.StringVar(value="1")
d_max_size = 10 #replace later

range_var = tk.StringVar(value="0")

##attacker 
a_size_label = ttk.Label(squad_size_frame, text="Attacker Squad Size:")
a_size_label.grid(row=0, column=0, sticky="e", padx=5)
a_dec_button = ttk.Button(squad_size_frame, text="-", command=lambda: rebuild_squad(a_squad, update_squad_size(a_squad_size_var, -1, a_max_size),factions[a_selected_faction.get()].get_unit(a_selected_unit.get()).default_squad.loadout, attacker_frames, attacker_loadout_frame, factions[a_selected_faction.get()].get_unit(a_selected_unit.get()), alignment="w", column=0))
a_dec_button.grid(row = 1, column=0, sticky="e", padx=5)
a_size_entry = ttk.Entry(squad_size_frame, textvariable=a_squad_size_var, width=5, justify="center")
a_size_entry.grid(row=1, column=1, sticky="w", padx=5)
a_inc_button = ttk.Button(squad_size_frame, text="+", command=lambda:rebuild_squad(a_squad, update_squad_size(a_squad_size_var, 1, a_max_size),factions[a_selected_faction.get()].get_unit(a_selected_unit.get()).default_squad.loadout, attacker_frames, attacker_loadout_frame, factions[a_selected_faction.get()].get_unit(a_selected_unit.get()), alignment="w", column=0))
a_inc_button.grid(row=1, column=2, sticky="w", padx=5)

##defender
d_size_label = ttk.Label(squad_size_frame, text="Defender Squad Size:")
d_size_label.grid(row=0, column=3, sticky="e", padx=5)
d_dec_button = ttk.Button(squad_size_frame, text="-", command=lambda: rebuild_squad(a_squad, update_squad_size(d_squad_size_var, -1, d_max_size),factions[d_selected_faction.get()].get_unit(d_selected_unit.get()).default_squad.loadout, defender_frames, defender_loadout_frame, factions[d_selected_faction.get()].get_unit(d_selected_unit.get()), alignment="w", column=1))
d_dec_button.grid(row = 1, column=3, sticky="e", padx=5)
d_size_entry = ttk.Entry(squad_size_frame, textvariable=d_squad_size_var, width=5, justify="center")
d_size_entry.grid(row=1, column=4, sticky="e", padx=5)
d_inc_button = ttk.Button(squad_size_frame, text="+", command=lambda: rebuild_squad(d_squad, update_squad_size(d_squad_size_var, 1, d_max_size),factions[d_selected_faction.get()].get_unit(d_selected_unit.get()).default_squad.loadout, defender_frames, defender_loadout_frame, factions[d_selected_faction.get()].get_unit(d_selected_unit.get()), alignment="w", column=1))
d_inc_button.grid(row=1, column=5, sticky="e", padx=5)

##column config
squad_size_frame.grid_columnconfigure(0, weight=1)
squad_size_frame.grid_columnconfigure(3, weight=1)
squad_size_frame.grid_columnconfigure(1, weight=0)
squad_size_frame.grid_columnconfigure(4, weight=0)

#Reporting Column
reporting_frame = ttk.Frame(main_frame, padding="10")
reporting_frame.grid(row=6, column=1, sticky="nsew")

report_label = ttk.Label(reporting_frame, text="Results:")
report_label.grid(row=0, column=0, sticky="n", pady=5)
report_text = tk.Text(reporting_frame, height=10, wrap="word")
report_text.grid(row=1, column=0, sticky="nsew")

reporting_frame.grid_rowconfigure(1, weight=1)
reporting_frame.grid_columnconfigure(0, weight=1)

#loadout frames
attacker_loadout_frame = ttk.Frame(main_frame, padding="5")
attacker_loadout_frame.grid(row=6, column=0, sticky="nsew")

defender_loadout_frame = ttk.Frame(main_frame, padding="5")
defender_loadout_frame.grid(row=6, column=2, sticky="nsew")

main_frame.grid_rowconfigure(4, weight=0)
main_frame.grid_rowconfigure(5, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=2)
main_frame.grid_columnconfigure(2, weight=1)


#update dropdown when faction is selected
def update_attacker_unit_dropdown(event):
    faction_name = a_selected_faction.get()
    print(f"Selected Faction: {faction_name}")
    if faction_name in factions:
        faction = factions[faction_name]
        print(f"Units in {faction_name}: {faction.list_units()}")
        a_unit_dropdown["values"] = faction.list_units()
        a_unit_dropdown.set("")
        a_selected_unit.set("")
        clear_squad_display(attacker_frames)

def update_defender_unit_dropdown(event):
    faction_name = d_selected_faction.get()
    if faction_name in factions:
        faction = factions[faction_name]
        d_unit_dropdown["values"] = faction.list_units()
        d_unit_dropdown.set("")
        d_selected_unit.set("")
        clear_squad_display(defender_frames)

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
            global a_max_size
            global a_squad_size_var 
            a_squad_size_var.set(get_min_size(unit))
            a_max_size = get_max_size(unit)
            a_squad = build_squad(unit.default_squad.models, unit.default_squad.loadout)
            update_model_loadouts(a_squad, attacker_frames, attacker_loadout_frame, unit, alignment="w",column=0)
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
            global d_max_size
            global d_squad_size_var
            d_squad_size_var.set(get_min_size(unit))
            d_max_size = get_max_size(unit)
            d_squad = build_squad(unit.default_squad.models, unit.default_squad.loadout)
            update_model_loadouts(d_squad, defender_frames, defender_loadout_frame, unit, alignment="e",column=1)
        except ValueError as e:
            print(e)

def on_attacker_size_change(*args):
    try:
        size_str = a_squad_size_var.get()
        size = int(size_str)
        size = max(1, min(size, a_max_size))
        a_squad_size_var.set(size)
        faction_name = a_selected_faction.get()
        unit_name = a_selected_unit.get()
        if faction_name and unit_name:
            rebuild_squad(a_squad, size, factions[faction_name].get_unit(unit_name).default_squad.loadout,attacker_frames, attacker_loadout_frame, factions[faction_name].get_unit(unit_name),alignment="w", column=0)
    except (ValueError, KeyError):
        pass

def on_defender_size_change(*args):
    try:
        size=int(d_squad_size_var.get())
        size = max(1, min(size, d_max_size))
        d_squad_size_var.set(size)
        faction_name = d_selected_faction.get()
        unit_name = d_selected_unit.get()
        if faction_name and unit_name:
            rebuild_squad(d_squad, size ,factions[faction_name].get_unit(unit_name).default_squad.loadout, defender_frames, defender_loadout_frame, factions[faction_name].get_unit(unit_name), alignment="w", column=1)
    except (ValueError, KeyError):
        pass
def melta_damage(weapon, range):
    if range < (weapon.range // 2):
        melta_kw = [kw for kw in weapon.type if "Melta" in kw]
        if melta_kw:
            kw_list = melta_kw[0].split()
            melta_val = int(kw_list[1])
            return melta_val + weapon.damage
        return weapon.damage
    

def shooting_phase(attacker_squad, target_squad):
    #Overall Button Function for the Shooting Phase
    # ADD A .SELECTED_WEAPONS TO UNIT CLASS
    pass

def reset_all():
    a_selected_faction.set("")
    a_selected_unit.set("")
    d_selected_faction.set("")
    d_selected_unit.set("")
    a_squad_size_var.set("1")
    d_squad_size_var.set("1")
    report_text.delete("1.0", "end")
    clear_squad_display(attacker_frames)
    clear_squad_display(defender_frames)

##BUTTONS
button_frame = ttk.Frame(main_frame, padding="5")
button_frame.grid(row=5, column=0, columnspan=3, sticky="ew")

reset_button = ttk.Button(button_frame, text="Reset All", command=reset_all)
reset_button.grid(row=0, column=1, padx=5)

range_label = ttk.Label(button_frame, text="Range")
range_label.grid(row=0, column=2, sticky="e", padx=5)

range_entry = ttk.Entry(button_frame, textvariable=range_var, width=10, justify="center")
range_entry.grid(row=0, column=3, sticky="w", padx=5)

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=0)
button_frame.grid_columnconfigure(3, weight=0)


a_squad_size_var.trace_add("write", on_attacker_size_change)
d_squad_size_var.trace_add("write", on_defender_size_change)
attacker_dropdown.bind("<<ComboboxSelected>>", update_attacker_unit_dropdown)
defender_dropdown.bind("<<ComboboxSelected>>", update_defender_unit_dropdown)
a_unit_dropdown.bind("<<ComboboxSelected>>", load_attacker_unit)
d_unit_dropdown.bind("<<ComboboxSelected>>", load_defender_unit)
  
#run the gui

root.mainloop()