# Created by Janek Behrens on 15.08.23.
json_file_path = ""
def get_json_file_path():
    return json_file_path

def set_json_file_path(new_path):
    global json_file_path
    json_file_path = new_path
