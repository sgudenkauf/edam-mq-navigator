# Created by Janek Behrens on 15.08.23.
import json
import plotly.express as px
from controller.globals import get_json_file_path


class SunburstGenerator:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = self._read_data_from_json()
        self.name_counts = {}
        self.fig = None

    # Daten aus JSON-Datei lesen
    def _read_data_from_json(self):
        with open(self.json_file_path, 'r') as file:
            data = json.load(file)
        return data

    # Funktion zum aufbereiten der Daten um sie für plotly kompatibel zu machen
    def _extract_data(self, data, parent=None):
        character_list = []
        parent_list = []
        color_list = []
        description_list = []

        for item in data:
            character_list.append(item['name'])
            parent_list.append(parent)
            color_list.append(item['color'])
            description_list.append(item.get('description', ''))
            if 'children' in item:
                child_character, child_parent, child_color, description = self._extract_data(item['children'],
                                                                                             parent=item['name'])
                character_list.extend(child_character)
                parent_list.extend(child_parent)
                color_list.extend(child_color)
                description_list.extend(description)

        return character_list, parent_list, color_list, description_list

    # Doppelte Namen müssen umbenannt werden, weil sonst nicht mit plotly kompatibel
    def _rename_duplicates(self, name):
        if name in self.name_counts:
            self.name_counts[name] += 1
            return f"{name} {self.name_counts[name]}"
        else:
            self.name_counts[name] = 1
            return name

    def generate_sunburst(self):
        # Daten extrahieren
        character, parent, colors, descriptions = self._extract_data(self.data)

        # Doppelte Namen umbenennen
        character = [self._rename_duplicates(name) for name in character]

        # Daten im dictionary speichern
        dataDict = dict(
            character=character,
            parent=parent,
            colors=colors,
            descriptions=descriptions
        )

        # Sunburstdiagramm definieren
        self.fig = px.sunburst(
            dataDict,
            names='character',
            parents='parent',
            title=("Filepath: "+get_json_file_path()),
            color='colors',
            color_discrete_sequence=['#FF9933', '#3399FF', '#FFFFFF']
        )

        # Rahmen um die Elemente
        self.fig.update_traces(
            marker=dict(line=dict(color="black", width=1))
        )

        # Anpassen des Hovertemplates, um die Beschreibung anzuzeigen
        hover_template = "<b>%{label}</b><br>%{customdata}<extra></extra>"
        self.fig.update_traces(
            hovertemplate=hover_template,
            customdata=descriptions
        )

        # Sunburstdiagramm zeichnen
        self.fig.show()

        # Info Ausgabe
        print("character =", character)
        print("parent =", parent)
        print("colors =", colors)
        print("descriptions =", descriptions)
        print("character =", len(character))
        print("parent =", len(parent))
        print("colors =", len(colors))
        print("descriptions =", len(descriptions))
