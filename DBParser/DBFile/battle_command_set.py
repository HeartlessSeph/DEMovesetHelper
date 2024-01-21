from util import tree, get_entries, import_json, get_file_information, file_entry, check_workspace
import json


def sort_dict_by_file_info(mdict, file_info):
    to_sort = {}
    keys_to_remove = []
    for command_set in mdict:
        to_sort[command_set] = {"SortKey": file_info[command_set], "Dict": mdict[command_set]}
    to_sort = dict(sorted(to_sort.items(), key=lambda item: item[1]["SortKey"]))
    result_dict = {key: to_sort[key]["Dict"] for key in to_sort}
    return result_dict


def find_matching_index(dict_list, my_dict):
    for idx, d in enumerate(dict_list):
        if all(d[key] == value for key, value in my_dict.items()):
            return idx
    return None  # Return None if no match is found


def remove_duplicates(dict_list):
    seen_representations = set()
    unique_dicts = []

    for d in dict_list:
        representation = tuple(sorted(d.items()))
        if representation not in seen_representations:
            seen_representations.add(representation)
            unique_dicts.append(d)

    return unique_dicts


def prep_workspace(file_jsons):
    req_files = ["battle_command_set", "battle_motion_set"]
    if check_workspace(req_files, file_jsons): return
    command_set = file_entry(file_jsons, "battle_command_set", False)
    motion_set = file_entry(file_jsons, "battle_motion_set", False)

    new_dict = tree()
    mot_set = get_entries(motion_set)
    for entry in [e for e in command_set["subTable"] if e.isdigit()]:
        set_name = list(command_set["subTable"][entry].keys())[0]
        set_table = str(command_set["subTable"][entry][set_name]["2"])
        for set_entry in command_set[set_table][""]:
            if set_entry == "motion_set":
                new_dict[set_name][set_entry] = mot_set[command_set[set_table][""][set_entry]]
            elif set_entry != "*":
                new_dict[set_name][set_entry] = command_set[set_table][""][set_entry]
    file_jsons["Final"]["battle_command_set"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["battle_command_set", "battle_motion_set", "File Information"]
    if check_workspace(req_files, file_jsons): return
    command_set = file_entry(file_jsons, "battle_command_set")
    motion_set = file_entry(file_jsons, "battle_motion_set")
    file_information = file_entry(file_jsons, "File Information")

    global base_json
    global sub_json
    new_dict = tree()
    sub_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    mot_set = get_entries(motion_set, True)
    file_info = get_file_information(file_information, True)
    sub_ROW_COUNT = len(list(command_set.keys()))
    main_entry_list = []

    for entry in command_set:
        command_set[entry]["motion_set"] = mot_set[command_set[entry]["motion_set"]]
        new_entry = {"*": 256 * command_set[entry]["motion_set"], **command_set[entry]}
        main_entry_list.append(new_entry)
    main_entry_list = remove_duplicates(main_entry_list)
    for entry in command_set:
        entry_ref = find_matching_index(main_entry_list, command_set[entry])
        command_set[entry] = entry_ref

    new_dict["ROW_COUNT"] = len(main_entry_list)
    sub_dict["ROW_COUNT"] = sub_ROW_COUNT

    command_set = sort_dict_by_file_info(command_set, file_info)

    for midx, entry in enumerate(main_entry_list):
        new_dict[str(midx)][""] = entry

    for midx, entry in enumerate(list(command_set.keys())):
        sub_dict[str(midx)][entry]["0"] = file_info[entry]
        sub_dict[str(midx)][entry]["2"] = command_set[entry]
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["battle_command_set"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 10,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 1282,
  "STORAGE_MODE": 1,
  "columnValidity": {
    "": "0",
    "*": "1",
    "motion_set": "1",
    "is_sync_move_push": "1",
    "sync_move_ang_limit": "1",
    "sync_move_speed": "1",
    "is_prog_sway": "1",
    "antidown_type": "1",
    "antiattack_type": "1",
    "antidown_type_2": "1"
  },
  "columnTypes": {
    "": -1,
    "*": 1,
    "motion_set": 1,
    "is_sync_move_push": 6,
    "sync_move_ang_limit": 7,
    "sync_move_speed": 7,
    "is_prog_sway": 6,
    "antidown_type": 2,
    "antiattack_type": 2,
    "antidown_type_2": 2
  },
  "COLUMN_INDICES": [1, 2, 3, 4, 5, 6, 7, 9, 8, 0]
}
'''

sub_json = '''
{
"ROW_COUNT": 0,
"COLUMN_COUNT": 3,
"TEXT_COUNT": 0,
"ROW_VALIDATOR": -1,
"COLUMN_VALIDATOR": -1,
"HAS_ROW_NAMES": true,
"HAS_COLUMN_NAMES": false,
"HAS_ROW_VALIDITY": false,
"HAS_COLUMN_VALIDITY": false,
"HAS_UNKNOWN_BITMASK": false,
"HAS_ROW_INDICES": false,
"TABLE_ID": 0,
"STORAGE_MODE": 0,
"columnTypes": {
  "0": 0,
  "1": 9,
  "2": 0
}
}
'''
