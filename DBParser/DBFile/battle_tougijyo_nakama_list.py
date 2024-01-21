from util import tree, get_entries, check_workspace, file_entry
import json


def get_rarity(mdict, rev=False):
    new_dict = {}
    for entry in [e for e in mdict if e.isdigit()]:
        r_name = list(mdict[entry].keys())[0]
        if "name" in mdict[entry][r_name]:
            new_dict[int(entry)] = mdict[entry][r_name]["name"]
        else:
            new_dict[int(entry)] = ""
    if rev: new_dict = {v: k for k, v in new_dict.items()}
    return new_dict


def get_unique_entries(mdict, rev=False):
    new_dict = {}
    new_dict_rev = {}
    for entry in [e for e in mdict if e.isdigit()]:
        puid_name = list(mdict[entry].keys())[0]
        if puid_name in new_dict_rev:
            puid_name = f"{puid_name}{[entry]}"
        new_dict_rev[puid_name] = int(entry)
        new_dict[int(entry)] = puid_name
    if rev: return new_dict_rev
    return new_dict


def prep_workspace(file_jsons):
    req_files = ["battle_tougijyo_nakama_list",
                 "battle_tougijyo_nakama_type",
                 "battle_tougijyo_nakama_skill",
                 "character_npc_soldier_personal_data",
                 "ui_texture",
                 "behavior_set"]
    if check_workspace(req_files, file_jsons): return
    nakama_list = file_entry(file_jsons, "battle_tougijyo_nakama_list", False)
    nakama_type = file_entry(file_jsons, "battle_tougijyo_nakama_type", False)
    nakama_skill = file_entry(file_jsons, "battle_tougijyo_nakama_skill", False)
    nakama_rarity = file_entry(file_jsons, "battle_tougijyo_nakama_rarity", False)
    soldier_personal = file_entry(file_jsons, "character_npc_soldier_personal_data", False)
    ui_texture = file_entry(file_jsons, "ui_texture", False)
    behavior = file_entry(file_jsons, "behavior_set", False)

    new_dict = tree()
    skill = get_entries(nakama_skill)
    n_type = get_entries(nakama_type)
    rarity = get_rarity(nakama_rarity)
    personal = get_unique_entries(soldier_personal)
    ui = get_unique_entries(ui_texture)
    bhv = get_entries(behavior)
    for entry in [e for e in nakama_list if e.isdigit()]:
        set_name = list(nakama_list[entry].keys())[0]
        new_dict[set_name] = nakama_list[entry][set_name]

        new_dict[set_name].pop("reARMP_rowIndex")
        new_dict[set_name]["type"] = n_type[new_dict[set_name]["type"]]
        new_dict[set_name]["skill"] = skill[new_dict[set_name]["skill"]]
        new_dict[set_name]["personal_id"] = personal[new_dict[set_name]["personal_id"]]
        new_dict[set_name]["face_picture"] = ui[new_dict[set_name]["face_picture"]]
        new_dict[set_name]["rarity"] = rarity[new_dict[set_name]["rarity"]]
        new_dict[set_name]["job_skill"] = skill[new_dict[set_name]["job_skill"]]
        new_dict[set_name]["main_menu_bhv_set_id"] = bhv[new_dict[set_name]["main_menu_bhv_set_id"]]
        new_dict[set_name]["face_picture_s"] = ui[new_dict[set_name]["face_picture_s"]]
    file_jsons["Final"]["battle_tougijyo_nakama_list"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["battle_tougijyo_nakama_list",
                 "battle_tougijyo_nakama_type",
                 "battle_tougijyo_nakama_skill",
                 "character_npc_soldier_personal_data",
                 "ui_texture",
                 "behavior_set"]
    if check_workspace(req_files, file_jsons): return
    nakama_list = file_entry(file_jsons, "battle_tougijyo_nakama_list")
    nakama_type = file_entry(file_jsons, "battle_tougijyo_nakama_type")
    nakama_skill = file_entry(file_jsons, "battle_tougijyo_nakama_skill")
    nakama_rarity = file_entry(file_jsons, "battle_tougijyo_nakama_rarity")
    soldier_personal = file_entry(file_jsons, "character_npc_soldier_personal_data")
    ui_texture = file_entry(file_jsons, "ui_texture")
    behavior = file_entry(file_jsons, "behavior_set")

    global base_json
    new_dict = tree()
    new_dict.update(json.loads(base_json))
    skill = get_entries(nakama_skill, True)
    n_type = get_entries(nakama_type, True)
    rarity = get_rarity(nakama_rarity, True)
    personal = get_unique_entries(soldier_personal, True)
    ui = get_unique_entries(ui_texture, True)
    bhv = get_entries(behavior, True)
    ROW_COUNT = len(list(nakama_list.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    for midx, entry in enumerate(list(nakama_list.keys())):
        idx = str(midx)
        new_dict[idx][entry] = nakama_list[entry]
        new_dict[idx][entry]["type"] = n_type[new_dict[idx][entry]["type"]]
        new_dict[idx][entry]["skill"] = skill[new_dict[idx][entry]["skill"]]
        new_dict[idx][entry]["personal_id"] = personal[new_dict[idx][entry]["personal_id"]]
        new_dict[idx][entry]["face_picture"] = ui[new_dict[idx][entry]["face_picture"]]
        new_dict[idx][entry]["rarity"] = rarity[new_dict[idx][entry]["rarity"]]
        new_dict[idx][entry]["job_skill"] = skill[new_dict[idx][entry]["job_skill"]]
        new_dict[idx][entry]["main_menu_bhv_set_id"] = bhv[new_dict[idx][entry]["main_menu_bhv_set_id"]]
        new_dict[idx][entry]["face_picture_s"] = ui[new_dict[idx][entry]["face_picture_s"]]
        new_dict[idx][entry]["reARMP_rowIndex"] = midx
    file_jsons["Final"]["battle_tougijyo_nakama_list"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 52,
  "TEXT_COUNT": 82,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": true,
  "TABLE_ID": 4513,
  "STORAGE_MODE": 1,
  "columnValidity": {
    "": "0",
    "initial_hp": "1",
    "initial_atk": "1",
    "initial_def": "1",
    "type": "1",
    "skill": "1",
    "kizuna_level": "0",
    "start_motion": "0",
    "personal_id": "1",
    "flavor_text": "1",
    "face_picture": "1",
    "Rarity": "0",
    "rarity": "1",
    "exp": "1",
    "kizuna_point": "1",
    "timeline_unacquired": "0",
    "timeline_can_get": "0",
    "timeline_get": "0",
    "timeline_dead": "0",
    "timeline_training": "0",
    "timeline_check_unacquired": "1",
    "timeline_check_acquirable": "1",
    "timeline_check_aquired": "1",
    "timeline_check_dead": "1",
    "timeline_check_training": "1",
    "timeline_set_acquirable": "1",
    "timeline_set_unacquired": "1",
    "timeline_set_aquired": "1",
    "timeline_set_dead": "1",
    "timeline_set_training": "1",
    "job_skill": "1",
    "timeline_set_scout": "1",
    "scout_dispose_uid": "1",
    "scout_dispose_must": "1",
    "job": "1",
    "ex_attribute": "1",
    "resist_elec": "1",
    "resist_fire": "1",
    "resist_stun": "1",
    "style": "1",
    "main_menu_bhv_set_id": "1",
    "main_menu_bhv_group_id": "1",
    "main_menu_bhv_action_id": "1",
    "card_index": "1",
    "chara_tag": "1",
    "face_picture_s": "1",
    "is_dlc": "1",
    "event_ofs_pos_x": "1",
    "event_ofs_pos_y": "1",
    "event_ofs_pos_z": "1",
    "event_ofs_rot_y": "1",
    "yaruki_point": "1"
  },
  "columnTypes": {
    "": -1,
    "initial_hp": 3,
    "initial_atk": 3,
    "initial_def": 3,
    "type": 2,
    "skill": 2,
    "kizuna_level": -1,
    "start_motion": -1,
    "personal_id": 1,
    "flavor_text": 13,
    "face_picture": 1,
    "Rarity": -1,
    "rarity": 2,
    "exp": 1,
    "kizuna_point": 1,
    "timeline_unacquired": -1,
    "timeline_can_get": -1,
    "timeline_get": -1,
    "timeline_dead": -1,
    "timeline_training": -1,
    "timeline_check_unacquired": 1,
    "timeline_check_acquirable": 1,
    "timeline_check_aquired": 1,
    "timeline_check_dead": 1,
    "timeline_check_training": 1,
    "timeline_set_acquirable": 1,
    "timeline_set_unacquired": 1,
    "timeline_set_aquired": 1,
    "timeline_set_dead": 1,
    "timeline_set_training": 1,
    "job_skill": 2,
    "timeline_set_scout": 1,
    "scout_dispose_uid": 8,
    "scout_dispose_must": 6,
    "job": 2,
    "ex_attribute": 2,
    "resist_elec": 6,
    "resist_fire": 6,
    "resist_stun": 6,
    "style": 13,
    "main_menu_bhv_set_id": 1,
    "main_menu_bhv_group_id": 2,
    "main_menu_bhv_action_id": 1,
    "card_index": 0,
    "chara_tag": 1,
    "face_picture_s": 1,
    "is_dlc": 6,
    "event_ofs_pos_x": 7,
    "event_ofs_pos_y": 7,
    "event_ofs_pos_z": 7,
    "event_ofs_rot_y": 7,
    "yaruki_point": 1
  },
  "COLUMN_INDICES": [
    8,
    1,
    2,
    3,
    34,
    4,
    5,
    30,
    12,
    13,
    14,
    51,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    31,
    32,
    33,
    27,
    28,
    29,
    9,
    10,
    45,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    46,
    47,
    48,
    49,
    50,
    19,
    18,
    17,
    16,
    15,
    11,
    7,
    6,
    0
  ]
}
'''
