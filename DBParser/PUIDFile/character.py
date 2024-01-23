from util import tree, get_entries, import_json, get_file_information
import json


def prep_build(character_character_data):
    global base_json
    new_dict = tree()
    new_dict.update(json.loads(base_json))
    file_info = get_entries(character_character_data, True)
    last_entry = list(file_info.keys())[-1]
    ROW_COUNT = int(file_info[last_entry]) + 1
    new_dict["ROW_COUNT"] = ROW_COUNT
    file_info = dict(sorted(file_info.items(), key=lambda item: item[1]))
    file_info.pop("")
    for entry in file_info:
        cur_num = file_info[entry]
        new_dict[cur_num][entry]["reARMP_isValid"] = "1"
    return new_dict



base_json = '''
{
  "VERSION": 2,
  "REVISION": 0,
  "ROW_COUNT": 25100,
  "COLUMN_COUNT": 0,
  "TEXT_COUNT": 0,
  "ROW_VALIDATOR": 0,
  "COLUMN_VALIDATOR": -1,
  "HAS_ROW_NAMES": true,
  "HAS_COLUMN_NAMES": true,
  "HAS_ROW_VALIDITY": true,
  "HAS_COLUMN_VALIDITY": false,
  "HAS_UNKNOWN_BITMASK": false,
  "HAS_ROW_INDICES": false,
  "TABLE_ID": 0,
  "STORAGE_MODE": 0,
  "columnTypes": {}
}
'''
