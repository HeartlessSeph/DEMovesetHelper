from util import tree, get_entries
import json


def add_column(fighter_info, new_select_match):
    new_match = f"select_match[{new_select_match}]"
    cur_idx = 2
    while new_match in fighter_info["columnValidity"]:
        new_match = f"select_match{str(cur_idx)}[{new_select_match}]"
        cur_idx += 1
    fighter_info["columnValidity"][new_match] = "1"
    fighter_info["columnTypes"][new_match] = 2
    fighter_info["COLUMN_COUNT"] += 1
    fighter_info["COLUMN_INDICES"].append(len(fighter_info["COLUMN_INDICES"]))
    for entry in [e for e in fighter_info if e.isdigit()]:
        f_name = list(fighter_info[entry].keys())[0]
        my_dict = fighter_info[entry][f_name]
        my_dict = list(my_dict.items())
        my_dict.insert(-2, (new_match, 0))
        my_dict = dict(my_dict)
        fighter_info[entry][f_name] = my_dict
    return fighter_info


base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 218,
  "COLUMN_COUNT": 123,
  "TEXT_COUNT": 47,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": 0,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": true,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": true,
  "TABLE_ID": 1620,
  "STORAGE_MODE": 1,
  "SPECIAL_FIELD_INDICES": [
    0,
    14,
    0,
    0,
    17,
    18,
    19,
    20,
    0,
    22,
    23,
    24,
    0,
    26,
    27,
    28,
    0,
    30,
    31,
    32,
    0,
    34,
    35,
    36,
    0,
    38,
    39,
    40,
    0,
    42,
    43,
    44,
    0,
    46,
    47,
    48,
    0,
    0,
    0,
    0,
    0,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    86,
    87,
    88,
    120,
    121,
    122,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    94,
    0,
    95,
    0,
    96,
    0,
    97,
    0,
    98,
    0,
    99,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    100,
    101,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    103,
    0,
    104,
    0,
    105,
    0,
    106,
    0,
    107,
    0,
    108,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    109,
    110,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    112,
    113,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    115,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    117,
    0
  ],
  "columnValidity": {
    "": "0",
    "name": "1",
    "soldier_id": "1",
    "catch_phrase": "0",
    "picture": "1",
    "picture_small": "1",
    "nationality": "0",
    "battle_style": "0",
    "clear_flag": "0",
    "detail_text": "0",
    "unlock_flag": "0",
    "is_sude": "1",
    "is_amon": "1",
    "select_match": "1",
    "select_match[normal1]": "1",
    "select_match[normal2]": "0",
    "select_match[normal3]": "0",
    "select_match[test]": "1",
    "select_match[ippan_r1_1]": "1",
    "select_match[ippan_r1_2]": "1",
    "select_match[ippan_r1_3]": "1",
    "select_match[ippan_r1_4]": "0",
    "select_match[ippan_r2_1]": "1",
    "select_match[ippan_r2_2]": "1",
    "select_match[ippan_r2_3]": "1",
    "select_match[ippan_r2_4]": "0",
    "select_match[ippan_r3_1]": "1",
    "select_match[ippan_r3_2]": "1",
    "select_match[ippan_r3_3]": "1",
    "select_match[ippan_r3_4]": "0",
    "select_match[ippan_r4_1]": "1",
    "select_match[ippan_r4_2]": "1",
    "select_match[ippan_r4_3]": "1",
    "select_match[ippan_r4_4]": "0",
    "select_match[ransen_r1_1]": "1",
    "select_match[ransen_r1_2]": "1",
    "select_match[ransen_r1_3]": "1",
    "select_match[ransen_r1_4]": "0",
    "select_match[ransen_r2_1]": "1",
    "select_match[ransen_r2_2]": "1",
    "select_match[ransen_r2_3]": "1",
    "select_match[ransen_r2_4]": "0",
    "select_match[ransen_r3_1]": "1",
    "select_match[ransen_r3_2]": "1",
    "select_match[ransen_r3_3]": "1",
    "select_match[ransen_r3_4]": "0",
    "select_match[ransen_r4_1]": "1",
    "select_match[ransen_r4_2]": "1",
    "select_match[ransen_r4_3]": "1",
    "select_match[ransen_r4_4]": "0",
    "select_match[rangoku_r1_1]": "0",
    "select_match[rangoku_r1_2]": "0",
    "select_match[rangoku_r1_3]": "0",
    "select_match[rangoku_r1_4]": "0",
    "select_match[rangoku_r2_1]": "1",
    "select_match[rangoku_r2_2]": "1",
    "select_match[rangoku_r2_3]": "1",
    "select_match[rangoku_r2_4]": "1",
    "select_match[rangoku_r3_1]": "1",
    "select_match[rangoku_r3_2]": "1",
    "select_match[rangoku_r3_3]": "1",
    "select_match[rangoku_r3_4]": "1",
    "select_match[rangoku_r4_1]": "1",
    "select_match[rangoku_r4_2]": "1",
    "select_match[rangoku_r4_3]": "1",
    "select_match[rangoku_r4_4]": "1",
    "select_match[saiten_r1_1]": "1",
    "select_match[saiten_r2_1]": "1",
    "select_match[saiten_r3_1]": "1",
    "select_match[saiten_r4_1]": "1",
    "is_mikata": "1",
    "group": "1",
    "select_match[rangoku_r2_5]": "1",
    "select_match[rangoku_r3_5]": "1",
    "select_match[rangoku_r4_5]": "1",
    "select_match[rangoku_r4_6]": "1",
    "select_match[rangoku_r4_7]": "1",
    "select_match[saiten_r4_2]": "1",
    "select_match[saiten_r4_3]": "1",
    "select_match[saiten_r1_2]": "1",
    "select_match[saiten_r1_3]": "1",
    "select_match[saiten_r1_4]": "1",
    "start_motion": "0",
    "start_bhv_set_id": "1",
    "start_bhv_group_id": "1",
    "start_bhv_action_id": "1",
    "select_match[rangoku_r4_8]": "1",
    "select_match[rangoku_r4_9]": "1",
    "select_match[rangoku_r4_10]": "1",
    "vs_bhv_set_id": "1",
    "vs_bhv_group_id": "1",
    "vs_bhv_action_id": "1",
    "select_match2[ippan_r1_1]": "0",
    "select_match2": "1",
    "select_match2[ippan_r2_1]": "1",
    "select_match2[ippan_r2_3]": "1",
    "select_match2[ippan_r3_1]": "1",
    "select_match2[ippan_r3_3]": "1",
    "select_match2[ippan_r4_1]": "1",
    "select_match2[ippan_r4_3]": "1",
    "select_match2[saiten_r4_2]": "1",
    "select_match2[saiten_r4_3]": "1",
    "select_match3": "1",
    "select_match3[ippan_r2_1]": "1",
    "select_match3[ippan_r2_3]": "1",
    "select_match3[ippan_r3_1]": "1",
    "select_match3[ippan_r3_3]": "1",
    "select_match3[ippan_r4_1]": "1",
    "select_match3[ippan_r4_3]": "1",
    "select_match3[saiten_r4_2]": "1",
    "select_match3[saiten_r4_3]": "1",
    "select_match4": "1",
    "select_match4[saiten_r4_2]": "1",
    "select_match4[saiten_r4_3]": "1",
    "select_match5": "1",
    "select_match5[saiten_r4_3]": "1",
    "select_match6": "1",
    "select_match6[saiten_r4_3]": "1",
    "style": "1",
    "start_gmt": "1",
    "select_match[arena_btl04_0100]": "1",
    "select_match[arena_btl07_0100]": "1",
    "select_match[arena_btl10_0100]": "1"
  },
  "columnTypes": {
    "": -1,
    "name": 13,
    "soldier_id": 1,
    "catch_phrase": -1,
    "picture": 1,
    "picture_small": 1,
    "nationality": -1,
    "battle_style": -1,
    "clear_flag": -1,
    "detail_text": -1,
    "unlock_flag": -1,
    "is_sude": 6,
    "is_amon": 6,
    "select_match": 14,
    "select_match[normal1]": 2,
    "select_match[normal2]": -1,
    "select_match[normal3]": -1,
    "select_match[test]": 2,
    "select_match[ippan_r1_1]": 2,
    "select_match[ippan_r1_2]": 2,
    "select_match[ippan_r1_3]": 2,
    "select_match[ippan_r1_4]": -1,
    "select_match[ippan_r2_1]": 2,
    "select_match[ippan_r2_2]": 2,
    "select_match[ippan_r2_3]": 2,
    "select_match[ippan_r2_4]": -1,
    "select_match[ippan_r3_1]": 2,
    "select_match[ippan_r3_2]": 2,
    "select_match[ippan_r3_3]": 2,
    "select_match[ippan_r3_4]": -1,
    "select_match[ippan_r4_1]": 2,
    "select_match[ippan_r4_2]": 2,
    "select_match[ippan_r4_3]": 2,
    "select_match[ippan_r4_4]": -1,
    "select_match[ransen_r1_1]": 2,
    "select_match[ransen_r1_2]": 2,
    "select_match[ransen_r1_3]": 2,
    "select_match[ransen_r1_4]": -1,
    "select_match[ransen_r2_1]": 2,
    "select_match[ransen_r2_2]": 2,
    "select_match[ransen_r2_3]": 2,
    "select_match[ransen_r2_4]": -1,
    "select_match[ransen_r3_1]": 2,
    "select_match[ransen_r3_2]": 2,
    "select_match[ransen_r3_3]": 2,
    "select_match[ransen_r3_4]": -1,
    "select_match[ransen_r4_1]": 2,
    "select_match[ransen_r4_2]": 2,
    "select_match[ransen_r4_3]": 2,
    "select_match[ransen_r4_4]": -1,
    "select_match[rangoku_r1_1]": -1,
    "select_match[rangoku_r1_2]": -1,
    "select_match[rangoku_r1_3]": -1,
    "select_match[rangoku_r1_4]": -1,
    "select_match[rangoku_r2_1]": 2,
    "select_match[rangoku_r2_2]": 2,
    "select_match[rangoku_r2_3]": 2,
    "select_match[rangoku_r2_4]": 2,
    "select_match[rangoku_r3_1]": 2,
    "select_match[rangoku_r3_2]": 2,
    "select_match[rangoku_r3_3]": 2,
    "select_match[rangoku_r3_4]": 2,
    "select_match[rangoku_r4_1]": 2,
    "select_match[rangoku_r4_2]": 2,
    "select_match[rangoku_r4_3]": 2,
    "select_match[rangoku_r4_4]": 2,
    "select_match[saiten_r1_1]": 2,
    "select_match[saiten_r2_1]": 2,
    "select_match[saiten_r3_1]": 2,
    "select_match[saiten_r4_1]": 2,
    "is_mikata": 6,
    "group": 0,
    "select_match[rangoku_r2_5]": 2,
    "select_match[rangoku_r3_5]": 2,
    "select_match[rangoku_r4_5]": 2,
    "select_match[rangoku_r4_6]": 2,
    "select_match[rangoku_r4_7]": 2,
    "select_match[saiten_r4_2]": 2,
    "select_match[saiten_r4_3]": 2,
    "select_match[saiten_r1_2]": 2,
    "select_match[saiten_r1_3]": 2,
    "select_match[saiten_r1_4]": 2,
    "start_motion": -1,
    "start_bhv_set_id": 1,
    "start_bhv_group_id": 2,
    "start_bhv_action_id": 1,
    "select_match[rangoku_r4_8]": 2,
    "select_match[rangoku_r4_9]": 2,
    "select_match[rangoku_r4_10]": 2,
    "vs_bhv_set_id": 1,
    "vs_bhv_group_id": 2,
    "vs_bhv_action_id": 1,
    "select_match2[ippan_r1_1]": -1,
    "select_match2": 14,
    "select_match2[ippan_r2_1]": 2,
    "select_match2[ippan_r2_3]": 2,
    "select_match2[ippan_r3_1]": 2,
    "select_match2[ippan_r3_3]": 2,
    "select_match2[ippan_r4_1]": 2,
    "select_match2[ippan_r4_3]": 2,
    "select_match2[saiten_r4_2]": 2,
    "select_match2[saiten_r4_3]": 2,
    "select_match3": 14,
    "select_match3[ippan_r2_1]": 2,
    "select_match3[ippan_r2_3]": 2,
    "select_match3[ippan_r3_1]": 2,
    "select_match3[ippan_r3_3]": 2,
    "select_match3[ippan_r4_1]": 2,
    "select_match3[ippan_r4_3]": 2,
    "select_match3[saiten_r4_2]": 2,
    "select_match3[saiten_r4_3]": 2,
    "select_match4": 14,
    "select_match4[saiten_r4_2]": 2,
    "select_match4[saiten_r4_3]": 2,
    "select_match5": 14,
    "select_match5[saiten_r4_3]": 2,
    "select_match6": 14,
    "select_match6[saiten_r4_3]": 2,
    "style": 13,
    "start_gmt": 1,
    "select_match[arena_btl04_0100]": 2,
    "select_match[arena_btl07_0100]": 2,
    "select_match[arena_btl10_0100]": 2
  },
  "COLUMN_INDICES": [
    1,
    2,
    70,
    4,
    5,
    11,
    12,
    71,
    83,
    84,
    85,
    89,
    90,
    91,
    13,
    17,
    14,
    18,
    19,
    20,
    22,
    94,
    103,
    23,
    24,
    95,
    104,
    26,
    96,
    105,
    27,
    28,
    97,
    106,
    30,
    98,
    107,
    31,
    32,
    99,
    108,
    34,
    35,
    36,
    38,
    39,
    40,
    42,
    43,
    44,
    46,
    47,
    48,
    54,
    55,
    56,
    57,
    72,
    58,
    59,
    60,
    61,
    73,
    62,
    63,
    64,
    65,
    74,
    75,
    76,
    86,
    87,
    88,
    66,
    67,
    68,
    69,
    77,
    100,
    109,
    112,
    78,
    101,
    110,
    113,
    115,
    117,
    79,
    80,
    81,
    120,
    121,
    122,
    93,
    102,
    111,
    114,
    116,
    118,
    119,
    92,
    82,
    53,
    52,
    51,
    50,
    49,
    45,
    41,
    37,
    33,
    29,
    25,
    21,
    16,
    15,
    10,
    9,
    8,
    7,
    6,
    3,
    0
  ]
}
'''
