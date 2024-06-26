import tkinter as tk
from tkinter import ttk
import random

previous_tempo = None  # Variable to store the previous tempo


def map_percentages_to_integers(values, target_value):
    # Step 1: Normalize the values
    total = sum(values)
    normalized_values = [v / total for v in values]

    # Step 2: Multiply each normalized value by the target value
    mapped_values = [int(v * target_value) for v in normalized_values]

    # Step 3: Adjust for rounding errors
    adjustment = target_value - sum(mapped_values)
    if adjustment != 0:
        # Sort mapped values in descending order
        sorted_indices = sorted(range(len(mapped_values)), key=lambda x: mapped_values[x], reverse=True)

        # Distribute adjustment to top values until exhausted
        for i in sorted_indices:
            if adjustment == 0:
                break
            mapped_values[i] += 1
            adjustment -= 1

    return mapped_values



def update_variable_A(value):
    with open('twin_text.txt', 'r') as file:
        lines = file.readlines()

    with open('twin_text.txt', 'w') as file:
        for line in lines:
            if line.startswith("A"):
                file.write("A = {}\n".format(value))
            else:
                file.write(line)
                
def read_settings_from_file():
    try:
        with open("twin_text.txt", "r") as file:
            lines = file.readlines()
            tempo_line = [line for line in lines if line.startswith("tempo")]
            tempo = float(tempo_line[0].split("=")[1].strip())
            num_colors_line = [line for line in lines if line.startswith("nbr_of_colors")]
            num_colors = int(num_colors_line[0].split("=")[1].strip())
            return tempo, num_colors
    except FileNotFoundError:
        print("Error: twin_text.txt not found.")
        return None, None
    except ValueError:
        print("Error: Invalid data in twin_text.txt.")
        return None, None

def read_colors_from_file():
    try:
        with open("colors.txt", "r") as file:
            colors = [line.strip() for line in file.readlines()]
            return colors
    except FileNotFoundError:
        print("Error: colors.txt not found.")
        return None

def write_settings_to_file(tempo, num_colors):
    with open("twin_text.txt", "r") as file:
        lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("tempo"):
            lines[i] = f"tempo = {tempo}\n"
        elif line.startswith("nbr_of_colors"):
            lines[i] = f"nbr_of_colors = {num_colors}\n"
        elif line.startswith("FinalPepeColors"):
            # chosen_colors = colors[:num_colors] ### HERE YOU  PUT THE RANDOM colors
            colors = read_colors_from_file()
            lines[i] = f"FinalPepeColors = {colors}\n"
    with open("twin_text.txt", "w") as file:
        file.writelines(lines)

def generate_random_num_colors():
    return random.randint(5, 12)

def update_settings(tempo, num_colors):
    write_settings_to_file(tempo, num_colors)
    tempo_slider.set(tempo)
    num_colors_slider.set(num_colors)
    update_color_display(num_colors)
    

def get_new_colors(nbr_of_colors): ##### Faz update das colors no colors.txt
    # Read colors from colors.txt
    with open('colors.txt', 'r') as colors_file:
        colors = [line.strip() for line in colors_file.readlines()]

    # Read all colors from all_colors.txt
    all_colors = {}
    with open('all_colors.txt', 'r') as all_colors_file:
        current_group = None
        for line in all_colors_file:
            line = line.strip()
            if line.startswith("#"):
                all_colors[current_group].append(line)
            else:
                current_group = line
                all_colors[current_group] = []
    # Read number of colors
    # with open("twin_text.txt", "r") as f:
    #             lines = f.readlines()
    #             for line in lines[:-1]: ### essenctial para usar as pepecolors //// lines[:-1] é pq conta a ultima linha como excepção
    #                 var, value = line.strip().split(" = ")
    #                 if var == "nbr_of_colors":
    #                     nbr_of_colors = eval(value)
        
    # Read color_ratio from
    with open("twin_text.txt", "r") as f:
                lines = f.readlines()
                for line in lines[:-1]: ### essenctial para usar as pepecolors //// lines[:-1] é pq conta a ultima linha como excepção
                    var, value = line.strip().split(" = ")
                    if var == "color_ratio":
                        color_ratio = eval(value)
                        brightHot_clr, darkHot_clr, darkCold_clr, brightCold_clr= map_percentages_to_integers(color_ratio, nbr_of_colors)
        # Apply Ratio select colors from each group in all_colors.txt
    new_colors = []
    bh_group = list(all_colors.get('brightHot'))
    dh_group = list(all_colors.get('darkHot'))
    dc_group = list(all_colors.get('darkCold'))
    bc_group = list(all_colors.get('brightCold'))
    nbrcolor = brightHot_clr + darkHot_clr + darkCold_clr + brightCold_clr
    while nbrcolor:
        if brightHot_clr > 0:
            new_color = random.choice(bh_group)
            bh_group.remove(new_color)  
            brightHot_clr = brightHot_clr - 1
        elif darkHot_clr > 0:
            new_color = random.choice(dh_group)
            dh_group.remove(new_color)  
            darkHot_clr = darkHot_clr - 1
        elif darkCold_clr > 0:
            new_color = random.choice(dc_group)
            dc_group.remove(new_color)  
            darkCold_clr = darkCold_clr - 1
        elif brightCold_clr > 0:
            new_color = random.choice(bc_group)
            bc_group.remove(new_color)  
            brightCold_clr = brightCold_clr - 1
            
        new_colors.append(new_color)
        nbrcolor = nbrcolor - 1                      


    # Write new colors back to colors.txt
    with open('colors.txt', 'w') as colors_file:
        for color in new_colors:
            colors_file.write(color + '\n')


def create_new_settings():                                      ##### LOOPS HERE
    global previous_tempo  # Declare previous_tempo as global
    new_tempo = tempo_slider.get()
    if previous_tempo is None or new_tempo != previous_tempo:
        previous_tempo = new_tempo
    else:
        new_tempo = generate_random_tempo()
    new_num_colors = generate_random_num_colors() # Fazer if else para absorver leitura do slider
    get_new_colors(new_num_colors)
    update_colors()
    update_settings(new_tempo, new_num_colors) 
    update_variable_A(True)
    root.after(int(new_tempo * 1000), create_new_settings)

def update_color_display(num_colors):
    for i, label in enumerate(color_labels):
        row = (i // 2) * 2 + 3  # Put color pairs in alternating rows starting from row 3
        col = i % 2  # Alternate between columns
        if i < num_colors:
            label.grid(row=row, column=col, padx=5, pady=5)
        else:
            label.grid_forget()

def update_colors():
    #global colors
    colors = read_colors_from_file()
    if colors is not None:
        for i, color in enumerate(colors):
            color_labels[i].configure(bg=color)

def tempo_changed(event):
    pass

def num_colors_changed(event):
    num_colors = num_colors_slider.get()
    update_settings(tempo_slider.get(), num_colors)

def generate_random_tempo():
    return round(random.uniform(1, 5), 1)

# Create the main window
root = tk.Tk()
root.title("Twin Window")

# Create the tempo slider
tempo_slider_label = tk.Label(root, text="Tempo:")
tempo_slider_label.grid(row=0, column=0, sticky="S")  # Align to the west (left)
tempo_slider = tk.Scale(root, from_=1, to=5, resolution=0.1, orient=tk.HORIZONTAL)
tempo_slider.grid(row=0, column=1, columnspan=9)  # Make the slider fill the cell horizontally
tempo_slider.bind("<ButtonRelease-1>", tempo_changed)  # Bind change event to function

# Create the number of colors slider
num_colors_slider_label = tk.Label(root, text="Number of Colors:")
num_colors_slider_label.grid(row=1, column=0, sticky="S")  # Align to the west (left)
num_colors_slider = tk.Scale(root, from_=5, to=12, resolution=1, orient=tk.HORIZONTAL)
num_colors_slider.grid(row=1, column=1, columnspan=9)  # Make the slider fill the cell horizontally
num_colors_slider.bind("<ButtonRelease-1>", num_colors_changed)  # Bind change event to function



# Display the colors
color_labels = []
colors = []
#colors = read_colors_from_file()

with open('all_colors.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith("#"):
            # file.write("A = {}\n".format(value))
            colors.append(line.strip())
            
    # colors = ["#ffffff"] * 14 

for i, color in enumerate(colors):
    label = tk.Label(root, bg=color, width=10, height=2)
    color_labels.append(label)

# Initialize sliders with values from file
initial_tempo, initial_num_colors = read_settings_from_file()
if initial_tempo is not None and initial_num_colors is not None:
    tempo_slider.set(initial_tempo)
    num_colors_slider.set(initial_num_colors)
    update_color_display(initial_num_colors)

create_new_settings()

root.mainloop()
