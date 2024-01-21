from util import tree, get_entries, import_json, get_file_information
import json


def create_name_dict(mdict, rev=False):
    new_dict = {}
    for asset in mdict["Assets"]:
        asset_id = asset["ID"]
        if "Data" in asset:
            new_dict[asset_id] = asset["Data"][0]["Name"]
        else:
            new_dict[asset_id] = asset_id
    if rev: new_dict = {v: k for k, v in new_dict.items()}
    return new_dict
