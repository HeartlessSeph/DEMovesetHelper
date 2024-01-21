from util import tree, get_entries, check_workspace, file_entry
import json


def prep_workspace(file_jsons):
    req_files = ["battle_motion_group", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    motion_group = file_entry(file_jsons, "battle_motion_group", False)
    motion_gmt = file_entry(file_jsons, "motion_gmt", False)

    new_dict = tree()
    mot = get_entries(motion_gmt)
    for entry in [e for e in motion_group if e.isdigit()]:
        set_name = list(motion_group[entry].keys())[0]
        for set_entry in motion_group[entry][set_name]:
            if set_entry not in ["reARMP_isValid", "mot_tbl", "reARMP_rowIndex"]:
                new_dict[set_name][set_entry] = mot[motion_group[entry][set_name][set_entry]]
            elif set_entry != "reARMP_rowIndex":
                new_dict[set_name][set_entry] = motion_group[entry][set_name][set_entry]
    file_jsons["Final"]["battle_motion_group"] = new_dict
    return


def prep_build(file_jsons):
    req_files = ["battle_motion_group", "motion_gmt"]
    if check_workspace(req_files, file_jsons): return
    motion_group = file_entry(file_jsons, "battle_motion_group")
    motion_gmt = file_entry(file_jsons, "motion_gmt")

    global base_json
    new_dict = tree()
    new_dict.update(json.loads(base_json))
    mot = get_entries(motion_gmt, True)
    ROW_COUNT = len(list(motion_group.keys()))
    new_dict["ROW_COUNT"] = ROW_COUNT
    for midx, entry in enumerate(list(motion_group.keys())):
        for sub_entry in motion_group[entry]:
            if sub_entry not in ["reARMP_isValid", "mot_tbl", "reARMP_rowIndex"]:
                motion_group[entry][sub_entry] = mot[motion_group[entry][sub_entry]]
            new_dict[str(midx)][entry][sub_entry] = motion_group[entry][sub_entry]
        new_dict[str(midx)][entry]["reARMP_rowIndex"] = midx
    file_jsons["Final"]["battle_motion_group"] = new_dict
    return


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 54,
  "COLUMN_COUNT": 23,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": true,
  "TABLE_ID": 3978,
  "STORAGE_MODE": 1,
  "SPECIAL_FIELD_INDICES": [
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
    0
  ],
  "columnValidity": {
    "": "0",
    "mot_tbl": "1",
    "mot_tbl[0]": "1",
    "mot_tbl[1]": "1",
    "mot_tbl[2]": "1",
    "mot_tbl[3]": "1",
    "mot_tbl[4]": "1",
    "mot_tbl[5]": "1",
    "mot_tbl[6]": "1",
    "mot_tbl[7]": "1",
    "mot_tbl[8]": "1",
    "mot_tbl[9]": "1",
    "mot_tbl[10]": "1",
    "mot_tbl[11]": "1",
    "mot_tbl[12]": "1",
    "mot_tbl[13]": "1",
    "mot_tbl[14]": "1",
    "mot_tbl[15]": "1",
    "mot_tbl[16]": "1",
    "mot_tbl[17]": "1",
    "mot_tbl[18]": "1",
    "mot_tbl[19]": "1",
    "mot_tbl[20]": "1"
  },
  "columnTypes": {
    "": -1,
    "mot_tbl": 16,
    "mot_tbl[0]": 1,
    "mot_tbl[1]": 1,
    "mot_tbl[2]": 1,
    "mot_tbl[3]": 1,
    "mot_tbl[4]": 1,
    "mot_tbl[5]": 1,
    "mot_tbl[6]": 1,
    "mot_tbl[7]": 1,
    "mot_tbl[8]": 1,
    "mot_tbl[9]": 1,
    "mot_tbl[10]": 1,
    "mot_tbl[11]": 1,
    "mot_tbl[12]": 1,
    "mot_tbl[13]": 1,
    "mot_tbl[14]": 1,
    "mot_tbl[15]": 1,
    "mot_tbl[16]": 1,
    "mot_tbl[17]": 1,
    "mot_tbl[18]": 1,
    "mot_tbl[19]": 1,
    "mot_tbl[20]": 1
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
    0
  ]
}
'''
