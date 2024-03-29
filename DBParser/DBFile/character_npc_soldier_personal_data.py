from util import tree, get_entries, check_workspace, file_entry
import json
import random
import string


def generate_short_random_id(length=4):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def add_name_group_entry(c_name, name_group, name_string):
    m_group = str(name_group)
    group_name = list(c_name[m_group].keys())[0]
    new_index = c_name[m_group][group_name]["table"]["ROW_COUNT"]
    c_name[m_group][group_name]["table"][str(new_index)] = \
        {"": {"1": name_string, "2": 0, "reARMP_isValid": "1", "reARMP_rowIndex": new_index}}
    c_name[m_group][group_name]["table"]["ROW_COUNT"] += 1
    return new_index


def update_name_group_text_counts(mdict):
    for entry in [e for e in mdict if e.isdigit()]:
        unique_str_dict = {}
        group_name = list(mdict[entry].keys())[0]
        if not "table" in mdict[entry][group_name]: continue
        for nidx, nid in enumerate([e for e in mdict[entry][group_name]["table"] if e.isdigit()]):
            if "1" in mdict[entry][group_name]["table"][nid][""]:
                unique_str_dict[mdict[entry][group_name]["table"][nid][""]["1"]] = 0
        mdict[entry][group_name]["table"]["TEXT_COUNT"] = len(unique_str_dict) + int((len(unique_str_dict) > 0))


def prep_workspace(file_jsons):
    req_files = ["character_npc_soldier_personal_data",
                 "battle_ctrltype",
                 "character",
                 "asset_id",
                 "battle_ai_setting",
                 "character_npc_soldier_name_group"]
    if check_workspace(req_files, file_jsons): return
    soldier_personal = file_entry(file_jsons, "character_npc_soldier_personal_data", False)
    battle_ctrl_type = file_entry(file_jsons, "battle_ctrltype", False)
    character = file_entry(file_jsons, "character", False)
    asset_id = file_entry(file_jsons, "asset_id", False)
    battle_ai_setting = file_entry(file_jsons, "battle_ai_setting", False)
    c_name = file_entry(file_jsons, "character_npc_soldier_name_group", False)

    new_dict = tree()
    ctrl = get_entries(battle_ctrl_type)
    chara = get_entries(character)
    ai = get_entries(battle_ai_setting)

    for entry in [e for e in soldier_personal if e.isdigit()]:
        set_name = list(soldier_personal[entry].keys())[0]
        n_set_name = set_name
        if set_name in new_dict:
            n_set_name = f"{set_name} (UID: {generate_short_random_id()})"
            while n_set_name in new_dict:
                n_set_name = f"{set_name} (UID: {generate_short_random_id()})"
        new_dict[n_set_name] = soldier_personal[entry][set_name]

        new_dict[n_set_name].pop("reARMP_rowIndex")
        name_group = new_dict[n_set_name]["name_group"]
        name_id = new_dict[n_set_name]["name"]
        if isinstance(c_name.get(name_group, {}).get(name_id, {}), dict):
            new_dict[n_set_name]["name"] = None
        else:
            new_dict[n_set_name]["name"] = c_name[name_group][name_id]
        new_dict[n_set_name]["ctrltype"] = ctrl[new_dict[n_set_name]["ctrltype"]]
        new_dict[n_set_name]["chara"] = chara[new_dict[n_set_name]["chara"]]
        new_dict[n_set_name]["equip_l"] = asset_id[new_dict[n_set_name]["equip_l"]]
        new_dict[n_set_name]["equip_r"] = asset_id[new_dict[n_set_name]["equip_r"]]
        new_dict[n_set_name]["battle_ai_setting"] = ai[new_dict[n_set_name]["battle_ai_setting"]]
    file_jsons["Final"]["character_npc_soldier_personal_data"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["character_npc_soldier_personal_data",
                 "battle_ctrltype",
                 "character",
                 "asset_id",
                 "battle_ai_setting",
                 "character_npc_soldier_name_group"]
    if check_workspace(req_files, file_jsons): return
    soldier_personal = file_entry(file_jsons, "character_npc_soldier_personal_data")
    battle_ctrl_type = file_entry(file_jsons, "battle_ctrltype")
    character = file_entry(file_jsons, "character")
    asset_id = file_entry(file_jsons, "asset_id")
    battle_ai_setting = file_entry(file_jsons, "battle_ai_setting")
    c_name = file_jsons["puid"]["character_npc_soldier_name_group"]
    c_name_orig = file_entry(file_jsons, "character_npc_soldier_name_group")

    global base_json
    new_dict = tree()
    new_dict.update(json.loads(base_json))
    ctrl = get_entries(battle_ctrl_type, True)
    chara = get_entries(character, True)
    chara[""] = 0
    ai = get_entries(battle_ai_setting, True)
    ROW_COUNT = len(list(soldier_personal.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    name_update_bool = False
    for midx, entry in enumerate(list(soldier_personal.keys())):
        idx = str(midx)
        new_entry = entry.split("(")[0].strip()
        new_dict[idx][new_entry] = soldier_personal[entry]
        m_name = new_dict[idx][new_entry]["name"]
        m_n_group = new_dict[idx][new_entry]["name_group"]
        if not m_name:
            n_index = 0
        elif m_name not in c_name[m_n_group]:
            n_index = add_name_group_entry(c_name_orig, m_n_group, m_name)
            name_update_bool = True
        else:
            n_index = c_name[m_n_group][m_name]
        new_dict[idx][new_entry]["name"] = n_index
        new_dict[idx][new_entry]["ctrltype"] = ctrl[new_dict[idx][new_entry]["ctrltype"]]
        new_dict[idx][new_entry]["chara"] = chara[new_dict[idx][new_entry]["chara"]]
        new_dict[idx][new_entry]["equip_l"] = asset_id[new_dict[idx][new_entry]["equip_l"]]
        new_dict[idx][new_entry]["equip_r"] = asset_id[new_dict[idx][new_entry]["equip_r"]]
        new_dict[idx][new_entry]["battle_ai_setting"] = ai[new_dict[idx][new_entry]["battle_ai_setting"]]
        new_dict[idx][new_entry]["reARMP_rowIndex"] = midx
    if name_update_bool:
        update_name_group_text_counts(c_name_orig)
        file_jsons["Final"]["character_npc_soldier_name_group"] = c_name_orig
    file_jsons["Final"]["character_npc_soldier_personal_data"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 8328,
  "COLUMN_COUNT": 128,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": true,
  "TABLE_ID": 275,
  "STORAGE_MODE": 1,
  "SPECIAL_FIELD_INDICES": [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "columnValidity": {
    "": "0",
    "kind": "0",
    "ctrltype": "1",
    "name_group": "1",
    "name": "1",
    "force_kind": "1",
    "hp": "1",
    "keep_dead": "1",
    "chara": "1",
    "height": "1",
    "voicer": "1",
    "equip_l": "1",
    "equip_r": "1",
    "mission": "1",
    "group": "1",
    "power_ratio": "1",
    "muscle": "0",
    "agility": "0",
    "guts": "0",
    "technique": "0",
    "charm": "0",
    "stomach": "0",
    "npc_list": "1",
    "encounter_kind": "1",
    "ratio": "1",
    "timeline_category": "1",
    "timeline": "1",
    "open_clock": "1",
    "equip_pocket": "1",
    "magic_number": "1",
    "hide_map_icon": "1",
    "adjust_param": "1",
    "battle_level": "1",
    "scenario_id": "1",
    "find_voice_id": "1",
    "add_unsafe_value": "0",
    "is_dummy": "1",
    "sp": "1",
    "def_bash": "0",
    "def_slash": "0",
    "def_shot": "0",
    "def_fire": "0",
    "def_elec": "0",
    "def_ice": "0",
    "def_poison": "0",
    "enemy_id": "0",
    "enemy_level": "0",
    "drop_item": "0",
    "drop_ratio": "0",
    "exp_point": "0",
    "money_point": "0",
    "money_drop_ratio": "0",
    "job_exp_point": "0",
    "exp": "0",
    "attack": "0",
    "defence": "0",
    "dodge": "0",
    "accuracy": "0",
    "resist_charm": "0",
    "resist_sleep": "0",
    "transformed_chara": "0",
    "mp": "0",
    "transformed_list": "0",
    "drop_ratio_tbl": "0",
    "drop_item_tbl": "0",
    "drop_item_tbl[0]": "0",
    "drop_ratio_tbl[0]": "0",
    "drop_item_tbl[1]": "0",
    "drop_ratio_tbl[1]": "0",
    "sp_attack": "0",
    "event_priority": "0",
    "base_wait": "0",
    "sujimon_id": "0",
    "rpg_name": "0",
    "no_sujimon": "0",
    "ref_resist_param": "0",
    "resist_bleed": "0",
    "resist_burn": "0",
    "resist_cold": "0",
    "resist_paralysis": "0",
    "resist_poison": "0",
    "resist_piyori": "0",
    "resist_drunk": "0",
    "resist_terror": "0",
    "resist_mind_control": "0",
    "resist_anger": "0",
    "resist_silence": "0",
    "resist_death": "0",
    "resist_steal": "0",
    "resist_scrounge": "0",
    "resist_persuade": "0",
    "resist_bribery": "0",
    "resist_threaten": "0",
    "rare_drop_rate_tbl": "0",
    "rare_drop_item_tbl": "0",
    "ref_item_drop_tbl": "0",
    "drop_rate_tbl[0]": "0",
    "drop_rate_tbl[1]": "0",
    "rare_drop_item_tbl[0]": "0",
    "rare_drop_rate_tbl[0]": "0",
    "rare_item_steal_ratio": "0",
    "comment01": "0",
    "comment02": "0",
    "rare_drop_ratio_tbl": "0",
    "rare_drop_ratio_tbl[0]": "0",
    "priority_ref_name": "0",
    "rpg_name_id": "0",
    "is_appear_by_event": "0",
    "valid_skill_set": "0",
    "life_gauge_type": "1",
    "auto_guard": "0",
    "call_enemy_id": "0",
    "battle_ai_setting": "1",
    "drop_ma_counter": "1",
    "drop_disarm": "1",
    "is_no_break_asset": "1",
    "drop_dead": "1",
    "drop_difficulty": "1",
    "is_easy_bibiri": "1",
    "is_show_debug_create_fighter_menu": "0",
    "add_player_point_type_on_defeat": "1",
    "unlock_tropy_on_defeat": "1",
    "is_battle_mob": "1",
    "show_debug_create_fighter_menu_idx": "1",
    "is_force_enable_dead": "1",
    "is_no_use_sp_attack": "1",
    "is_need_tougijo_sound_direction": "1",
    "is_adjust_pre_attack_obstruct_collision": "1"
  },
  "columnTypes": {
    "": -1,
    "kind": -1,
    "ctrltype": 1,
    "name_group": 2,
    "name": 0,
    "force_kind": 6,
    "hp": 0,
    "keep_dead": 6,
    "chara": 1,
    "height": 2,
    "voicer": 1,
    "equip_l": 1,
    "equip_r": 1,
    "mission": 1,
    "group": 1,
    "power_ratio": 7,
    "muscle": -1,
    "agility": -1,
    "guts": -1,
    "technique": -1,
    "charm": -1,
    "stomach": -1,
    "npc_list": 1,
    "encounter_kind": 1,
    "ratio": 2,
    "timeline_category": 2,
    "timeline": 0,
    "open_clock": 0,
    "equip_pocket": 1,
    "magic_number": 5,
    "hide_map_icon": 6,
    "adjust_param": 2,
    "battle_level": 2,
    "scenario_id": 1,
    "find_voice_id": 2,
    "add_unsafe_value": -1,
    "is_dummy": 6,
    "sp": 3,
    "def_bash": -1,
    "def_slash": -1,
    "def_shot": -1,
    "def_fire": -1,
    "def_elec": -1,
    "def_ice": -1,
    "def_poison": -1,
    "enemy_id": -1,
    "enemy_level": -1,
    "drop_item": -1,
    "drop_ratio": -1,
    "exp_point": -1,
    "money_point": -1,
    "money_drop_ratio": -1,
    "job_exp_point": -1,
    "exp": -1,
    "attack": -1,
    "defence": -1,
    "dodge": -1,
    "accuracy": -1,
    "resist_charm": -1,
    "resist_sleep": -1,
    "transformed_chara": -1,
    "mp": -1,
    "transformed_list": -1,
    "drop_ratio_tbl": -1,
    "drop_item_tbl": -1,
    "drop_item_tbl[0]": -1,
    "drop_ratio_tbl[0]": -1,
    "drop_item_tbl[1]": -1,
    "drop_ratio_tbl[1]": -1,
    "sp_attack": -1,
    "event_priority": -1,
    "base_wait": -1,
    "sujimon_id": -1,
    "rpg_name": -1,
    "no_sujimon": -1,
    "ref_resist_param": -1,
    "resist_bleed": -1,
    "resist_burn": -1,
    "resist_cold": -1,
    "resist_paralysis": -1,
    "resist_poison": -1,
    "resist_piyori": -1,
    "resist_drunk": -1,
    "resist_terror": -1,
    "resist_mind_control": -1,
    "resist_anger": -1,
    "resist_silence": -1,
    "resist_death": -1,
    "resist_steal": -1,
    "resist_scrounge": -1,
    "resist_persuade": -1,
    "resist_bribery": -1,
    "resist_threaten": -1,
    "rare_drop_rate_tbl": -1,
    "rare_drop_item_tbl": -1,
    "ref_item_drop_tbl": -1,
    "drop_rate_tbl[0]": -1,
    "drop_rate_tbl[1]": -1,
    "rare_drop_item_tbl[0]": -1,
    "rare_drop_rate_tbl[0]": -1,
    "rare_item_steal_ratio": -1,
    "comment01": -1,
    "comment02": -1,
    "rare_drop_ratio_tbl": -1,
    "rare_drop_ratio_tbl[0]": -1,
    "priority_ref_name": -1,
    "rpg_name_id": -1,
    "is_appear_by_event": -1,
    "valid_skill_set": -1,
    "life_gauge_type": 2,
    "auto_guard": -1,
    "call_enemy_id": -1,
    "battle_ai_setting": 1,
    "drop_ma_counter": 1,
    "drop_disarm": 1,
    "is_no_break_asset": 6,
    "drop_dead": 1,
    "drop_difficulty": 2,
    "is_easy_bibiri": 6,
    "is_show_debug_create_fighter_menu": -1,
    "add_player_point_type_on_defeat": 1,
    "unlock_tropy_on_defeat": 1,
    "is_battle_mob": 6,
    "show_debug_create_fighter_menu_idx": 2,
    "is_force_enable_dead": 6,
    "is_no_use_sp_attack": 6,
    "is_need_tougijo_sound_direction": 6,
    "is_adjust_pre_attack_obstruct_collision": 6
  },
  "COLUMN_INDICES": [
    36,
    13,
    14,
    2,
    5,
    29,
    31,
    32,
    109,
    37,
    34,
    3,
    4,
    6,
    15,
    28,
    8,
    22,
    30,
    7,
    9,
    10,
    11,
    12,
    23,
    24,
    25,
    26,
    27,
    33,
    112,
    115,
    113,
    114,
    116,
    117,
    118,
    123,
    120,
    121,
    122,
    124,
    125,
    126,
    127,
    119,
    111,
    110,
    108,
    107,
    106,
    105,
    104,
    103,
    102,
    101,
    100,
    99,
    98,
    97,
    96,
    95,
    94,
    93,
    92,
    91,
    90,
    89,
    88,
    87,
    86,
    85,
    84,
    83,
    82,
    81,
    80,
    79,
    78,
    77,
    76,
    75,
    74,
    73,
    72,
    71,
    70,
    69,
    68,
    67,
    66,
    65,
    64,
    63,
    62,
    61,
    60,
    59,
    58,
    57,
    56,
    55,
    54,
    53,
    52,
    51,
    50,
    49,
    48,
    47,
    46,
    45,
    44,
    43,
    42,
    41,
    40,
    39,
    38,
    35,
    21,
    20,
    19,
    18,
    17,
    16,
    1,
    0
  ]
}
'''
