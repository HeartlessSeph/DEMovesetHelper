import argparse
from pathlib import Path
from binary_reader import BinaryReader
from util import import_json, export_json, get_entries, yes_or_no
import DBParser.PUIDFile.battle_command_set_puid as battle_command_puid
from deepmerge import always_merger
import importlib
import MBVReader, MBVEdit
import subprocess
from lists_and_dicts import *
import shutil, re
from BEP import update_bep_particles


def dynamic_import(mdict: dict, method_name: str, sub_dict_name: str):
    for module_name in mdict[sub_dict_name]:
        module_instance = None
        submodule_paths = ["DBParser.DBFile", "DBParser.MiscFile", "DBParser.PUIDFile"]

        for submodule_path in submodule_paths:
            full_module_path = submodule_path + "." + module_name
            try:
                module_instance = importlib.import_module(full_module_path)
                break
            except ImportError:
                # print(f"Failed to import {sub_dict_name}:{module_name} module from {submodule_path}.")
                pass

        if not module_instance:
            continue

        method_instance = getattr(module_instance, method_name, None)

        if method_instance:
            method_instance(mdict)


def update_pib_ids(file_jsons, mpath):
    m_dict = file_jsons["puid"]["particle_p"]
    pib_lookup = {k.lower(): k for k, v in m_dict.items()}
    my_files = [x for x in mpath.glob(f'**/*.pib') if x.is_file()]
    print("Patching pib file Particle IDs")
    for my_file in my_files:
        f_name = my_file.stem.lower()
        if f_name in pib_lookup:
            cur_id = m_dict[pib_lookup[f_name]]
            with my_file.open('rb') as f:
                buffer = BinaryReader(f.read())
            buffer.seek(0x10)
            buffer.write_uint32(cur_id)
            with my_file.open('wb') as f:
                f.write(buffer.buffer())


def update_puid(file_type: str, puid_file: str, file_jsons: dict, puid_path: Path, search_criteria: str = "**/*."):
    mjson = file_jsons["Sub"][puid_file]
    lookup_json = get_entries(mjson, True)
    lookup_json = {key.lower(): value for key, value in lookup_json.items()}
    my_files = [x.stem for x in puid_path.glob(f'{search_criteria}{file_type}') if x.is_file()]
    cur_key = int(list(mjson.keys())[-1]) + 1
    file_jsons["puid"][f"{puid_file}_p"] = {}
    for my_file in my_files:
        if my_file.lower() in lookup_json:
            mot_name = f"{list(mjson[str(lookup_json[my_file.lower()])].keys())[0]}"
            file_jsons["puid"][f"{puid_file}_p"][mot_name] = lookup_json[my_file.lower()]
            if mjson[str(lookup_json[my_file.lower()])][mot_name]["reARMP_isValid"] == "0":
                mjson[str(lookup_json[my_file.lower()])][mot_name]["reARMP_isValid"] = "1"
            continue
        mjson[str(cur_key)] = {my_file: {"reARMP_isValid": "1"}}
        file_jsons["puid"][f"{puid_file}_p"][my_file] = cur_key
        cur_key += 1
    if len(file_jsons["puid"][f"{puid_file}_p"]) == 0:
        file_jsons["puid"].pop(f"{puid_file}_p")
    mjson["ROW_COUNT"] = cur_key
    file_jsons["Sub"][puid_file] = mjson


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
    print(f"Copying mbv files to Build\\motion\\behavior")
    for mbv in mbv_files:
        MBVEdit.create_mbv(mbv, mot_json, n_path, anim_paths)


def prep_workspace():
    mpath = Path(args.path)
    wpath = mpath / "Workspace"
    ppath = mpath / "Patches"
    wpath.mkdir(exist_ok=True)
    ppath.mkdir(exist_ok=True)
    path_types = ("Motion", "MBV", "Sound", "Particle", "UI")
    for path_name in path_types:
        globals()[f"{path_name}path"] = mpath / path_name
        globals()[f"{path_name}path"].mkdir(exist_ok=True)
    file_jsons = {"Work": {}, "Sub": {}, "puid": {}, "Final": {}}

    for sub_type, mfile_name in {"Sub": file_names, "Work": wfile_names}.items():
        for name in mfile_name:
            if not (mpath / f"{name}.json").exists(): continue
            file_jsons[sub_type][name] = import_json(mpath, name)

    dynamic_import(file_jsons, "create_entries", "Sub")
    for d in puid_auto_update:
        d_file, d_search, d_ext, d_puid, d_isUpdate = (d["file"], d["search"], d["ext"], d["puidpath"], d["update"])
        if d_file in file_jsons["Sub"]:
            if d_isUpdate: update_puid(d_ext, d_file, file_jsons, mpath / d_puid, d_search)
            if d_file == "motion_gmt": extract_mbv_info(file_jsons, MBVpath)

    dynamic_import(file_jsons, "prep_workspace", "Work")
    for name in file_jsons["Final"]:
        if (wpath / f"{name}.json").exists():
            print(f"{name}.json already exists in Workspace. Would you like to replace it?")
            if not yes_or_no(): continue
        export_json(wpath, name, file_jsons["Final"][name])


def build_workspace():
    mpath = Path(args.path)
    wpath = mpath / "Workspace"
    ppath = mpath / "Patches"
    path_types = ("Motion", "MBV", "Sound", "Particle", "UI")
    for path_name in path_types:
        globals()[f"{path_name}path"] = mpath / path_name
    new_folder = mpath / "Build"
    file_jsons = {"Work": {}, "Sub": {}, "puid": {}, "Final": {}}
    shutil.rmtree(new_folder, ignore_errors=True)

    for sub_type, (mfile_name, cur_path) in \
            {"Sub": (file_names, mpath), "Work": (wfile_names, wpath)}.items():
        for name in mfile_name:
            if not (cur_path / f"{name}.json").exists(): continue
            file_jsons[sub_type][name] = import_json(cur_path, name)

    dynamic_import(file_jsons, "create_entries_rev", "Sub")

    if "File Information" in file_jsons["Sub"]:
        cfc_lookup = {key.lower(): value for key, value in file_jsons["Sub"]["File Information"]["File Specific Info"]["Set Order"].items()}

    for d in puid_auto_update:
        d_file, d_search, d_ext, d_puid, d_out, d_isUpdate, d_isCopy, d_copySearch = (
            d["file"], d["search"], d["ext"], d["puidpath"], d["outpath"],
            d["update"], d["copy"], d["copy_search"]
        )
        if d_file in file_jsons["Sub"]:
            if d_isUpdate:
                update_puid(d_ext, d_file, file_jsons, mpath / d_puid, d_search)
            file_jsons["Final"][d_file] = file_jsons["Sub"][d_file]
            if args.copy_files and d_isCopy:
                paths = list((mpath / d_puid).glob(f'{d_copySearch}'))
                if paths:
                    print(f"Copying {d_ext} files to Build\\{str(d_out)}")
                    folder = new_folder / d_out
                    folder.mkdir(parents=True, exist_ok=True)
                    for file_path in paths:
                        if file_path.is_dir():
                            shutil.copytree(file_path, folder, dirs_exist_ok=True)
                        else:
                            shutil.copy2(file_path, folder)
            if d_file == "motion_gmt" and args.copy_files:
                write_mbv(file_jsons, MBVpath, new_folder / "motion" / "behavior", Motionpath)
        if args.particle and "particle_p" in file_jsons["puid"]:
            update_bep_particles(file_jsons, new_folder / "motion" / "bep")
            update_pib_ids(file_jsons, new_folder / "particle")

    patchFiles = [Path(x) for x in ppath.glob('**/*.json') if x.is_file()]

    export_file_info = False
    for patch in patchFiles:
        cur_json = import_json(patch.parent, patch.stem)
        pn = patch.stem
        for sub_type in file_jsons["Work"]:
            if sub_type in pn: always_merger.merge(file_jsons["Work"][sub_type], cur_json)
        if "cfc" in pn and "File Information" in file_jsons["Sub"]:
            export_file_info = True
            last_set_id = max(file_jsons["Sub"]["File Information"]["File Specific Info"]["Set Order"].values())
            cset_name = re.findall(r'\((.*?)\)', pn)[0]
            if cset_name.lower() in cfc_lookup:
                continue
            cfc_lookup[cset_name] = last_set_id + 1
            file_jsons["Sub"]["File Information"]["File Specific Info"]["Set Order"][cset_name] = last_set_id + 1
    dynamic_import(file_jsons, "prep_build", "Work")

    if "File Information" in file_jsons["Sub"]:
        file_jsons["Final"]["battle_command_set_puid"] = battle_command_puid.prep_build(file_jsons["Sub"]["File Information"])
        if export_file_info:
            file_jsons["Final"]["File Information"] = file_jsons["Sub"]["File Information"]
            file_jsons["Final"]["File Information"]["File Specific Info"]["Set Order"].pop("")

    new_folder.mkdir(exist_ok=True)
    for sub_type in file_jsons["Final"]:
        if sub_type == "File Information" and args.cfc: continue
        db_path = new_folder / db_paths[sub_type]
        db_path.mkdir(exist_ok=True)
        export_json(db_path, sub_type, file_jsons["Final"][sub_type])
        if args.rearmp:
            if sub_type == "File Information": continue
            bin_name = f"{sub_type.replace('_puid', '')}.bin"
            bin_path = Path(db_path / bin_name)
            if bin_path.exists(): bin_path.unlink()
            subprocess.run([args.rearmp, str(db_path / f"{sub_type}.json")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=db_path)
            Path(db_path / f"{sub_type}.json").unlink()
            new_path = Path(db_path / f"{sub_type}.json.bin")
            new_path.rename(new_path.with_name(bin_name))
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="Folder containing the required jsons")
    parser.add_argument("-build", action="store_true", help="Build for game use")
    parser.add_argument("-copy_files", action="store_true", help="Copies files updated through PUID when building.")
    parser.add_argument("-particle", action="store_true", help="Updates the PiB ID's in BEP files. Requires copy_files to work.")
    parser.add_argument("-rearmp", action="store", help="Path to reARMP.exe. Runs reARMP on resulting files.")
    parser.add_argument("-cfc", action="store", help="Path to fighter_commander.exe. Builds new cfc from patches.")
    args = parser.parse_args()

    if args.build:
        build_workspace()
    else:
        prep_workspace()
