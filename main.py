# Created by Janek Behrens on 15.08.23.
from tkinter import ttk
from controller.json_functions import open_file_dialog, create_new_json, load_json_data
from controller.tkinter_tree_functions import *
from controller.globals import get_json_file_path
from tkinter import filedialog
import subprocess
import platform

# Vordefinierte Farben
predefined_colors = {
    "🟧 Orangerot": "#FF9933",
    "🟦 Hellblau": "#3399FF",
    "⬜️ Weiß": "#FFFFFF"
}

def convert_xml_to_json():
    xml_file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if xml_file_path:
        subprocess.run(["python", "controller/xml_to_json.py", xml_file_path])



# Erstellen der tkinter-Oberfläche
root = tk.Tk()
root.title("JSON Tree Viewer")

# JSON-Daten aus Datei laden
try:
    with open(get_json_file_path(), 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = []

root.update()

# Menüleiste
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Dateimenü
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open JSON File", command=lambda: open_file_dialog(tree))
file_menu.add_command(label="Create New JSON File", command=lambda: create_new_json(tree))
file_menu.add_command(label="Convert XML to JSON", command=convert_xml_to_json)

# Rahmen für die Baumansicht
tree_frame = ttk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

tree = ttk.Treeview(tree_frame, columns=("Description", "Color"))
tree.heading("#0", text="Name")
tree.heading("Description", text="Description")
tree.heading("Color", text="Color")

tree.column("#0", width=200)
tree.column("Description", width=100)
tree.column("Color", width=80)

tree.pack(fill="both", expand=True)

for entry in data:
    populate_tree(tree, "", entry)

# Erstellen eines Rahmens für die zwei Spalten
frame_split = ttk.Frame(root)
frame_split.pack(fill="both", expand=False, padx=10, pady=10)

def change_color(new_color):
    selected_items = tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        tree.item(selected_item, values=(tree.item(selected_item, "values")[0], new_color), tags=(new_color,))
        tree.tag_configure(new_color, background=new_color, foreground="black")


def on_treeview_right_click(event):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        context_menu.tk_popup(event.x_root, event.y_root)

# Erstellen des Kontextmenüs für Farbauswahl
context_menu = tk.Menu(root, tearoff=0)
for color_name in predefined_colors:
    context_menu.add_command(label=color_name, command=lambda color=predefined_colors[color_name]: change_color(color))

if platform.system() == "Darwin":  # macOS
    tree.bind("<Button-2>", on_treeview_right_click)
else: # Windows
    tree.bind("<Button-3>", on_treeview_right_click)

# linke Spalte
left_frame = ttk.Frame(frame_split)
left_frame.pack(side="left", fill="both", expand=False)

# rechte Spalte
right_frame = ttk.Frame(frame_split)
right_frame.pack(side="right", fill="both", expand=False)

delete_button = ttk.Button(right_frame, text="Delete Selected", command=delete_selected)
delete_button.pack(side="right", expand=False)

# Erkennung welcher Eintrag der Liste angewählt ist und ausgabe der Beschreibung
current_clicked_name = tk.StringVar()
clicked_name_label = ttk.Label(left_frame, textvariable=current_clicked_name, font=("Helvetica", 13))
clicked_name_label.pack(side="left")

# Rahmen für die Schaltflächen und Eingabefelder
input_and_button_frame = ttk.Frame(root)
input_and_button_frame.pack(pady=5, padx=10, anchor="center")

# Rahmen für den gesamten Inhalt unterhalb der Überschrift
content_frame = ttk.LabelFrame(input_and_button_frame, text="Add new nodes to diagram", borderwidth=2, relief="solid")
content_frame.pack(side="top", fill="both", expand=True, pady=(10, 0), padx=10)

# Child Name
child_name_label = ttk.Label(content_frame, text="New Child Name:")
child_name_label.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="w")

child_name_entry = ttk.Entry(content_frame)
child_name_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

# Child Description
child_description_label = ttk.Label(content_frame, text="Child Description:")
child_description_label.grid(row=1, column=0, padx=(0, 5), pady=10, sticky="w")

child_description_entry = ttk.Entry(content_frame)
child_description_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="w")

# Farbauswahl
color_label = ttk.Label(content_frame, text="Color:")
color_label.grid(row=2, column=0, padx=(0, 5), pady=10, sticky="w")

color_combobox = ttk.Combobox(content_frame, values=list(predefined_colors.keys()), state="readonly")
color_combobox.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")
color_combobox.set(list(predefined_colors.keys())[0])

# Schaltflächen
add_button = ttk.Button(content_frame, text="Add Child", command=add_child)
add_button.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="we")

# Rahmen für untere Schaltflächen
final_section = ttk.Frame(root)
final_section.pack(pady=10, padx=10, anchor="center")

web_button = ttk.Button(final_section, text="Open in Browser", command=open_in_browser)
web_button.pack(side="right", expand=False)

save_button = ttk.Button(final_section, text="Save JSON", command=save_tree)
save_button.pack(side="right")

# binding der Funktionen an Ereignisse, damit funktioniert die Auslagerung vom Methoden
web_button.config(command=lambda: open_in_browser())
add_button.config(
    command=lambda: add_child(tree, child_name_entry, child_description_entry, color_combobox, predefined_colors))
save_button.config(command=lambda: save_tree(tree))
delete_button.config(command=lambda: delete_selected(tree))


def on_treeview_click(event):
    item = tree.identify("item", event.x, event.y)
    if item:
        item_text = tree.item(item, "values")
        if item_text:
            description = item_text[0]
            current_clicked_name.set(description)

            current_selection = tree.selection()
            if current_selection and item in current_selection:
                tree.selection_remove(item)
                current_clicked_name.set("")
        else:
            current_clicked_name.set("")


tree.bind("<Button-1>", on_treeview_click)

# Funktion zum Ändern der Farbe

load_json_data(tree)

if __name__ == "__main__":
    root.mainloop()