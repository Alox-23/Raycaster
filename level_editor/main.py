from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import json
import os
import math

root = Tk()

root.configure(bg = "#303030")

root.option_add("*Font", "Helvetica 8 bold")
root.option_add("*Background", "#303030")
root.option_add("*Foreground", "white")

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
class map_item:
    value = 0
    def __init__(self, btn, value):
        self.btn = btn
        self.value = value

    def get_value(self):
        return self.value
    
    def set_value(self, v):
        self.value = v

    def set_btn_image(self):
        if selected_texture == 0:
           self.btn.config(image = default_btn_img) 
        else:
            self.btn.config(image = textures[0][selected_texture][3])
    
    def get_btn(self):
        return self.btn


texture_folder_path = "assets"
selected_texture = 1

textures = []

photo = Image.open("default.png")
photo = photo.resize((60, 60))
default_img = ImageTk.PhotoImage(photo)

photo = photo.resize((map_button_size, map_button_size))
default_btn_img = ImageTk.PhotoImage(photo)

#functions
def load_textures_from_folder(path, texture_label_frame):
    try:
        os.listdir(path+"/textures")
        global textures
        response = "yes"
        if len(textures) > 0:
            response = messagebox.askquestion("Warning", "Are you sure? this will delete the map you have made and reset textures")
        print(response)
        if response == "yes":
            print(
                response == "yes"
            )
            textures = []
            texture_list = {}
            door_list = {}
            for id, i in enumerate(os.listdir(path+"/textures")):
                photo = Image.open(path+"/textures/"+i)
                photo = photo.resize((60, 60))
                img = ImageTk.PhotoImage(photo)

                photo = photo.resize((map_button_size, map_button_size))
                btn_img = ImageTk.PhotoImage(photo)

                texture_list[id+1] = [img, i, id, btn_img]
            textures.append(texture_list)

            for id, i in enumerate(os.listdir(path+"/doors")):
                photo = Image.open(path+"/doors/"+i)
                photo = photo.resize((60, 60))
                img = ImageTk.PhotoImage(photo)

                photo = photo.resize((map_button_size, map_button_size))
                btn_img = ImageTk.PhotoImage(photo)

                door_list[id] = [img, i, id, btn_img]
            textures.append(door_list)

            texture_label_frame.pack_forget()

            for key, value in textures[0].items():
                texture_frame = LabelFrame(texture_label_frame, text=value[1], padx=30)
                if key % 2 == 0:
                    texture_frame.grid(row = math.floor(key/2), column=1, pady=10, padx=10)
                else:
                    texture_frame.grid(row = math.floor(key/2), column=2, pady=10, padx=10)
                label = Label(texture_frame, image=value[0])
                label.pack()
                button = Button(texture_frame, text = "Select", command = lambda i=key: change_texture(i))
                button.pack()
            texture_frame = LabelFrame(texture_label_frame, text="default", padx=30)
            texture_frame.grid(row = 0, column=1, pady=10, padx=10)
            label = Label(texture_frame, image=default_img)
            label.pack()
            button = Button(texture_frame, text = "Select", command = lambda i=key: change_texture(0))
            button.pack()

            texture_label_frame.pack(padx=10, pady=10)

            for y in range(map_size):
                for x in range(map_size):
                    map[0][y][x].get_btn().config(image=default_btn_img, command = lambda x=x, y=y: paint(x, y))
                    map[0][y][x].set_value(0)
    except FileNotFoundError:
        messagebox.showerror("Invalid directory", "The directory entered does not exist level_editor/"+path)

def change_texture(id):
    global selected_texture
    selected_texture = id

def paint(x, y):
    map[0][y][x].set_value(selected_texture)
    map[0][y][x].set_btn_image()

def get_level():
    level = [
        [

        ]
    ]
    print("level:")
    for y in range(map_size):
        level[0].append([])
        for x in range(map_size):
            item = map[0][y][x]
            level[0][y].append(item.get_value())
            print(item.get_value(), ",", end="")
        print()
        
#panels
left_panel = LabelFrame(root, text = "Settings:")
mid_panel = LabelFrame(root, text = "Editor:")
right_panel = LabelFrame(root, text = "Textures:")

left_panel.grid(row=1, column=1, sticky="WENS", padx=5, pady=5)
mid_panel.grid(row=1, column=2, columnspan=3, sticky="WENS", padx=5, pady=5)
right_panel.grid(row=1, column=5, sticky="WENS", padx=5, pady=5)

#main

#right_panel
#textures
texture_label_frame = LabelFrame(right_panel, text="Textures:")

for y in range(map_size):
    map[0].append([])
    for x in range(map_size):
        item = map_item(
            Button(mid_panel, command = lambda x=x, y=y: paint(x, y), background="#1c1c1c", highlightbackground="#adadad", activebackground="#f5ff96", activeforeground="#f5ff96", relief="flat"),
            0
        )

        map[0][y].append(item)
        map[0][y][x].get_btn().grid(row = y, column = x, sticky="WENS") 

load_textures_from_folder(texture_folder_path, texture_label_frame)

#left_panel
open_textures_frame = Frame(left_panel, pady=10, padx=10, borderwidth=1, relief="ridge")
open_textures_frame.pack(pady=10, padx=10)

open_textures_label = Label(open_textures_frame, text="Open texture")
open_textures_entry = Entry(open_textures_frame)
open_textures_button = Button(open_textures_frame, text="Open", command = lambda : load_textures_from_folder(open_textures_entry.get(), texture_label_frame))

open_textures_label.pack()
open_textures_entry.pack()
open_textures_button.pack()

save_as_frame = Frame(left_panel, pady=10, padx=10, borderwidth=1, relief="ridge")
save_as_frame.pack(pady=10, padx=10)

save_as_label = Label(save_as_frame, text="Save as")
save_as_entry = Entry(save_as_frame)
save_as_button = Button(save_as_frame, text="Save as", command = get_level)

save_as_label.pack()
save_as_entry.pack()
save_as_button.pack()

#mid_panel

root.mainloop()