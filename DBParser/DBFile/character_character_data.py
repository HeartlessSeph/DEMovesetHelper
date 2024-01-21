from util import tree, get_entries, import_json, get_file_information
import json


# TODO: Only the base and sub jsons were done. Fix this for release
def sort_dict_by_file_info(mdict, file_info):
    to_sort = {}
    keys_to_remove = []
    for command_set in mdict:
        to_sort[command_set] = {"SortKey": file_info[command_set], "Dict": mdict[command_set]}
    to_sort = dict(sorted(to_sort.items(), key=lambda item: item[1]["SortKey"]))
    result_dict = {key: to_sort[key]["Dict"] for key in to_sort}
    return result_dict


def prep_workspace(command_set, motion_set):
    new_dict = tree()
    mot_set = get_entries(motion_set)
    for entry in [e for e in command_set["subTable"] if e.isdigit()]:
        set_name = list(command_set["subTable"][entry].keys())[0]
        set_table = str(command_set["subTable"][entry][set_name]["2"])
        for set_entry in command_set[set_table][""]:
            if set_entry == "motion_set":
                new_dict[set_name][set_entry] = mot_set[command_set[set_table][""][set_entry]]
            else:
                new_dict[set_name][set_entry] = command_set[set_table][""][set_entry]
    return new_dict


def prep_build(command_set, motion_set, file_information):
    global base_json
    global sub_json
    new_dict = tree()
    sub_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    mot_set = get_entries(motion_set, True)
    file_info = get_file_information(file_information, True)
    ROW_COUNT = len(list(command_set.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    sub_dict["ROW_COUNT"] = ROW_COUNT

    command_set = sort_dict_by_file_info(command_set, file_info)

    for midx, entry in enumerate(list(command_set.keys())):
        command_set[entry]["motion_set"] = mot_set[command_set[entry]["motion_set"]]
        for sub_entry in command_set[entry]:
            new_dict[str(midx)][""][sub_entry] = command_set[entry][sub_entry]
        sub_dict[str(midx)][entry]["0"] = file_info[entry]
        sub_dict[str(midx)][entry]["2"] = midx
    new_dict["subTable"] = sub_dict
    return new_dict


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 2678,
  "COLUMN_COUNT": 22,
  "TEXT_COUNT": 87,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 1190,
  "STORAGE_MODE": 0,
  "columnValidity": {
    "": "0",
    "*character": "1",
    "adv_model_id": "1",
    "auth_model_id": "1",
    "height": "0",
    "cloth_physics": "0",
    "face_target": "1",
    "voicer": "1",
    "character_physics": "0",
    "test_motion": "1",
    "auto_wrinkle_scale": "0",
    "main_chara": "1",
    "chara_physics_off": "1",
    "default_behavior_set_id": "1",
    "is_boss": "1",
    "face_target_custom": "1",
    "is_enum": "1",
    "is_not_exist_face_target": "1",
    "face_target_ta": "0",
    "face_target_ek": "0",
    "face_target_ekkaiwa": "1",
    "is_disable_jobchange": "1"
  },
  "columnTypes": {
    "": -1,
    "*character": 1,
    "adv_model_id": 1,
    "auth_model_id": 1,
    "height": -1,
    "cloth_physics": -1,
    "face_target": 13,
    "voicer": 1,
    "character_physics": -1,
    "test_motion": 13,
    "auto_wrinkle_scale": -1,
    "main_chara": 6,
    "chara_physics_off": 6,
    "default_behavior_set_id": 1,
    "is_boss": 6,
    "face_target_custom": 13,
    "is_enum": 6,
    "is_not_exist_face_target": 6,
    "face_target_ta": -1,
    "face_target_ek": -1,
    "face_target_ekkaiwa": 13,
    "is_disable_jobchange": 6
  },
  "COLUMN_INDICES": [
    1,
    2,
    3,
    6,
    15,
    20,
    7,
    12,
    9,
    11,
    14,
    13,
    16,
    17,
    21,
    19,
    18,
    10,
    8,
    5,
    4,
    0
  ]
}
'''

sub_json = '''
{
    "ROW_COUNT": 2678,
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
