from util import tree, get_entries, import_json, get_file_information, check_workspace, file_entry
import json
from collections import OrderedDict
from copy import deepcopy


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
    req_files = ["motion_flag_info", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    motion_flag_info = file_entry(file_jsons, "motion_flag_info", False)
    motion_gmt = file_entry(file_jsons, "motion_gmt", False)

    new_dict = tree()
    mot = get_entries(motion_gmt)
    for entry in [e for e in motion_flag_info["subTable"] if e.isdigit()]:
        motion_name = list(motion_flag_info["subTable"][entry].keys())[0]
        motion_table = str(motion_flag_info["subTable"][entry][motion_name]["2"])
        for motion_entry in motion_flag_info[motion_table][""]:
            if motion_entry == "base_gmt":
                new_dict[motion_name][motion_entry] = mot[motion_flag_info[motion_table][""][motion_entry]]
            else:
                new_dict[motion_name][motion_entry] = motion_flag_info[motion_table][""][motion_entry]
    file_jsons["Final"]["motion_flag_info"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["motion_flag_info", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    motion_flag_info = file_entry(file_jsons, "motion_flag_info")
    motion_gmt = file_entry(file_jsons, "motion_gmt")

    global base_json
    global sub_json
    new_dict = tree()
    sub_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    mot = get_entries(motion_gmt, True)
    ROW_COUNT = len(list(motion_flag_info.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    sub_dict["ROW_COUNT"] = ROW_COUNT

    motion_flag_info = sort_dict_by_motion(motion_flag_info, mot)

    for midx, entry in enumerate(list(motion_flag_info.keys())):
        for sub_entry in motion_flag_info[entry]:
            if sub_entry == "base_gmt":
                new_dict[str(midx)][""][sub_entry] = mot[motion_flag_info[entry][sub_entry]]
            else:
                new_dict[str(midx)][""][sub_entry] = motion_flag_info[entry][sub_entry]
        sub_dict[str(midx)][entry]["0"] = mot[entry]
        sub_dict[str(midx)][entry]["2"] = midx
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["motion_flag_info"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 26,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 197,
  "STORAGE_MODE": 1,
  "columnValidity": {
    "": "0",
    "*": "1",
    "is_common_pack": "1",
    "is_loop": "1",
    "base_gmt": "1",
    "start_frame": "1",
    "is_counter_attack": "1",
    "action_joint_tick": "1",
    "is_charge_attack": "1",
    "is_nage_attack": "1",
    "is_finish_hold_attack": "1",
    "is_heavy_attack": "1",
    "is_light_attack": "1",
    "is_wpv_buki2": "0",
    "is_damage_reversal": "1",
    "is_ma_break": "1",
    "is_reverse_attack": "1",
    "is_avoid_action": "0",
    "is_same_damage_down": "0",
    "is_enable_rev_sabaki": "1",
    "is_sway_attack": "1",
    "is_ex_attack": "1",
    "is_revenge": "1",
    "is_run_attack": "1",
    "is_low_attack": "1",
    "is_combo_finish": "1"
  },
  "columnTypes": {
    "": -1,
    "*": 1,
    "is_common_pack": 6,
    "is_loop": 6,
    "base_gmt": 1,
    "start_frame": 7,
    "is_counter_attack": 6,
    "action_joint_tick": 0,
    "is_charge_attack": 6,
    "is_nage_attack": 6,
    "is_finish_hold_attack": 6,
    "is_heavy_attack": 6,
    "is_light_attack": 6,
    "is_wpv_buki2": -1,
    "is_damage_reversal": 6,
    "is_ma_break": 6,
    "is_reverse_attack": 6,
    "is_avoid_action": -1,
    "is_same_damage_down": -1,
    "is_enable_rev_sabaki": 6,
    "is_sway_attack": 6,
    "is_ex_attack": 6,
    "is_revenge": 6,
    "is_run_attack": 6,
    "is_low_attack": 6,
    "is_combo_finish": 6
  },
  "COLUMN_INDICES": [
    1,
    2,
    3,
    4,
    5,
    7,
    6,
    8,
    9,
    10,
    25,
    11,
    12,
    24,
    14,
    15,
    16,
    19,
    20,
    21,
    22,
    23,
    18,
    17,
    13,
    0
  ]
}
'''

sub_json = '''
{
    "ROW_COUNT": 666,
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