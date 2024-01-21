from util import tree, get_entries, import_json, get_file_information, file_entry, check_workspace
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
    req_files = ["battle_charge_attack_info", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    charge_attack_info = file_entry(file_jsons, "battle_charge_attack_info", False)
    motion_gmt = file_entry(file_jsons, "motion_gmt", False)

    new_dict = tree()
    mot = get_entries(motion_gmt)
    for entry in [e for e in charge_attack_info["subTable"] if e.isdigit()]:
        motion_name = list(charge_attack_info["subTable"][entry].keys())[0]
        motion_table = str(charge_attack_info["subTable"][entry][motion_name]["2"])
        new_dict[motion_name] = charge_attack_info[motion_table][""]
    file_jsons["Final"]["battle_charge_attack_info"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["battle_charge_attack_info", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    charge_attack_info = file_entry(file_jsons, "battle_charge_attack_info")
    motion_gmt = file_entry(file_jsons, "motion_gmt")

    global base_json
    global sub_json
    new_dict = tree()
    sub_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    mot = get_entries(motion_gmt, True)
    sub_ROW_COUNT = len(list(charge_attack_info.keys()))
    main_entry_list = []

    for entry in charge_attack_info:
        main_entry_list.append(charge_attack_info[entry])
    main_entry_list = remove_duplicates(main_entry_list)
    for entry in charge_attack_info:
        entry_ref = find_matching_index(main_entry_list, charge_attack_info[entry])
        charge_attack_info[entry] = entry_ref

    new_dict["ROW_COUNT"] = len(main_entry_list)
    sub_dict["ROW_COUNT"] = sub_ROW_COUNT

    charge_attack_info = sort_dict_by_motion(charge_attack_info, mot)

    for midx, entry in enumerate(main_entry_list):
        new_dict[str(midx)][""] = entry

    for midx, entry in enumerate(list(charge_attack_info.keys())):
        sub_dict[str(midx)][entry]["0"] = mot[entry]
        sub_dict[str(midx)][entry]["2"] = charge_attack_info[entry]
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["battle_charge_attack_info"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 25,
  "COLUMN_COUNT": 23,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 4470,
  "STORAGE_MODE": 1,
  "SPECIAL_FIELD_INDICES": [
    9,
    20,
    21,
    22
  ],
  "columnValidity": {
    "": "0",
    "*": "1",
    "attr": "1",
    "power": "1",
    "is_prohibit_react_down": "1",
    "is_valid_normal_attack": "0",
    "is_valid_ultimate_attack": "0",
    "add_damage_ratio": "1",
    "option_attr": "1",
    "option_attr[0]": "1",
    "attr_for_ultimate": "1",
    "power_for_ultimate": "1",
    "knockback_lv": "1",
    "knockback_lv_guard": "1",
    "knockback_lv_fly_damage": "1",
    "can_ex_wall_bound": "1",
    "knockback_lv_for_ultimate": "1",
    "knockback_lv_guard_for_ultimate": "1",
    "knockback_lv_fly_damage_for_ultimate": "1",
    "can_ex_wall_bound_for_ultimate": "1",
    "option_attr[1]": "1",
    "option_attr[2]": "1",
    "option_attr[3]": "1"
  },
  "columnTypes": {
    "": -1,
    "*": 1,
    "attr": 2,
    "power": 0,
    "is_prohibit_react_down": 6,
    "is_valid_normal_attack": -1,
    "is_valid_ultimate_attack": -1,
    "add_damage_ratio": 7,
    "option_attr": 16,
    "option_attr[0]": 2,
    "attr_for_ultimate": 2,
    "power_for_ultimate": 0,
    "knockback_lv": 5,
    "knockback_lv_guard": 5,
    "knockback_lv_fly_damage": 5,
    "can_ex_wall_bound": 6,
    "knockback_lv_for_ultimate": 5,
    "knockback_lv_guard_for_ultimate": 5,
    "knockback_lv_fly_damage_for_ultimate": 5,
    "can_ex_wall_bound_for_ultimate": 6,
    "option_attr[1]": 2,
    "option_attr[2]": 2,
    "option_attr[3]": 2
  },
  "COLUMN_INDICES": [
    1,
    2,
    3,
    10,
    11,
    4,
    7,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    8,
    9,
    20,
    21,
    22,
    6,
    5,
    0
  ]
}
'''

sub_json = '''
{
    "ROW_COUNT": 25,
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
