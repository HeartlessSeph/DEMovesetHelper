from util import tree, get_entries, check_workspace, file_entry
import json


def prep_workspace(file_jsons):
    req_files = ["battle_motion_set", "motion_gmt", "behavior_set"]
    if check_workspace(req_files, file_jsons): return
    motion_set = file_entry(file_jsons, "battle_motion_set", False)
    motion_gmt = file_entry(file_jsons, "motion_gmt", False)
    behavior_set = file_entry(file_jsons, "behavior_set", False)

    new_dict = tree()
    mot = get_entries(motion_gmt)
    bhv = get_entries(behavior_set)
    for entry in [e for e in motion_set if e.isdigit()]:
        set_name = list(motion_set[entry].keys())[0]
        for set_entry in motion_set[entry][set_name]:
            if set_entry == "behavior_set":
                new_dict[set_name][set_entry] = bhv[motion_set[entry][set_name][set_entry]]
            elif set_entry not in ["guard_type", "react_damage_type", "reARMP_isValid", "reARMP_rowIndex"]:
                new_dict[set_name][set_entry] = mot[motion_set[entry][set_name][set_entry]]
            elif set_entry != "reARMP_rowIndex":
                new_dict[set_name][set_entry] = motion_set[entry][set_name][set_entry]
    file_jsons["Final"]["battle_motion_set"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["battle_motion_set", "motion_gmt", "behavior_set"]
    if check_workspace(req_files, file_jsons): return
    motion_set = file_entry(file_jsons, "battle_motion_set")
    motion_gmt = file_entry(file_jsons, "motion_gmt")
    behavior_set = file_entry(file_jsons, "behavior_set")

    global base_json
    new_dict = tree()
    new_dict.update(json.loads(base_json))
    mot = get_entries(motion_gmt, True)
    bhv = get_entries(behavior_set, True)
    ROW_COUNT = len(list(motion_set.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    for midx, entry in enumerate(list(motion_set.keys())):
        for sub_entry in motion_set[entry]:
            if sub_entry == "behavior_set":
                motion_set[entry][sub_entry] = bhv[motion_set[entry][sub_entry]]
            elif sub_entry not in ["guard_type", "react_damage_type", "reARMP_isValid"]:
                motion_set[entry][sub_entry] = mot[motion_set[entry][sub_entry]]
            new_dict[str(midx)][entry][sub_entry] = motion_set[entry][sub_entry]
        new_dict[str(midx)][entry]["reARMP_rowIndex"] = midx
    file_jsons["Final"]["battle_motion_set"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 31,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": true,
  "TABLE_ID": 425,
  "STORAGE_MODE": 1,
  "columnValidity": {
    "": "0",
    "behavior_set": "1",
    "sway_f": "1",
    "sway_b": "1",
    "sway_l": "1",
    "sway_r": "1",
    "sway_fl": "1",
    "sway_fr": "1",
    "sway_bl": "1",
    "sway_br": "1",
    "sway_f2": "1",
    "sway_b2": "1",
    "sway_l2": "1",
    "sway_r2": "1",
    "sway_f3": "1",
    "sway_b3": "1",
    "sway_l3": "1",
    "sway_r3": "1",
    "guard_st": "1",
    "guard_lp": "1",
    "guard_en": "1",
    "guard_reaction": "1",
    "guard_type": "1",
    "react_damage_type": "1",
    "pickup": "1",
    "battou": "1",
    "noutou": "1",
    "dying_st": "1",
    "dying_lp": "1",
    "dying_en": "1",
    "replace_pickup": "1"
  },
  "columnTypes": {
    "": -1,
    "behavior_set": 1,
    "sway_f": 1,
    "sway_b": 1,
    "sway_l": 1,
    "sway_r": 1,
    "sway_fl": 1,
    "sway_fr": 1,
    "sway_bl": 1,
    "sway_br": 1,
    "sway_f2": 1,
    "sway_b2": 1,
    "sway_l2": 1,
    "sway_r2": 1,
    "sway_f3": 1,
    "sway_b3": 1,
    "sway_l3": 1,
    "sway_r3": 1,
    "guard_st": 1,
    "guard_lp": 1,
    "guard_en": 1,
    "guard_reaction": 1,
    "guard_type": 2,
    "react_damage_type": 2,
    "pickup": 1,
    "battou": 1,
    "noutou": 1,
    "dying_st": 1,
    "dying_lp": 1,
    "dying_en": 1,
    "replace_pickup": 1
  },
  "COLUMN_INDICES": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    30,
    25,
    26,
    27,
    28,
    29,
    0
  ]
}
'''
