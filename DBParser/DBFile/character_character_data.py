from util import tree, get_entries, get_file_information, check_workspace, file_entry
import json


def sort_dict_by_puid(mdict, mot):
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
    req_files = ["character_character_data", "character", "sound_voicer", "character_model"]
    if check_workspace(req_files, file_jsons): return
    character_character = file_entry(file_jsons, "character_character_data", False)
    character_ref = file_entry(file_jsons, "character", False)
    sound_voicer = file_entry(file_jsons, "sound_voicer", False)
    character_model = file_entry(file_jsons, "character_model", False)

    new_dict = tree()
    chara = get_entries(character_ref)
    chara_model = get_entries(character_model)
    voicer = get_entries(sound_voicer)
    for entry in [e for e in character_character["subTable"] if e.isdigit()]:
        set_name = list(character_character["subTable"][entry].keys())[0]
        set_table = str(character_character["subTable"][entry][set_name]["2"])
        new_dict[set_name] = character_character[set_table][""]
        new_dict[set_name].pop("*character")
        new_dict[set_name]["voicer"] = voicer[new_dict[set_name]["voicer"]]
        new_dict[set_name]["adv_model_id"] = chara_model[new_dict[set_name]["adv_model_id"]]
        new_dict[set_name]["auth_model_id"] = chara_model[new_dict[set_name]["auth_model_id"]]
    file_jsons["Final"]["character_character_data"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["character_character_data", "character", "sound_voicer", "character_model"]
    if check_workspace(req_files, file_jsons): return
    character_character = file_entry(file_jsons, "character_character_data")
    character_ref = file_entry(file_jsons, "character")
    sound_voicer = file_entry(file_jsons, "sound_voicer")
    character_model = file_entry(file_jsons, "character_model")

    global base_json
    global sub_json
    new_dict = tree()
    sub_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    chara_model = get_entries(character_model, True)
    voicer = get_entries(sound_voicer, True)
    chara = get_entries(character_ref, True)
    sub_ROW_COUNT = len(list(character_character.keys()))
    main_entry_list = []
    txt_dict = {}
    new_chara_dict = {}
    last_entry = list(chara.keys())[-1]
    last_chara_entry = int(chara[last_entry]) + 1

    for entry in character_character:
        character_character[entry]["voicer"] = voicer[character_character[entry]["voicer"]]
        character_character[entry]["adv_model_id"] = chara_model[character_character[entry]["adv_model_id"]]
        character_character[entry]["auth_model_id"] = chara_model[character_character[entry]["auth_model_id"]]
        if entry not in chara:
            new_chara_dict[entry] = last_chara_entry
            chara[entry] = last_chara_entry
            last_chara_entry += 1
        new_entry = {"*character": chara[entry], **character_character[entry]}
        txt_dict[character_character[entry]["face_target"]] = 0
        txt_dict[character_character[entry]["test_motion"]] = 0
        txt_dict[character_character[entry]["face_target_custom"]] = 0
        txt_dict[character_character[entry]["face_target_ekkaiwa"]] = 0
        main_entry_list.append(new_entry)
    main_entry_list = remove_duplicates(main_entry_list)
    for entry in character_character:
        entry_ref = find_matching_index(main_entry_list, character_character[entry])
        character_character[entry] = entry_ref

    new_dict["ROW_COUNT"] = len(main_entry_list)
    new_dict["TEXT_COUNT"] = len(txt_dict)
    sub_dict["ROW_COUNT"] = sub_ROW_COUNT

    character_character = sort_dict_by_puid(character_character, chara)

    for midx, entry in enumerate(main_entry_list):
        new_dict[str(midx)][""] = entry

    for midx, entry in enumerate(list(character_character.keys())):
        sub_dict[str(midx)][entry]["0"] = chara[entry]
        sub_dict[str(midx)][entry]["2"] = character_character[entry]
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["character_character_data"] = new_dict
    for entry in new_chara_dict:
        entry_num = str(new_chara_dict[entry])
        file_jsons["Sub"]["character"][entry_num] = {entry: {"reARMP_isValid": "1"}}
        file_jsons["Sub"]["character"]["ROW_COUNT"] += 1
        file_jsons["Final"]["character"] = file_jsons["Sub"]["character"]
    return


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
