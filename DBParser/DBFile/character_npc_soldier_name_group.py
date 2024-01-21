from util import tree, get_entries, import_json, get_file_information
import json


def create_name_dict(mdict):
    new_dict = tree()
    for entry in [e for e in mdict if e.isdigit()]:
        group_name = list(mdict[entry].keys())[0]
        if not "table" in mdict[entry][group_name]: continue
        for nid in reversed([e for e in mdict[entry][group_name]["table"] if e.isdigit()]):
            if "1" in mdict[entry][group_name]["table"][nid][""]:
                new_dict[int(entry)][int(nid)] = mdict[entry][group_name]["table"][nid][""]["1"]
            else:
                new_dict[int(entry)][int(nid)] = "Null"
    return new_dict
