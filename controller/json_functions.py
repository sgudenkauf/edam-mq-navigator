# Created by Janek Behrens on 15.08.23.
import json
from tkinter import filedialog
from controller.globals import get_json_file_path, set_json_file_path
from controller.tkinter_tree_functions import populate_tree

def open_file_dialog(tree):
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        set_json_file_path(file_path)

        load_json_data(tree)  # Rufe die Funktion auf, um die Daten zu laden

def create_new_json(tree):
    set_json_file_path(filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")]))
    if get_json_file_path():
        with open(get_json_file_path(), "w") as file:
            json.dump([], file)
        load_json_data(tree)  # Rufe die Funktion auf, um die Daten zu laden

def load_json_data(tree):
    if get_json_file_path():
        tree.delete(*tree.get_children())  # Clear the tree before loading new data
        with open(get_json_file_path(), 'r') as file:
            data = json.load(file)
        for entry in data:
            populate_tree(tree, "", entry)
    else:
        print("No JSON file selected.")