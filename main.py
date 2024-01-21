import argparse
from pathlib import Path
from util import import_json, export_json, get_entries
import DBParser.PUIDFile.battle_command_set_puid as battle_command_puid
import DBParser.MiscFile.asset_id as asset_id_parse
import DBParser.DBFile.character_npc_soldier_name_group as name_group_parse
import DBParser.DBFile.battle_tougijyo_fighter_info as tougi_fighter_info
import DBParser.DBFile.battle_skill as battle_skill
from deepmerge import always_merger
import importlib
import MBVReader, MBVEdit
import subprocess
from lists_and_dicts import *
import shutil, re


def dynamic_import(mdict: dict, method_name: str):
    for module_name in mdict["Work"]:
        module_instance = None
        submodule_paths = ["DBParser.DBFile", "DBParser.MiscFile", "DBParser.PUIDFile"]

        for submodule_path in submodule_paths:
            full_module_path = submodule_path + "." + module_name
            try:
                module_instance = importlib.import_module(full_module_path)
                break
            except ImportError:
                print(f"Failed to import {module_name} module from {submodule_path}.")

        if not module_instance:
            continue

        method_instance = getattr(module_instance, method_name, None)

        if method_instance:
            method_instance(mdict)


def update_mot_puid(mot_type: str, file_jsons: dict, mot_path: Path):
    mjson = file_jsons["Sub"][f"motion_{mot_type}"]
    mot_json = get_entries(mjson, True)
    mot_json = {key.lower(): value for key, value in mot_json.items()}
    mot_files = [x.stem for x in mot_path.glob(f'**/*.{mot_type}') if x.is_file()]
    cur_key = int(list(mjson.keys())[-1]) + 1
    for mot in mot_files:
        if mot.lower() in mot_json:
            mot_name = f"{list(mjson[str(mot_json[mot.lower()])].keys())[0]}"
            if mjson[str(mot_json[mot.lower()])][mot_name]["reARMP_isValid"] == "0":
                mjson[str(mot_json[mot.lower()])][mot_name]["reARMP_isValid"] = "1"
            continue
        mjson[str(cur_key)] = {mot: {"reARMP_isValid": "1"}}
        cur_key += 1
    mjson["ROW_COUNT"] = cur_key
    file_jsons["Sub"][f"motion_{mot_type}"] = mjson


def update_bhv_puid(file_jsons: dict, bhv_path: Path):
    mjson = file_jsons["Sub"][f"behavior_set"]
    bhv_json = get_entries(mjson, True)
    bhv_json = {key.lower(): value for key, value in bhv_json.items()}
    bhv_files = [x for x in bhv_path.glob(f'**/*.mbv') if x.is_file()]
    cur_key = int(list(mjson.keys())[-1]) + 1
    for mot_path in bhv_files:
        mot = mot_path.stem
        if mot.lower() in bhv_json:
            bhv_name = f"{list(mjson[str(bhv_json[mot.lower()])].keys())[0]}"
            mot_path.rename(mot_path.with_name(f"{bhv_name}.mbv"))
            if mjson[str(bhv_json[mot.lower()])][bhv_name]["reARMP_isValid"] == "0":
                mjson[str(bhv_json[mot.lower()])][bhv_name]["reARMP_isValid"] = "1"
            continue
        mjson[str(cur_key)] = {mot: {"reARMP_isValid": "1"}}
        cur_key += 1
    mjson["ROW_COUNT"] = cur_key
    file_jsons["Sub"][f"behavior_set"] = mjson


def extract_mbv_info(file_jsons, mbv_path):
    mbv_files = [x for x in mbv_path.glob(f'**/*.mbv') if x.is_file()]
    mjson = file_jsons["Sub"][f"motion_gmt"]
    mot_json = get_entries(mjson)
    for mbv in mbv_files:
        if (mbv.parents[0] / f"{mbv.stem}.json").exists():
            print(f"{mbv.stem}.json already exists in MBV. Would you like to replace it?")
            if not yes_or_no(): continue
        MBVReader.create_mbv_json(mbv, mot_json)


def write_mbv(file_jsons: dict, mbv_path: Path, n_path: Path, m_path: Path):
    n_path.mkdir(parents=True, exist_ok=True)
    mbv_files = [x for x in mbv_path.glob(f'**/*.mbv') if x.is_file()]
    mjson = file_jsons["Sub"][f"motion_gmt"]
    mot_json = get_entries(mjson, True)
    anim_paths = [x for x in m_path.glob(f'**/*.gmt')]
    for mbv in mbv_files:
        MBVEdit.create_mbv(mbv, mot_json, n_path, anim_paths)


def yes_or_no():
    print("Type y and press enter if yes, otherwise just press enter.")
    minput = input("")
    if minput.lower() == "y":
        return True
    else:
        return False


def prep_workspace():
    mpath = Path(args.path)
    wpath = mpath / "Workspace"
    ppath = mpath / "Patches"
    motpath = mpath / "Motion"
    mbvpath = mpath / "MBV"
    motpath.mkdir(exist_ok=True)
    mbvpath.mkdir(exist_ok=True)
    file_jsons = {"Work": {}, "Sub": {}, "Final": {}}

    for name in file_names:
        if not (mpath / f"{name}.json").exists(): continue
        file_jsons["Sub"][name] = {}
        file_jsons["Sub"][name] = import_json(mpath, name)
    for name in wfile_names:
        if not (mpath / f"{name}.json").exists(): continue
        file_jsons["Work"][name] = {}
        file_jsons["Work"][name] = import_json(mpath, name)

    if "asset_id" in file_jsons["Sub"]:
        file_jsons["Sub"]["asset_id"] = asset_id_parse.create_name_dict(file_jsons["Sub"]["asset_id"])
    if "character_npc_soldier_name_group" in file_jsons["Sub"]:
        file_jsons["Sub"]["character_npc_soldier_name_group"] = name_group_parse.create_name_dict(file_jsons["Sub"]["character_npc_soldier_name_group"])
    for sub_key in ["motion_gmt", "motion_bep"]:
        if sub_key in file_jsons["Sub"]:
            update_mot_puid(sub_key.split('_')[1], file_jsons, motpath)
            if sub_key == "motion_gmt": extract_mbv_info(file_jsons, mbvpath)

    dynamic_import(file_jsons, "prep_workspace")

    wpath.mkdir(exist_ok=True)
    ppath.mkdir(exist_ok=True)
    for name in file_jsons["Final"]:
        if (wpath / f"{name}.json").exists():
            print(f"{name}.json already exists in Workspace. Would you like to replace it?")
            if not yes_or_no(): continue
        export_json(wpath, name, file_jsons["Final"][name])


def build_workspace():
    mpath = Path(args.path)
    wpath = mpath / "Workspace"
    ppath = mpath / "Patches"
    motpath = mpath / "Motion"
    mbvpath = mpath / "MBV"
    new_folder = mpath / "Build"
    file_jsons = {"Work": {}, "Sub": {}, "Final": {}}
    shutil.rmtree(new_folder, ignore_errors=True)

    for name in file_names:
        if not (mpath / f"{name}.json").exists(): continue
        file_jsons["Sub"][name] = {}
        file_jsons["Sub"][name] = import_json(mpath, name)
    for name in wfile_names:
        if not (wpath / f"{name}.json").exists(): continue
        file_jsons["Work"][name] = {}
        file_jsons["Work"][name] = import_json(wpath, name)
    if "asset_id" in file_jsons["Sub"]:
        file_jsons["Sub"]["asset_id"] = asset_id_parse.create_name_dict(file_jsons["Sub"]["asset_id"], True)
    if "behavior_set" in file_jsons["Sub"]:
        update_bhv_puid(file_jsons, mbvpath)
        file_jsons["Final"]["behavior_set"] = file_jsons["Sub"]["behavior_set"]
    if "File Information" in file_jsons["Sub"]:
        cfc_lookup = {key.lower(): value for key, value in file_jsons["Sub"]["File Information"]["File Specific Info"]["Set Order"].items()}
    for sub_key in ["motion_gmt", "motion_bep"]:
        if sub_key in file_jsons["Sub"]:
            update_mot_puid(sub_key.split('_')[1], file_jsons, motpath)
            file_jsons["Final"][sub_key] = file_jsons["Sub"][sub_key]
            if sub_key == "motion_gmt": write_mbv(file_jsons, mbvpath, new_folder / "motion" / "behavior", motpath)

    patchFiles = [Path(x) for x in ppath.glob('**/*.json') if x.is_file()]

    export_file_info = False
    for patch in patchFiles:
        cur_json = import_json(patch.parent, patch.stem)
        pn = patch.stem
        for name in file_jsons["Work"]:
            if name in pn: always_merger.merge(file_jsons["Work"][name], cur_json)
        if "cfc" in pn and "File Information" in file_jsons["Sub"]:
            export_file_info = True
            last_set_id = max(file_jsons["Sub"]["File Information"]["File Specific Info"]["Set Order"].values())
            cset_name = re.findall(r'\((.*?)\)', pn)[0]
            if cset_name.lower() in cfc_lookup:
                continue
            cfc_lookup[cset_name] = last_set_id + 1
            file_jsons["Sub"]["File Information"]["File Specific Info"]["Set Order"][cset_name] = last_set_id + 1
    dynamic_import(file_jsons, "prep_build")

    if "File Information" in file_jsons["Sub"]:
        file_jsons["Final"]["battle_command_set_puid"] = battle_command_puid.prep_build(file_jsons["Sub"]["File Information"])
        if export_file_info:
            file_jsons["Final"]["File Information"] = file_jsons["Sub"]["File Information"]
            file_jsons["Final"]["File Information"]["File Specific Info"]["Set Order"].pop("")

    new_folder.mkdir(exist_ok=True)
    for name in file_jsons["Final"]:
        if name == "File Information" and args.cfc: continue
        db_path = new_folder / db_paths[name]
        db_path.mkdir(exist_ok=True)
        export_json(db_path, name, file_jsons["Final"][name])
        if args.rearmp:
            if name == "File Information": continue
            bin_name = f"{name.replace('_puid', '')}.bin"
            bin_path = Path(db_path / bin_name)
            if bin_path.exists(): bin_path.unlink()
            subprocess.run([args.rearmp, str(db_path / f"{name}.json")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=db_path)
            Path(db_path / f"{name}.json").unlink()
            new_path = Path(db_path / f"{name}.json.bin")
            new_path.rename(new_path.with_name(bin_name))
    if args.copy_motion:
        gmt_paths = [x for x in motpath.glob(f'**/*.gmt')]
        bep_paths = [x for x in motpath.glob(f'**/*.bep')]
        if len(gmt_paths) > 0:
            print("Copying gmt files to Build/motion/gmt")
            gmt_folder = new_folder / "motion" / "gmt"
            gmt_folder.mkdir(parents=True, exist_ok=True)
            for m_gmt in gmt_paths:
                shutil.copy2(m_gmt, gmt_folder)
        if len(bep_paths) > 0:
            print("Copying bep files to Build/motion/bep")
            bep_folder = new_folder / "motion" / "bep"
            bep_folder.mkdir(parents=True, exist_ok=True)
            for m_bep in bep_paths:
                shutil.copy2(m_bep, bep_folder)
    if args.cfc and export_file_info:
        if "talk_param" not in file_jsons["Sub"] and "motion_gmt" not in file_jsons["Sub"]:
            raise Exception("talk_param and motion_gmt are required for automatic cfc rebuilding.")
        print("Building CFC")
        base_cfc_path = mpath / "Fighter Command"
        cfc_path = mpath / "CFC TEMP REBUILDING FOLDER (DON'T USE)"
        shutil.rmtree(cfc_path, ignore_errors=True)
        shutil.copytree(base_cfc_path, cfc_path)
        file_jsons["Final"]["File Information"]["Files Directory"] = "Extracted"
        file_jsons["Final"]["File Information"]["Motion GMT File"] = "motion_gmt.json"
        file_jsons["Final"]["File Information"]["Talk Param File"] = "talk_param.json"
        export_json(cfc_path, "motion_gmt", file_jsons["Final"]["motion_gmt"], True)
        export_json(cfc_path, "talk_param", file_jsons["Sub"]["talk_param"], True)
        export_json(cfc_path, "File Information", file_jsons["Final"]["File Information"], True)

        cfcFiles = [Path(x) for x in ppath.glob('**/cfc*(*)*.json') if x.is_file()]

        for mjson in cfcFiles:
            pn = mjson.stem
            cset_name = re.findall(r'\((.*?)\)', pn)[0]
            cur_json = import_json(mjson.parent, mjson.stem)
            export_json(cfc_path / "Extracted", cset_name, cur_json, True)
        result = subprocess.run([args.cfc, str(cfc_path)], input="\n", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=mpath)
        print(result.stdout)
        shutil.rmtree(cfc_path, ignore_errors=True)
        cfc_file = mpath / "fighter_command_new.cfc"
        new_file_path = new_folder / "battle" / cfc_file.name.replace("_new", "")
        new_file_path.parents[0].mkdir(exist_ok=True)
        cfc_file.rename(new_file_path)


def add_col():
    mpath = Path(args.path)
    cur_json = import_json(mpath.parent, mpath.stem)
    if mpath.stem == "battle_tougijyo_fighter_info":
        cur_json = tougi_fighter_info.add_column(cur_json, args.add_col)
    elif mpath.stem == "battle_skill":
        cur_json = battle_skill.add_column(cur_json, args.add_col)
    export_json(mpath.parent, mpath.stem + "_new", cur_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="Folder containing the required jsons")
    parser.add_argument("-build", action="store_true", help="Build for game use")
    parser.add_argument("-add_col", action="store", help="DEBUG: Add a column with name to path")
    parser.add_argument("-copy_motion", action="store_true", help="Copies the motion files when building")
    parser.add_argument("-rearmp", action="store", help="Path to reARMP.exe. Runs reARMP on resulting files.")
    parser.add_argument("-cfc", action="store", help="Path to fighter_commander.exe. Builds new cfc from patches.")
    args = parser.parse_args()

    if args.build:
        build_workspace()
    elif args.add_col:
        add_col()
    else:
        prep_workspace()
