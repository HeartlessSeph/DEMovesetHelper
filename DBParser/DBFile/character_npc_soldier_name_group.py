from util import tree


def create_entries(file_jsons):
    new_dict = tree()
    mdict = file_jsons["Sub"]["character_npc_soldier_name_group"]
    for entry in [e for e in mdict if e.isdigit()]:
        group_name = list(mdict[entry].keys())[0]
        if not "table" in mdict[entry][group_name]: continue
        for nidx, nid in enumerate([e for e in mdict[entry][group_name]["table"] if e.isdigit()]):
            if "1" in mdict[entry][group_name]["table"][nid][""]:
                new_dict[int(entry)][int(nid)] = mdict[entry][group_name]["table"][nid][""]["1"]
            else:
                new_dict[int(entry)][int(nid)] = f"[**{nidx}]"
    file_jsons["Sub"]["character_npc_soldier_name_group"] = new_dict


def create_entries_rev(file_jsons):
    new_dict = tree()
    mdict = file_jsons["Sub"]["character_npc_soldier_name_group"]
    for entry in [e for e in mdict if e.isdigit()]:
        group_name = list(mdict[entry].keys())[0]
        if not "table" in mdict[entry][group_name]: continue
        for nidx, nid in enumerate([e for e in mdict[entry][group_name]["table"] if e.isdigit()]):
            if "1" in mdict[entry][group_name]["table"][nid][""]:
                new_dict[int(entry)][mdict[entry][group_name]["table"][nid][""]["1"]] = int(nid)
            else:
                new_dict[int(entry)][f"[**{nidx}]"] = int(nid)
    file_jsons["puid"]["character_npc_soldier_name_group"] = new_dict
