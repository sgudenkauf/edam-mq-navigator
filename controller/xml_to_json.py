# Created by Janek Behrens on 15.08.23.
import xml.etree.ElementTree as ET
import json
import sys
import tkinter as tk
from tkinter import messagebox

if len(sys.argv) != 2:
    print("Usage: python xml_to_json.py <input_xml_file>")
    sys.exit(1)

input_xml_file = sys.argv[1]

tree = None
try:
    tree = ET.parse(input_xml_file)
except Exception as e:
    messagebox.showerror("Error", f"Error while parsing XML file: {str(e)}")
    sys.exit(1)

root = tree.getroot()

def extract_data(element):
    data = {"name": element.get("name"), "description": "", "color": "", "children": []}
    description_elem = element.find("description")
    if description_elem is not None:
        data["description"] = description_elem.text.strip()
        data["color"] = "#FF9933"
    else:
        data["color"] = "#FFFFFF"
    children = element.findall("and") + element.findall("feature")
    for child in children:
        data["children"].append(extract_data(child))
    return data

json_data = []
for child in root.findall("struct/and"):
    json_data.append(extract_data(child))

output_json_file = input_xml_file.replace(".xml", ".json")
try:
    with open(output_json_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
except Exception as e:
    messagebox.showerror("Error", f"Error while writing JSON file: {str(e)}")
    sys.exit(1)

message = f"Conversion complete. JSON file saved as {output_json_file}"

root = tk.Tk()
root.title("XML to JSON Conversion")

label = tk.Label(root, text=message)
label.pack(padx=20, pady=20)

output_dir = output_json_file.rsplit("/", 1)[0]
output_dir_label = tk.Label(root, text=f"File saved in directory: {output_dir}")
output_dir_label.pack()

root.mainloop()
