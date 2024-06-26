import tkinter as tk

def calculate_percentages(slider_value):
    ratio = slider_value / 25
    group1 = 50 - ratio * 12.5
    group2 = 50 - ratio * 12.5
    group3 = 50 - (50 - ratio * 12.5) 
    group4 = 50 - (50 - ratio * 12.5) 


    return group1, group2, group3, group4

def update_percentages(event):
    slider_value = slider.get()
    group1_percent, group2_percent, group3_percent, group4_percent = calculate_percentages(slider_value)
    
    # Update label texts
    group1_label.config(text=f"brightHot: {group1_percent:.1f}%")
    group2_label.config(text=f"darkHot: {group2_percent:.1f}%")
    group3_label.config(text=f"darkCold: {group3_percent:.1f}%")
    group4_label.config(text=f"brightCold: {group4_percent:.1f}%")
    
    # Update color_ratio in twin_text.txt
    with open("twin_text.txt", "r") as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        if "color_ratio" in line:
            lines[i] = f"color_ratio = [{group1_percent:.1f}, {group2_percent:.1f}, {group3_percent:.1f}, {group4_percent:.1f}]\n"
            break
    
    with open("twin_text.txt", "w") as file:
        file.writelines(lines)

# Create the main window
root = tk.Tk()
root.title("Object Group Percentages")

# Create a slider
slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_percentages)
slider.pack()

# Create labels for displaying percentages
group1_label = tk.Label(root, text="brightHot 50%")
group1_label.pack()
group2_label = tk.Label(root, text="darkHot: 50%")
group2_label.pack()
group3_label = tk.Label(root, text="darkCold: 0%")
group3_label.pack()
group4_label = tk.Label(root, text="brightCold: 0%")
group4_label.pack()

# Start the GUI event loop
root.mainloop()
