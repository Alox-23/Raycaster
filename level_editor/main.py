from tkinter import *
from PIL import Image, ImageTk
import os
import math

root = Tk()

#constants
map_size = 32
map_size_pad = 700
map_button_size = map_size_pad // map_size

map = [
    [
        []
    ]
]

#variables
texture_folder_path = "assets"
selected_texture = 1

textures = []

#functions
def load_textures_from_folder(path):
    textures = []
    texture_list = {}
    door_list = {}

    for id, i in enumerate(os.listdir(path+"/textures")):
        photo = Image.open(path+"/textures/"+i)
        photo = photo.resize((60, 60))
        img = ImageTk.PhotoImage(photo)

        photo = photo.resize((map_button_size, map_button_size))
        btn_img = ImageTk.PhotoImage(photo)

        texture_list[id] = [img, i, id, btn_img]

    photo = Image.open("default.png")
    photo = photo.resize((60, 60))
    img = ImageTk.PhotoImage(photo)

    photo = photo.resize((map_button_size, map_button_size))
    btn_img = ImageTk.PhotoImage(photo)
    print(id+1)
    texture_list[id+1] = [img, "default", id+1, btn_img]
    textures.append(texture_list)

    for id, i in enumerate(os.listdir(path+"/doors")):
        photo = Image.open(path+"/doors/"+i)
        photo = photo.resize((60, 60))
        img = ImageTk.PhotoImage(photo)

        photo = photo.resize((map_button_size, map_button_size))
        btn_img = ImageTk.PhotoImage(photo)

        door_list[id] = [img, i, id, btn_img]
    textures.append(door_list)

    return textures

def change_texture(id):
    global selected_texture
    selected_texture = id
    print("change_texture", id)

def paint(x, y):
    map[0][y][x].config(image = textures[0][selected_texture][3])

#main
textures = load_textures_from_folder(texture_folder_path)

#panels
left_panel = LabelFrame(root, text = "Settings:")
mid_panel = LabelFrame(root, text = "Editor:")
right_panel = LabelFrame(root, text = "Textures:")

left_panel.grid(row=1, column=1, sticky="WENS", padx=5, pady=5)
mid_panel.grid(row=1, column=2, columnspan=3, sticky="WENS", padx=5, pady=5)
right_panel.grid(row=1, column=5, sticky="WENS", padx=5, pady=5)

#left_panel
open_textures_label = Label(left_panel, text="Open texture")
open_textures_entry = Entry(left_panel)
open_textures_button = Button(left_panel, text="Open")

open_textures_label.pack()
open_textures_entry.pack()
open_textures_button.pack()

#mid_panel
for y in range(map_size):
    map[0].append([])
    for x in range(map_size):
        map[0][y].append(Button(mid_panel, image=textures[0][len(textures[0])-1][3], command = lambda x=x, y=y: paint(x, y)))
        map[0][y][x].grid(row = y, column = x, sticky="WENS") 

#right_panel
#textures
texture_lable_frame = LabelFrame(right_panel, text="Textures:")

for key, value in textures[0].items():
    texture_frame = LabelFrame(texture_lable_frame, text=value[1], padx=30)
    if key % 2 == 0:
        texture_frame.grid(row = math.floor(key/2), column=1, pady=10, padx=10)
    else:
        texture_frame.grid(row = math.floor(key/2), column=2, pady=10, padx=10)
    label = Label(texture_frame, image=value[0])
    label.pack()
    button = Button(texture_frame, text = "Select", command = lambda i=key: change_texture(i))
    button.pack()

texture_lable_frame.pack(padx=10, pady=10)

root.mainloop()