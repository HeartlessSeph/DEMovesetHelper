from util import tree, get_entries, get_file_information, file_entry, check_workspace
import json


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
    req_files = ["battle_ctrltype", "asset_id", "File Information", "battle_ai_setting", "character"]
    if check_workspace(req_files, file_jsons): return
    ctrltype = file_entry(file_jsons, "battle_ctrltype", False)
    file_information = file_entry(file_jsons, "File Information", False)
    asset_id = file_entry(file_jsons, "asset_id", False)
    battle_ai_setting = file_entry(file_jsons, "battle_ai_setting", False)
    character = file_entry(file_jsons, "character", False)

    new_dict = tree()
    file_info = get_file_information(file_information)
    ai = get_entries(battle_ai_setting)
    chara = get_unique_entries(character)
    for entry in [e for e in ctrltype if e.isdigit()]:
        set_name = list(ctrltype[entry].keys())[0]
        new_dict[set_name] = ctrltype[entry][set_name]

        new_dict[set_name].pop("reARMP_rowIndex")
        new_dict[set_name]["command_set"] = file_info[new_dict[set_name]["command_set"]]
        new_dict[set_name]["weapon"] = asset_id[new_dict[set_name]["weapon"]]
        new_dict[set_name]["weapon_l"] = asset_id[new_dict[set_name]["weapon_l"]]
        new_dict[set_name]["ai_param"] = ai[new_dict[set_name]["ai_param"]]
        new_dict[set_name]["chara_id"] = chara[new_dict[set_name]["chara_id"]]
    file_jsons["Final"]["battle_ctrltype"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["battle_ctrltype", "asset_id", "File Information", "battle_ai_setting", "character"]
    if check_workspace(req_files, file_jsons): return
    ctrltype = file_entry(file_jsons, "battle_ctrltype")
    file_information = file_entry(file_jsons, "File Information")
    asset_id = file_entry(file_jsons, "asset_id")
    battle_ai_setting = file_entry(file_jsons, "battle_ai_setting")
    character = file_entry(file_jsons, "character")

    global base_json
    new_dict = tree()
    new_dict.update(json.loads(base_json))
    file_info = get_file_information(file_information, True)
    ai = get_entries(battle_ai_setting, True)
    chara = get_unique_entries(character, True)
    chara[""] = 0
    ROW_COUNT = len(list(ctrltype.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    for midx, entry in enumerate(list(ctrltype.keys())):
        idx = str(midx)
        new_dict[idx][entry] = ctrltype[entry]
        new_dict[idx][entry]["command_set"] = file_info[new_dict[idx][entry]["command_set"]]
        new_dict[idx][entry]["weapon"] = asset_id[new_dict[idx][entry]["weapon"]]
        new_dict[idx][entry]["weapon_l"] = asset_id[new_dict[idx][entry]["weapon_l"]]
        new_dict[idx][entry]["ai_param"] = ai[new_dict[idx][entry]["ai_param"]]
        new_dict[idx][entry]["chara_id"] = chara[new_dict[idx][entry]["chara_id"]]
        new_dict[idx][entry]["reARMP_rowIndex"] = midx
    file_jsons["Final"]["battle_ctrltype"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 255,
  "COLUMN_COUNT": 11,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": true,
  "TABLE_ID": 289,
  "STORAGE_MODE": 1,
  "columnValidity": {
    "": "0",
    "command_set": "1",
    "is_boss": "1",
    "chara_id": "1",
    "fighter_type": "1",
    "weapon": "1",
    "hp_max": "1",
    "is_npc": "1",
    "ai_param": "1",
    "weapon_l": "1",
    "dbg_list_filter_id": "1"
  },
  "columnTypes": {
    "": -1,
    "command_set": 1,
    "is_boss": 6,
    "chara_id": 1,
    "fighter_type": 2,
    "weapon": 1,
    "hp_max": 0,
    "is_npc": 6,
    "ai_param": 1,
    "weapon_l": 1,
    "dbg_list_filter_id": 2
  },
  "COLUMN_INDICES": [
    1,
    2,
    3,
    4,
    5,
    9,
    6,
    8,
    7,
    10,
    0
  ]
}
'''
