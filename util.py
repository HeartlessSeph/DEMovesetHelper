import json
from collections import defaultdict
import os
from pathlib import Path


def export_json(target_path, filename, data, silent=False):  # Writes a json to a certain directory
    """
    :param target_path: Path object
    :param filename: String
    :param data: Dictionary
    :param silent: Boolean
    """

    target_path.mkdir(parents=True, exist_ok=True)
    jsonFile = json.dumps(data, ensure_ascii=False, indent=2)
    jsonPath = target_path / (filename + r'.json')
    jsonPath.write_text(jsonFile, encoding='utf8')
    if not silent: print(f"{filename}.json created.")


def import_json(target_path, name):  # Goes through a directory, then loads json info into a dict
    """
    :param target_path: Path Object
    :param name: String
    """
    import_file = target_path / (name + r'.json')
    with import_file.open(encoding='utf8') as input_file:
        json_array = json.loads(input_file.read())
        return json_array


def tree():
    def the_tree():
        return defaultdict(the_tree)

    return the_tree()


def get_entries(mdict, rev=False):
    new_dict = {}
    for entry in [e for e in mdict if e.isdigit()]:
        puid_name = list(mdict[entry].keys())[0]
        new_dict[int(entry)] = puid_name
    if rev: new_dict = {v: k for k, v in new_dict.items()}
    return new_dict


def get_file_information(mdict, rev=False):
    new_dict = mdict["File Specific Info"]["Set Order"]
    new_dict[""] = 0
    if not rev: new_dict = {v: k for k, v in new_dict.items()}
    return new_dict


def file_entry(f_jsons: dict, mstring: str, f_bool=True):
    if mstring in f_jsons["Final"] and f_bool:
        return f_jsons["Final"][mstring]
    elif mstring in f_jsons["Work"]:
        return f_jsons["Work"][mstring]
    elif mstring in f_jsons["Sub"]:
        return f_jsons["Sub"][mstring]


def check_workspace(req_files, file_jsons):
    wrn_files = []
    for name in req_files:
        if name not in file_jsons["Work"] and name not in file_jsons["Sub"]:
            wrn_files.append(name)
    if len(wrn_files) > 0:
        warning_string = ', '.join([f'{item}.json' for item in wrn_files]) + f" are required to build {req_files[0]}."
        print(warning_string)
        return True
    return False


def yes_or_no():
    print("Type 'y' and press enter if yes, otherwise just press enter.")
    minput = input("")
    return minput.lower() == "y"
