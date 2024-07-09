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
global map_sizey
global map_sizex

level_config = {
    "player-pos": [11, 7],


    "fog-height" : 0,

    "floor-color" : [80,80,80],

    "roof-color" : [40,40,40],

    "fog-color" : [0,0,0],

    "sky" : 0,

    "doors" : [4],

    "door-level" : {
        "4": "city.json"
    }, 

    "sprites": [
        ["wall", [11, 2]],
        ["wall", [15, 5]]
    ]
}

map_sizey = 4
map_sizex = 4
map_size_padx = 700
map_size_pady = 700
global map_button_sizex
global map_button_sizey
global floor_num
map_button_sizex = map_size_padx // map_sizex
map_button_sizey = map_size_pady // map_sizey
floor_num = 0
global map
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
        if value != 0:
            self.btn.config(image = textures[value][3])
        else:
            self.btn.config(image = default_btn_img)

    def get_value(self):
        return self.value
    
    def set_value(self, v):
        self.value = v

    def set_btn_image(self):
        if selected_texture == 0:
           self.btn.config(image = default_btn_img) 
        else:
            self.btn.config(image = textures[selected_texture][3])
    
    def get_btn(self):
        return self.btn


texture_folder_path = "../assets/textures/"
selected_texture = 1

textures = []

photo = Image.open("default.png")
photo = photo.resize((60, 60))
default_img = ImageTk.PhotoImage(photo)

photo = photo.resize((map_button_sizex, map_button_sizey))
default_btn_img = ImageTk.PhotoImage(photo)

#functions
def load_textures_from_folder(path, texture_label_frame):
    try:
        os.listdir(path)
        global textures
        global texture_folder_path
        texture_folder_path = path
        response = "yes"
        if len(textures) > 0:
            response = messagebox.askquestion("Warning", "Are you sure? this will delete the map you have made and reset textures")
        if response == "yes":
            textures = {}
            for id, i in enumerate(os.listdir(path)):
                photo = Image.open(path+i)
                photo = photo.resize((60, 60))
                img = ImageTk.PhotoImage(photo)

                photo = photo.resize((map_button_sizex, map_button_sizey))
                btn_img = ImageTk.PhotoImage(photo)

                textures[id+1] = [img, i, id, btn_img]

            for widgets in texture_label_frame.winfo_children():
                widgets.destroy()

            for key, value in textures.items():
                texture_frame = LabelFrame(texture_label_frame, text="["+str(value[2])+"]"+value[1], padx=30)
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

            for y in range(map_sizey):
                for x in range(map_sizex):
                    map[floor_num][y][x].get_btn().config(image=default_btn_img, command = lambda x=x, y=y: paint(x, y))
                    map[floor_num][y][x].set_value(0)
    except FileNotFoundError:
        messagebox.showerror("Invalid directory", "The directory entered does not exist "+path)

def change_texture(id):
    global selected_texture
    selected_texture = id

def paint(x, y):
    map[floor_num][y][x].set_value(selected_texture)
    map[floor_num][y][x].set_btn_image()

def config_doors(texutre_indexes):
    level_config["doors"] = []
    level_config["door-level"] = []
    print(texutre_indexes.split(","))
    for i in texutre_indexes.split(","):
        level_config["door-level"][i.split(":")[0]] = i.split(":")[-1]
        level_config["doors"].append(int(i.split(":")[0]))
    print(level_config["doors"])
    print(level_config["door-level"])

def save_level(path):
    level = {

    }

    level["level"] = [
    ]

    for floor_num, floor in enumerate(map): 
        level["level"].append([])
        for y, row in enumerate(floor):
            level["level"][floor_num].append([])
            for x, cell in enumerate(row):
                print(level["level"][floor_num], y, floor_num)
                level["level"][floor_num][y].append(cell.get_value())


    for key, value in level_config.items():
        level[key] = value

    #json stuff
        
    try:
        print(path)
        json_object = json.dumps(level, indent = 4)
        with open(path, "w") as f:
            f.write(json_object)
    
    except FileNotFoundError:
        messagebox.showerror("Invalid directory", "The directory entered does not exist "+path)

def save_as_level(path):
    level = {

    }

    level["level"] = [
    ]

    for floor_num, floor in enumerate(map): 
        level["level"].append([])
        for y, row in enumerate(floor):
            level["level"][floor_num].append([])
            for x, cell in enumerate(row):
                print(level["level"][floor_num], y, floor_num)
                level["level"][floor_num][y].append(cell.get_value())


    for key, value in level_config.items():
        level[key] = value

    #json stuff
        
    try:
        print(path)
        json_object = json.dumps(level, indent = 4)
        with open(path, "x") as f:
            f.write(json_object)
    
    except FileExistsError:
        messagebox.showinfo("File exists", "The file " + path + " already exists. Saved your changes to " + "copy_of_" + path)
        with open("copy_of_"+path, "x") as f:
            f.write(json_object)

def save_textures():
    text = {}
    for key, value in texutres.items():
        text[key] = value[1]
    
def load_level(texture_json_path, level_json_path, texture_folder_path, texture_label_frame):
    with open(texture_json_path, "r") as f:
        texture_json_data = json.loads(f.read())

    """
    for id, i in enumerate(os.listdir(path+"/textures")):
                photo = Image.open(path+"/textures/"+i)
                photo = photo.resize((60, 60))
                img = ImageTk.PhotoImage(photo)

                photo = photo.resize((map_button_size, map_button_size))
                btn_img = ImageTk.PhotoImage(photo)

                texture_list[id+1] = [img, i, id, btn_img]
            textures.append(texture_list)
    """

    with open(level_json_path, "r") as f:
        level_json_data = json.loads(f.read())

    map_sizey = len(level_json_data["level"][0])
    map_sizex = len(level_json_data["level"][0][0])
    map_size_padx = 700
    map_size_pady = 700
    global map_button_sizex
    global map_button_sizey
    global floor_num
    map_button_sizex = map_size_padx // map_sizex
    map_button_sizey = map_size_pady // map_sizey

    #update textures
    global textures
    textures = {}
    for key, value in texture_json_data.items():
        photo = Image.open(texture_folder_path+value)
        photo = photo.resize((60, 60))
        img = ImageTk.PhotoImage(photo)

        photo = photo.resize((map_button_sizex, map_button_sizey))
        btn_img = ImageTk.PhotoImage(photo)

        textures[int(key)] = [img, value, int(key), btn_img]

    #update texture gui
    texture_label_frame.pack_forget()

    for key, value in textures.items():
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

    global map
    for floor_num, floor in enumerate(map):
        for y, row in enumerate(floor):
            for x, cell in enumerate(row):
                map[floor_num][y][x].get_btn().grid_forget()
    map = [
        [
            []
        ]
    ]

    for floor_num, floor in enumerate(level_json_data["level"]):
        for y, row in enumerate(floor):
            map[0].append([])
            for x, cell in enumerate(row):
                item = map_item(
                    Button(mid_panel, command = lambda x=x, y=y: paint(x, y), width=map_button_sizex, height=map_button_sizey, background="#1c1c1c", highlightbackground="#adadad", activebackground="#f5ff96", activeforeground="#f5ff96", relief="flat"),
                    cell
                )

                map[floor_num][y].append(item)
                map[floor_num][y][x].get_btn().grid(row = y, column = x, sticky="WENS") 
    
    for floor_num, floor in enumerate(map):
        print("new floor", floor_num)
        for y, row in enumerate(floor):
            for x, cell in enumerate(row):
                print(map[floor_num][y][x].get_value(), end = ", ")

            print()
    
    level_config = {k: v for k, v in level_json_data.items() if k not in {'level'}}
    root.update_idletasks()

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

for y in range(map_sizey):
    map[0].append([])
    for x in range(map_sizex):
        item = map_item(
            Button(mid_panel, command = lambda x=x, y=y: paint(x, y), background="#1c1c1c", highlightbackground="#adadad", activebackground="#f5ff96", activeforeground="#f5ff96", relief="flat"),
            0
        )

        map[floor_num][y].append(item)
        map[floor_num][y][x].get_btn().grid(row = y, column = x, sticky="WENS") 

load_textures_from_folder(texture_folder_path, texture_label_frame)

#left_panel

open_textures_frame = LabelFrame(left_panel, pady=10, padx=10, borderwidth=1, relief="ridge", text="Open texture")
open_textures_frame.pack(pady=10, padx=10)

open_textures_label = Label(open_textures_frame, text="Enter texture folder path")
open_textures_entry = Entry(open_textures_frame)
open_textures_button = Button(open_textures_frame, text="Open", command = lambda : load_textures_from_folder(open_textures_entry.get(), texture_label_frame))

open_textures_label.pack()
open_textures_entry.pack()
open_textures_button.pack()



save_as_frame = LabelFrame(left_panel, pady=10, padx=10, borderwidth=1, relief="ridge", text="Save as")
save_as_frame.pack(pady=10, padx=10)

save_as_label = Label(save_as_frame, text="Enter name")
save_as_entry = Entry(save_as_frame)
save_as_button = Button(save_as_frame, text="Save as", command = lambda : save_as_level(save_as_entry.get()))

save_as_label.pack()
save_as_entry.pack()
save_as_button.pack()



load_frame = LabelFrame(left_panel, pady=10, padx=10, borderwidth=1, relief="ridge", text="Load")
load_frame.pack(pady=10, padx=10)

load_label1 = Label(load_frame, text="Texture json path")
load_entry1 = Entry(load_frame)
load_label2 = Label(load_frame, text="Level json path")
load_entry2 = Entry(load_frame)
load_button = Button(load_frame, text="Load", command = lambda : load_level(load_entry1.get(), load_entry2.get(), texture_folder_path, texture_label_frame))

load_label1.pack()
load_entry1.pack()
load_label2.pack()
load_entry2.pack()
load_button.pack()


set_door_frame = LabelFrame(left_panel, pady=10, padx=10, borderwidth=1, relief="ridge", text="Config doors")
set_door_frame.pack(pady=10, padx=10)

set_door_label = Label(set_door_frame, text="Enter [door_number, level_name], ...")
set_door_entry = Entry(set_door_frame)
set_door_button = Button(set_door_frame, text="Config", command = lambda : config_doors(set_door_entry.get()))

set_door_label.pack()
set_door_entry.pack()
set_door_button.pack()

#mid_panel

root.mainloop()