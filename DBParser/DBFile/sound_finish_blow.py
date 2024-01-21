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


def sort_dict_by_voicer(mdict, voicer):
    to_sort = {}
    keys_to_remove = []
    for cur_voicer in mdict:
        to_sort[cur_voicer] = {"SortKey": voicer[cur_voicer], "Dict": mdict[cur_voicer]}
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
    req_files = ["sound_finish_blow",
                 "sound_cuesheet",
                 "sound_voicer",
                 "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    sound_finish_blow = file_entry(file_jsons, "sound_finish_blow", False)
    cuesheet = file_entry(file_jsons, "sound_cuesheet", False)
    sound_voicer = file_entry(file_jsons, "sound_voicer", False)

    new_dict = tree()
    cues = get_entries(cuesheet)
    voicer = get_entries(sound_voicer)
    for cat_num in [e for e in sound_finish_blow["subTable"] if e.isdigit()]:
        category = list(sound_finish_blow["subTable"][cat_num].keys())[0]
        for entry in [e for e in sound_finish_blow["subTable"][cat_num][category]["1"] if e.isdigit()]:
            motion_name = list(sound_finish_blow["subTable"][cat_num][category]["1"][entry].keys())[0]
            motion_table = str(sound_finish_blow["subTable"][cat_num][category]["1"][entry][motion_name]["2"])
            new_dict[category][motion_name] = deepcopy(sound_finish_blow[motion_table][""])
            new_dict[category][motion_name]["cuesheet"] = cues[new_dict[category][motion_name]["cuesheet"]]
    file_jsons["Final"]["sound_finish_blow"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["sound_finish_blow",
                 "motion_gmt",
                 "sound_cuesheet",
                 "sound_voicer"]
    if check_workspace(req_files, file_jsons): return
    sound_finish_blow = file_entry(file_jsons, "sound_finish_blow")
    motion_gmt = file_entry(file_jsons, "motion_gmt")
    cuesheet = file_entry(file_jsons, "sound_cuesheet")
    sound_voicer = file_entry(file_jsons, "sound_voicer")

    global base_json
    global sub_json
    global sub_sub_json
    global entry_json
    new_dict = tree()
    sub_dict = tree()

    entry_dict = tree()
    new_dict.update(json.loads(base_json))
    sub_dict.update(json.loads(sub_json))
    entry_dict.update(json.loads(entry_json))

    mot = get_entries(motion_gmt, True)
    cues = get_entries(cuesheet, True)
    voicer = get_entries(sound_voicer, True)
    main_entry_list = []
    sound_finish_blow = sort_dict_by_voicer(sound_finish_blow, voicer)

    for cat_idx, category in enumerate(list(sound_finish_blow.keys())):
        ROW_COUNT = len(sound_finish_blow[category]) - 1
        sub_sub_dict = tree()
        sub_sub_dict.update(json.loads(sub_sub_json))
        cat = str(cat_idx)
        sub_dict[cat][category]["0"] = voicer[category]
        sub_dict[cat][category]["1"] = sub_sub_dict
        sub_dict[cat][category]["2"] = 0
        sub_dict[cat][category]["1"]["ROW_COUNT"] = ROW_COUNT

    for category in sound_finish_blow:
        for entry in sound_finish_blow[category]:
            sound_finish_blow[category][entry]["cuesheet"] = cues[sound_finish_blow[category][entry]["cuesheet"]]
            main_entry_list.append(sound_finish_blow[category][entry])
    main_entry_list = remove_duplicates(main_entry_list)
    for cat_idx, category in enumerate(list(sound_finish_blow.keys())):
        for entry in sound_finish_blow[category]:
            entry_ref = find_matching_index(main_entry_list, sound_finish_blow[category][entry])
            sound_finish_blow[category][entry] = entry_ref
        temp_list = []
        for entry in sound_finish_blow[category]:
            temp_list.append(sound_finish_blow[category][entry])
        temp_list.sort()
        sub_dict[str(cat_idx)][category]["2"] = temp_list[0]

    for category in sound_finish_blow:
        temp_dict = sound_finish_blow[category]
        temp_dict = sort_dict_by_motion(temp_dict, mot)
        sound_finish_blow[category] = temp_dict

    main_ROW_COUNT = len(main_entry_list)
    new_dict["ROW_COUNT"] = main_ROW_COUNT
    sub_ROW_COUNT = len(list(sound_finish_blow.keys()))
    sub_dict["ROW_COUNT"] = sub_ROW_COUNT
    for idx, entry in enumerate(main_entry_list):
        new_dict[str(idx)][""] = entry

    for cat_idx, category in enumerate(list(sound_finish_blow.keys())):
        cat = str(cat_idx)
        for idx, entry in enumerate(list(sound_finish_blow[category].keys())):
            midx = str(idx)
            entry_ref = sound_finish_blow[category][entry]
            sub_dict[cat][category]["1"][midx][entry]["0"] = mot[entry]
            sub_dict[cat][category]["1"][midx][entry]["1"] = json.loads(entry_json)
            sub_dict[cat][category]["1"][midx][entry]["2"] = entry_ref
            sub_dict[cat][category]["1"][midx][entry]["1"]["0"][""]["2"] = entry_ref
    new_dict["subTable"] = sub_dict
    file_jsons["Final"]["sound_finish_blow"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 8,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": -1,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": false,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": false,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 2408,
  "STORAGE_MODE": 1,
  "columnValidity": {
    "": "0",
    "*": "1",
    "**": "1",
    "cuesheet": "1",
    "cue": "1",
    "comment2": "0",
    "comment3": "0",
    "***": "1"
  },
  "columnTypes": {
    "": -1,
    "*": 1,
    "**": 1,
    "cuesheet": 1,
    "cue": 1,
    "comment2": -1,
    "comment3": -1,
    "***": 1
  },
  "COLUMN_INDICES": [
    1,
    2,
    7,
    3,
    4,
    5,
    6,
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
"ROW_COUNT": 1,
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
},
"0": {
  "": {
    "0": 0,
    "2": 0
  }
}
}
'''
