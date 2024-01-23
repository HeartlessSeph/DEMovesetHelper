def create_entries(file_jsons):
    mdict = file_jsons["Sub"]["asset_id"]
    new_dict = {}
    for asset in mdict["Assets"]:
        asset_id = asset["ID"]
        if "Data" in asset:
            new_dict[asset_id] = asset["Data"][0]["Name"]
        else:
            new_dict[asset_id] = asset_id
    file_jsons["Sub"]["asset_id"] = new_dict


def create_entries_rev(file_jsons):
    create_entries(file_jsons)
    file_jsons["Sub"]["asset_id"] =\
        {v: k for k, v in file_jsons["Sub"]["asset_id"].items()}
