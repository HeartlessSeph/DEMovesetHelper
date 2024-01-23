from util import tree, get_entries, check_workspace, file_entry
import json


def prep_workspace(file_jsons):
    req_files = ["sound_voicer"]
    if check_workspace(req_files, file_jsons): return
    sound_voicer = file_entry(file_jsons, "sound_voicer", False)

    new_dict = tree()
    for entry in [e for e in sound_voicer if e.isdigit()]:
        set_name = list(sound_voicer[entry].keys())[0]
        new_dict[set_name] = sound_voicer[entry][set_name]
        new_dict[set_name].pop("reARMP_rowIndex")
    file_jsons["Final"]["sound_voicer"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["sound_voicer"]
    if check_workspace(req_files, file_jsons): return
    sound_voicer = file_entry(file_jsons, "sound_voicer")

    global base_json
    new_dict = tree()
    new_dict.update(json.loads(base_json))
    ROW_COUNT = len(list(sound_voicer.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    for midx, entry in enumerate(list(sound_voicer.keys())):
        new_dict[str(midx)][entry] = sound_voicer[entry]
        new_dict[str(midx)][entry]["reARMP_rowIndex"] = midx
    file_jsons["Final"]["sound_voicer"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 0,
  "COLUMN_COUNT": 11,
  "TEXT_COUNT": 12,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": true,
  "TABLE_ID": 40,
  "STORAGE_MODE": 0,
  "columnValidity": {
    "": "0",
    "data0": "0",
    "sex": "1",
    "job_kind1": "0",
    "job_kind2": "0",
    "job_kind3": "0",
    "job_kind4": "0",
    "expression_chara": "0",
    "message_se_cuesheet": "1",
    "message_se_cue": "1",
    "voice_type": "1"
  },
  "columnTypes": {
    "": -1,
    "data0": -1,
    "sex": 2,
    "job_kind1": -1,
    "job_kind2": -1,
    "job_kind3": -1,
    "job_kind4": -1,
    "expression_chara": -1,
    "message_se_cuesheet": 1,
    "message_se_cue": 1,
    "voice_type": 13
  },
  "COLUMN_INDICES": [
    2,
    8,
    9,
    10,
    7,
    6,
    5,
    4,
    3,
    1,
    0
  ]
}
'''
