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
    req_files = ["character_model_model_data", "character_model"]
    if check_workspace(req_files, file_jsons): return
    character_model_model = file_entry(file_jsons, "character_model_model_data", False)

    new_dict = tree()
    for entry in [e for e in character_model_model["subTable"] if e.isdigit()]:
        set_name = list(character_model_model["subTable"][entry].keys())[0]
        set_table = str(character_model_model["subTable"][entry][set_name]["2"])
        new_dict[set_name] = character_model_model[set_table][""]
        new_dict[set_name].pop("*model")
    file_jsons["Final"]["character_model_model_data"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["character_model_model_data", "character_model"]
    if check_workspace(req_files, file_jsons): return
    character_model_model = file_entry(file_jsons, "character_model_model_data")
    chara_model_ref = file_entry(file_jsons, "character_model")

    global base_json
    global sub_json
    new_dict = tree()
    sub_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    chara_model = get_entries(chara_model_ref, True)
    sub_ROW_COUNT = len(list(character_model_model.keys()))
    main_entry_list = []
    txt_dict = {}
    new_chara_dict = {}
    last_entry = list(chara_model.keys())[-1]
    last_chara_entry = int(chara_model[last_entry]) + 1

    for entry in character_model_model:
        if entry not in chara_model:
            new_chara_dict[entry] = last_chara_entry
            chara_model[entry] = last_chara_entry
            last_chara_entry += 1
        new_entry = {"*model": chara_model[entry], **character_model_model[entry]}
        for txt_key in ["face_model", "hair_model", "tops_model", "btms_model"]:
            txt_dict[character_model_model[entry][txt_key]] = 0
        main_entry_list.append(new_entry)
    main_entry_list = remove_duplicates(main_entry_list)
    for entry in character_model_model:
        entry_ref = find_matching_index(main_entry_list, character_model_model[entry])
        character_model_model[entry] = entry_ref

    new_dict["ROW_COUNT"] = len(main_entry_list)
    new_dict["TEXT_COUNT"] = len(txt_dict)
    sub_dict["ROW_COUNT"] = sub_ROW_COUNT

    character_model_model = sort_dict_by_puid(character_model_model, chara_model)

    for midx, entry in enumerate(main_entry_list):
        new_dict[str(midx)][""] = entry

    for midx, entry in enumerate(list(character_model_model.keys())):
        sub_dict[str(midx)][entry]["0"] = chara_model[entry]
        sub_dict[str(midx)][entry]["2"] = character_model_model[entry]
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["character_model_model_data"] = new_dict
    for entry in new_chara_dict:
        entry_num = str(new_chara_dict[entry])
        file_jsons["Sub"]["character_model"][entry_num] = {entry: {"reARMP_isValid": "1"}}
        file_jsons["Sub"]["character_model"]["ROW_COUNT"] += 1
        file_jsons["Final"]["character_model"] = file_jsons["Sub"]["character_model"]
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 48,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 1217,
  "STORAGE_MODE": 0,
  "columnValidity": {
    "": "0",
    "*model": "1",
    "is_reuse": "0",
    "category": "1",
    "class_id": "1",
    "age": "1",
    "is_woman": "1",
    "is_face_correct": "1",
    "height": "1",
    "height_range": "1",
    "body_type": "1",
    "language": "1",
    "voicer": "0",
    "bag_type": "1",
    "face_target": "0",
    "tex_skin": "1",
    "tex_face1": "1",
    "tex_face2": "1",
    "tex_face3": "1",
    "tex_face4": "1",
    "tex_hair1": "1",
    "tex_hair2": "1",
    "tex_tops1": "1",
    "tex_tops2": "1",
    "tex_tops3": "1",
    "tex_tops4": "1",
    "tex_btms1": "1",
    "tex_btms2": "1",
    "tex_btms3": "1",
    "dedit_category": "1",
    "dedit": "1",
    "face_model": "1",
    "hair_model": "1",
    "tops_model": "1",
    "btms_model": "1",
    "face_flags": "1",
    "hair_flags": "1",
    "tops_flags": "1",
    "btms_flags": "1",
    "cloth_physics": "1",
    "shoes_kind": "1",
    "auto_wrinkle_scale": "1",
    "can_sit": "1",
    "is_use_fur": "1",
    "auto_gen_advID": "0",
    "is_auto_gen": "0",
    "ui_tex_id": "0",
    "ui_face_texture": "1"
  },
  "columnTypes": {
    "": -1,
    "*model": 1,
    "is_reuse": -1,
    "category": 2,
    "class_id": 1,
    "age": 2,
    "is_woman": 6,
    "is_face_correct": 6,
    "height": 1,
    "height_range": 1,
    "body_type": 2,
    "language": 2,
    "voicer": -1,
    "bag_type": 2,
    "face_target": -1,
    "tex_skin": 2,
    "tex_face1": 2,
    "tex_face2": 2,
    "tex_face3": 2,
    "tex_face4": 2,
    "tex_hair1": 2,
    "tex_hair2": 2,
    "tex_tops1": 2,
    "tex_tops2": 2,
    "tex_tops3": 2,
    "tex_tops4": 2,
    "tex_btms1": 2,
    "tex_btms2": 2,
    "tex_btms3": 2,
    "dedit_category": 2,
    "dedit": 0,
    "face_model": 13,
    "hair_model": 13,
    "tops_model": 13,
    "btms_model": 13,
    "face_flags": 8,
    "hair_flags": 8,
    "tops_flags": 8,
    "btms_flags": 8,
    "cloth_physics": 6,
    "shoes_kind": 2,
    "auto_wrinkle_scale": 7,
    "can_sit": 6,
    "is_use_fur": 6,
    "auto_gen_advID": -1,
    "is_auto_gen": -1,
    "ui_tex_id": -1,
    "ui_face_texture": 1
  },
  "COLUMN_INDICES": [
    1,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    13,
    39,
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
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    40,
    41,
    42,
    43,
    44,
    45,
    47,
    46,
    14,
    12,
    2,
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
