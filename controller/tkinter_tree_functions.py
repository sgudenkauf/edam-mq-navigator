# Created by Janek Behrens on 15.08.23.
import tkinter as tk
from tkinter import messagebox
from sunburstGenerator import *
from controller.globals import get_json_file_path


def populate_tree(tree, parent, node):
    description = node.get("description", "")  # Standardwert: Leerstring, wenn "description" nicht vorhanden ist
    color = node.get("color", "#FF9933")  # Verwende "#FF9933", wenn "color" nicht vorhanden ist

    item = tree.insert(parent, "end", text=node["name"], values=(description, color),
                       tags=(color, description))
    tree.tag_configure(color, background=color, foreground="black")

    if "children" in node:
        for child in node["children"]:
            populate_tree(tree, item, child)


def add_child(tree, child_name_entry, child_description_entry, color_combobox, predefined_colors):
    selected_items = tree.selection()

    if selected_items:
        selected_item = selected_items[0]
    else:
        selected_item = ""

    child_name = child_name_entry.get()
    child_description = child_description_entry.get()
    child_color_name = color_combobox.get()

    # Pruefen ob Name leer ist
    if not child_name:
        messagebox.showerror("Error", "Please enter a child name.")
        return

    child_color = predefined_colors[child_color_name]
    child_data = {
        "name": child_name,
        "description": child_description,
        "color": child_color
    }

    new_item = tree.insert(selected_item, "end", text=child_data["name"],
                           values=(child_data["description"], child_data["color"],),
                           tags=(child_data["description"], child_data["color"] ))
    tree.tag_configure(child_data["color"], background=child_data["color"], foreground="black")

    if selected_item:
        selected_node = tree.item(selected_item)
        selected_node["values"] = (selected_node["values"][0],)

    child_name_entry.delete(0, tk.END)
    child_description_entry.delete(0, tk.END)


def save_tree(tree):
    data = []
    for child in tree.get_children():
        data.append(get_node_data(tree, child))
    try:
        with open(get_json_file_path(), "w") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Success", "JSON data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving JSON data:\n{e}")


def get_node_data(tree, item):
    node = {
        "name": tree.item(item, "text"),
        "description": "",
        "color": tree.item(item, "values")[1],
    }

    values = tree.item(item, "values")
    if len(values) > 1:
        node["description"] = values[0]

    children = tree.get_children(item)
    if children:
        node["children"] = [get_node_data(tree, child) for child in children]
    return node


def delete_selected(tree):
    selected_item = tree.selection()[0]
    tree.delete(selected_item)


def on_treeview_select(tree, current_clicked_name):
    selected_items = tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        selected_node = tree.item(selected_item)
        current_description = current_clicked_name.get()
        node_description = selected_node["values"]
        print(node_description)
        if len(node_description) > 1:
            if f"Description: {node_description[0]}" == current_description:
                print(f"Description: {node_description[0]}")
                tree.selection_remove(selected_item)
                current_clicked_name.set("Description: ")
            else:
                print("else inner")
                current_clicked_name.set(f"Description: {node_description[0]}")
        else:
            print("else outher")
            tree.selection_set(selected_item)
            current_clicked_name.set("Description: ")
    else:
        current_clicked_name.set("Description: ")


def open_in_browser():
    sunburst_generator = SunburstGenerator(get_json_file_path())
    sunburst_generator.generate_sunburst()
    print(get_json_file_path())

    # Optional bei Bedarf, funktioniert.
    # webbrowser.open('output_sunburst.html')
    # HTML-Datei speichern
    # sunburst_generator.fig.write_html("output_sunburst.html")
