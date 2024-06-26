import time
import RLBB as pepesmachine
import pygame
import random
import os

tempo = 1
temporale = 0
name_counter = 0  

PepesMachina = pepesmachine
StartPepes = PepesMachina.StartPepeFunction()
screen = StartPepes.get_screen()
pygame.display.set_caption("PEPESMACHINE")


# Function to update the value of variable A in the text file
def update_variable(value):
    with open('twin_text.txt', 'r') as file:
        lines = file.readlines()

    with open('twin_text.txt', 'w') as file:
        for line in lines:
            if line.startswith("A"):
                file.write("A = false\n")
            else:
                file.write(line)

# Get the initial modification time of the file
last_modified_time = os.path.getmtime('twin_text.txt')

while True:
    # Get the current modification time of the file
    current_modified_time = os.path.getmtime('twin_text.txt')

    # If the modification time has changed, react to the change
    if current_modified_time != last_modified_time:
        # Update the last modification time
        last_modified_time = current_modified_time

        # Read the state of variable A from the text file
        with open('twin_text.txt', 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            if line.startswith("A"):
                value = line.split("=")[1].strip().lower() == 'true'
                break

        # If the variable is true, execute the function
        if value:
            with open("twin_text.txt", "r") as f:
                lines = f.readlines()
                for line in lines[:-1]: ### essenctial para usar as pepecolors //// lines[:-1] é pq conta a ultima linha como excepção
                    var, value = line.strip().split(" = ")
                    if value == "True":
                        nbr = lines[-3:-2]
                        var_name, var_nbr_of_colors = nbr[0].strip().split(" = ")
                        nbr_of_colors = int(var_nbr_of_colors)
            PepesMachina.set_new_colors(nbr_of_colors)
            PepesMachina.StartPepeFunction()
            update_variable(False)

    # Wait for a short time before checking again (polling)
    time.sleep(0.1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("CLOSING")
            running = False
            pygame.quit()






# running = True
# while running:
#     PepesMachina = pepesmachine
#     with open("twin_text.txt", "r") as f:
#         lines = f.readlines()
#     for line in lines[:-1]: ### essenctial para usar as pepecolors //// lines[:-1] é pq conta a ultima linha como excepção
#         var, value = line.strip().split(" = ")
#         if value == "True":
#             nbr = lines[-3:-2]
#             var_name, var_nbr_of_colors = nbr[0].strip().split(" = ")
#             nbr_of_colors = int(var_nbr_of_colors)
#         if value == "True" and temporale == 0:
#             PepesMachina.set_new_colors(nbr_of_colors)
#             PepesMachina.StartPepeFunction() ##   Add random instead of temporale
#         if value == "True" and temporale == 1:
#             PepesMachina.set_new_colors(nbr_of_colors)
#             PepesMachina.ADNprocessor.colorChanger()
#         if var == "tempo":
#             tempo = float(value)
#     temporale = temporale + 1
#     if temporale >= 2:
#         temporale = 0
#     time.sleep(tempo)
    
    
    # # Closes pygame  
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         print("CLOSING")
    #         running = False
    #         pygame.quit()
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     realName = f"BabyPepe{name_counter}.png"
        #     name_counter = name_counter + 1
        #     pygame.image.save(screen , realName)


