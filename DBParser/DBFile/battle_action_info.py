from util import tree, get_entries, import_json, get_file_information, check_workspace, file_entry
import json
from collections import OrderedDict


def sort_dict_by_motion(mdict, mot):
    to_sort = {}
    keys_to_remove = []
    for cur_anim in mdict:
        to_sort[cur_anim] = {"SortKey": mot[cur_anim], "Dict": mdict[cur_anim]}
    to_sort = dict(sorted(to_sort.items(), key=lambda item: item[1]["SortKey"]))
    result_dict = {key: to_sort[key]["Dict"] for key in to_sort}
    return result_dict


def prep_workspace(file_jsons):
    req_files = ["battle_action_info", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    action_info = file_entry(file_jsons, "battle_action_info", False)
    motion_gmt = file_entry(file_jsons, "motion_gmt", False)

    new_dict = tree()
    mot = get_entries(motion_gmt)
    for entry in [e for e in action_info["subTable"] if e.isdigit()]:
        motion_name = list(action_info["subTable"][entry].keys())[0]
        motion_table = str(action_info["subTable"][entry][motion_name]["2"])
        for motion_entry in action_info[motion_table][""]:
            if motion_entry in ["is_each_bep", "*"]:
                new_dict[motion_name][motion_entry] = action_info[motion_table][""][motion_entry]
            else:
                new_dict[motion_name][motion_entry] = mot[action_info[motion_table][""][motion_entry]]
    file_jsons["Final"]["battle_action_info"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["battle_action_info", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    action_info = file_entry(file_jsons, "battle_action_info")
    motion_gmt = file_entry(file_jsons, "motion_gmt")

    global base_json
    global sub_json
    new_dict = tree()
    sub_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    mot = get_entries(motion_gmt, True)
    ROW_COUNT = len(list(action_info.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    sub_dict["ROW_COUNT"] = ROW_COUNT

    action_info = sort_dict_by_motion(action_info, mot)

    for midx, entry in enumerate(list(action_info.keys())):
        for sub_entry in action_info[entry]:
            if sub_entry in ["is_each_bep", "*"]:
                new_dict[str(midx)][""][sub_entry] = action_info[entry][sub_entry]
            else:
                new_dict[str(midx)][""][sub_entry] = mot[action_info[entry][sub_entry]]
        sub_dict[str(midx)][entry]["0"] = mot[entry]
        sub_dict[str(midx)][entry]["2"] = midx
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["battle_action_info"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 14,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 189,
  "STORAGE_MODE": 1,
  "columnValidity": {
    "": "0",
    "action": "0",
    "hit": "1",
    "guard": "1",
    "near_mot": "1",
    "hi_mot": "1",
    "low_mot": "1",
    "near_hi_mot": "1",
    "near_low_mot": "1",
    "*": "1",
    "is_each_bep": "1",
    "guard_to_damage": "1",
    "guard_break": "1",
    "hit_back_seize": "1"
  },
  "columnTypes": {
    "": -1,
    "action": -1,
    "hit": 1,
    "guard": 1,
    "near_mot": 1,
    "hi_mot": 1,
    "low_mot": 1,
    "near_hi_mot": 1,
    "near_low_mot": 1,
    "*": 1,
    "is_each_bep": 6,
    "guard_to_damage": 1,
    "guard_break": 1,
    "hit_back_seize": 1
  },
  "COLUMN_INDICES": [
    9,
    2,
    3,
    12,
    11,
    13,
    4,
    5,
    6,
    7,
    8,
    10,
    1,
    0
  ]
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
