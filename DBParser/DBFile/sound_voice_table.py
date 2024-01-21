from util import tree, get_entries, import_json, get_file_information, check_workspace, file_entry
import json
from collections import OrderedDict
from copy import deepcopy


def sort_dict_by_puid(mdict, mot):
    to_sort = {}
    keys_to_remove = []
    for cur_anim in mdict:
        to_sort[cur_anim] = {"SortKey": mot[cur_anim], "Dict": mdict[cur_anim]}
    to_sort = dict(sorted(to_sort.items(), key=lambda item: item[1]["SortKey"]))
    result_dict = {key: to_sort[key]["Dict"] for key in to_sort}
    return result_dict


def get_sound_se_id(sound_se_id, rev=False):
    se_dict = {}
    for se_entry in [e for e in sound_se_id["subTable"] if e.isdigit()]:
        se_name = list(sound_se_id["subTable"][se_entry].keys())[0]
        m_table = sound_se_id["subTable"][se_entry][se_name]["2"]
        cur_seid = sound_se_id[str(m_table)][""]["2"]
        se_dict[cur_seid] = se_name
    if rev: se_dict = {v: k for k, v in se_dict.items()}
    return se_dict


def prep_workspace(file_jsons):
    req_files = ["sound_voice_table",
                 "sound_voicer",
                 "sound_category",
                 "sound_se_all_id_to_id"]
    if check_workspace(req_files, file_jsons): return
    sound_voice_blow = file_entry(file_jsons, "sound_voice_table", False)
    sound_voicer = file_entry(file_jsons, "sound_voicer", False)
    sound_category = file_entry(file_jsons, "sound_category", False)
    sound_se_all_id_to_id = file_entry(file_jsons, "sound_se_all_id_to_id")

    new_dict = tree()
    voicer = get_entries(sound_voicer)
    sound_cats = get_entries(sound_category)
    se_id = get_sound_se_id(sound_se_all_id_to_id)
    for cat_num in [e for e in sound_voice_blow["subTable"] if e.isdigit()]:
        category = list(sound_voice_blow["subTable"][cat_num].keys())[0]
        for entry in [e for e in sound_voice_blow["subTable"][cat_num][category]["1"] if e.isdigit()]:
            voicer_name = list(sound_voice_blow["subTable"][cat_num][category]["1"][entry].keys())[0]
            for sound_entry in [e for e in sound_voice_blow["subTable"][cat_num][category]["1"][entry][voicer_name]["1"] if e.isdigit()]:
                sound_id = list(sound_voice_blow["subTable"][cat_num][category]["1"][entry][voicer_name]["1"][sound_entry].keys())[0]
                voice_table = str(sound_voice_blow["subTable"][cat_num][category]["1"][entry][voicer_name]["1"][sound_entry][sound_id]["2"])
                sound_eff_id = sound_voice_blow[voice_table][""]["se_id"]
                if sound_eff_id in se_id:
                    new_dict[category][voicer_name][sound_id] = se_id[sound_eff_id]
                else:
                    new_dict[category][voicer_name][sound_id] = sound_eff_id
    file_jsons["Final"]["sound_voice_table"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["sound_voice_table",
                 "sound_voicer",
                 "sound_category",
                 "sound_se_all_id_to_id"]
    if check_workspace(req_files, file_jsons): return
    sound_voice_table = file_entry(file_jsons, "sound_voice_table")
    sound_voicer = file_entry(file_jsons, "sound_voicer")
    sound_category = file_entry(file_jsons, "sound_category")
    sound_se_all_id_to_id = file_entry(file_jsons, "sound_se_all_id_to_id")

    global base_json
    global sub_json
    global sub_sub_json
    global entry_json
    new_dict = tree()
    sub_dict = tree()
    voicer_dict = tree()

    entry_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    voicer_dict.update(json.loads(entry_json))
    entry_dict.update(json.loads(sub_sub_json))

    voicer = get_entries(sound_voicer, True)
    sound_cats = get_entries(sound_category, True)
    se_id = get_sound_se_id(sound_se_all_id_to_id, True)
    cur_main_id = 0

    sound_voice_table = sort_dict_by_puid(sound_voice_table, sound_cats)
    for sound_cat in sound_voice_table:
        sound_voice_table[sound_cat] = sort_dict_by_puid(sound_voice_table[sound_cat], voicer)

    sub_row_count = 0
    for cat_idx, category in enumerate(list(sound_voice_table.keys())):
        sub_row_count = cat_idx + 1
        first_id_cat = cur_main_id
        cat = str(cat_idx)
        group_id = sound_cats[category]
        sub_dict[cat][category]["0"] = group_id
        m_c_dict = deepcopy(entry_dict)
        for idx, voice_name in enumerate(list(sound_voice_table[category].keys())):
            m_c_dict["ROW_COUNT"] = idx + 1
            first_id = cur_main_id
            midx = str(idx)
            cur_voicer_id = voicer[voice_name]
            m_c_dict[midx][voice_name]["0"] = cur_voicer_id
            m_v_dict = deepcopy(voicer_dict)
            for sound_idx, sound_id in enumerate(list(sound_voice_table[category][voice_name].keys())):
                m_v_dict["ROW_COUNT"] = sound_idx + 1
                sidx = str(sound_idx)
                cur_se_id = sound_voice_table[category][voice_name][sound_id]
                main_idx = str(cur_main_id)
                m_v_dict[sidx][sound_id]["0"] = int(sound_id)
                m_v_dict[sidx][sound_id]["2"] = cur_main_id
                new_dict[main_idx][""]["*"] = group_id
                new_dict[main_idx][""]["**"] = cur_voicer_id
                new_dict[main_idx][""]["***"] = int(sound_id)
                if cur_se_id in se_id:
                    new_dict[main_idx][""]["se_id"] = se_id[cur_se_id]
                elif isinstance(cur_se_id, int):
                    new_dict[main_idx][""]["se_id"] = cur_se_id
                else:
                    print(f"{cur_se_id} string not in sound_se_all_id_to_id. Value will be written as 0.")
                    new_dict[main_idx][""]["se_id"] = 0
                cur_main_id += 1
            m_c_dict[midx][voice_name]["1"] = deepcopy(m_v_dict)
            m_c_dict[midx][voice_name]["2"] = first_id
        sub_dict[cat][category]["1"] = deepcopy(m_c_dict)
        sub_dict[cat][category]["2"] = first_id_cat
    sub_dict["ROW_COUNT"] = sub_row_count
    new_dict["ROW_COUNT"] = cur_main_id
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["sound_voice_table"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 6,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 54,
  "STORAGE_MODE": 0,
  "columnValidity": {
    "": "0",
    "*": "1",
    "**": "1",
    "***": "1",
    "se_id": "1",
    "se_name": "0"
  },
  "columnTypes": {
    "": -1,
    "*": 2,
    "**": 1,
    "***": 0,
    "se_id": 0,
    "se_name": -1
  },
  "COLUMN_INDICES": [
    1,
    2,
    3,
    4,
    5,
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

sub_sub_json = '''
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

entry_json = '''
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
