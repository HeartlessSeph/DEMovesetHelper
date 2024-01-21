#!python3

# -*- coding: utf-8 -*-
import os
import json
import argparse
from collections import defaultdict
from collections import OrderedDict
import struct
from binary_reader import BinaryReader, Endian, Whence
from pathlib import Path
from util import tree, import_json, export_json


def TStruct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool):
    Magic = writer.read_str(4)
    if Magic == "": return
    HeaderSize = writer.read_uint32()  # Always 0x10

    if HeaderSize != 16:
        raise Exception("Improper Header Size")

    ContainerSize = writer.read_uint32()
    ContentSize = writer.read_uint32()

    if ContentSize != 0:
        struct_dict = {}
        if Magic == "PBBN":
            NameCount = writer.read_uint32()
            for i in range(max(NameCount, 1)): writer.read_str(32)
        elif Magic == "PBPJ":
            if not name_bool:
                writer.write_str_fixed(file_name, ContentSize)
                name_bool = True
            else:
                writer.read_str(ContentSize)
        elif Magic == "PFNL":
            NameCount1 = writer.read_uint32()
            StartOffset2 = writer.read_uint32()
            NameCount2 = writer.read_uint32()
            StartOffset2 = writer.read_uint32()
            for i in range(NameCount1): writer.read_str(16)
            for i in range(NameCount2): writer.read_str(16)
        elif Magic == "PSFN":
            NameCount = writer.read_uint32()
            StartOffset = writer.read_uint32()
            for i in range(NameCount): writer.read_str(16)
        elif Magic == "BSTN":
            NameCount = writer.read_uint32()
            StartOffset = writer.read_uint32()
            for i in range(NameCount): writer.read_str(16)
        elif Magic == "PBSB":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()  # Always 0
        elif Magic == "BSTL":
            Prev_Frame_Offset = writer.pos()
            Prev_Frame_Number = writer.read_float()  # Number of Frames * 2
            Unk2 = writer.read_uint32()
        elif Magic == "BSBM":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()
            Unk3 = writer.read_uint32()
            Unk4 = writer.read_uint32()
        elif Magic == "BTLT":
            Unk1 = writer.read_uint32()  # 0
            PBMPIdentifier = writer.read_uint32()
            mbv_dictionary[PBMPIdentifier]["Frame Offset"] = Prev_Frame_Offset
            if Prev_Frame_Offset in frame_dictionary and PBMPIdentifier in pbmp_list:
                frame_dictionary[Prev_Frame_Offset].append(str(PBMPIdentifier))
            elif PBMPIdentifier in pbmp_list:
                frame_dictionary[Prev_Frame_Offset] = [str(PBMPIdentifier)]
            Unk3 = writer.read_float()
            Unk4 = writer.read_uint32()  # 0
            Unk5 = writer.read_uint32()
        elif Magic == "BTBF":
            Unk1 = writer.read_uint32()
        elif Magic == "BSPS":
            Unk1 = writer.read_uint32()
        elif Magic == "PDMY":
            Dummy = writer.read_uint32()  # Always 0
        elif Magic == "BSBC":
            Unk1 = writer.read_int32()  # -1
            Unk2 = writer.read_uint32()
            Unk3 = writer.read_uint32()
            Unk4 = writer.read_uint32()
        elif Magic == "BSTT":
            Unk1 = writer.read_uint32()
        elif Magic == "SUID":
            Unk1 = writer.read_uint16()
            Unk2 = writer.read_uint16()  # 0
            Unk3 = writer.read_uint32()
            Unk4 = writer.read_uint16()
            Unk5 = writer.read_uint16()  # 0?
            Unk6 = writer.read_uint32()
        elif Magic == "BSTC":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()
        elif Magic == "BTSN":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()
            Unk3 = writer.read_uint32()
        elif Magic == "TCGL":
            Unk1 = writer.read_uint32()
        elif Magic == "TCGN":
            Unk1 = writer.read_uint32()
        elif Magic == "BTTL":
            Unk1 = writer.read_float()
            Unk2 = writer.read_uint32()
        elif Magic == "TBBN":
            Unk1 = writer.read_uint32()
        elif Magic == "BTBM":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()
        elif Magic == "BTVB":
            Unk1 = writer.read_uint32()
        elif Magic == "PBMP":
            PBMPIdentifier = writer.read_uint32()
            Unk2 = writer.read_float()
            Unk3 = writer.read_uint16()
            Unk4 = writer.read_uint16()  # 0?
            AnimationName = writer.read_uint32()
            if PBMPIdentifier > 0:
                mbv_dictionary[PBMPIdentifier]["Animation Offset"] = writer.pos() - 4
        elif Magic == "PBMI":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()
            Unk3 = writer.read_uint32()  # 0?
            Unk4 = writer.read_uint32()  # 0?
        elif Magic == "PBSI":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()
        elif Magic == "PBII":
            Unk1 = writer.read_uint8()
            Unk2 = writer.read_uint8()
            Unk3 = writer.read_uint16()
            Unk4 = writer.read_uint32()
        elif Magic == "PBUC":
            writer.read_str(16)
        elif Magic == "PBCK":
            Unk1 = writer.read_float()
            Unk2 = writer.read_float()
            Unk3 = writer.read_uint32()
        elif Magic == "PBMF":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_float()
            Unk3 = writer.read_float()
        elif Magic == "PBPB":
            Unk1 = writer.read_uint16()
            Unk2 = writer.read_uint16()
            Unk3 = writer.read_uint32()
            Unk4 = writer.read_uint16()
            Unk5 = writer.read_uint16()
            Unk6 = writer.read_uint32()
        elif Magic == "BTTT":
            Unk1 = writer.read_float()
            Unk2 = writer.read_float()
        elif Magic == "BTBR":
            Unk1 = writer.read_float()
            Unk2 = writer.read_float()
            Unk3 = writer.read_uint32()
        elif Magic == "BTTC":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_float()
            Unk3 = writer.read_float()
            writer.seek(-4, 1)
            new_val = max(10000, int(Unk3))
            writer.write_float(new_val)
            Unk4 = writer.read_uint32()  # 0
            Unk5 = writer.read_uint32()  # 0
            Unk6 = writer.read_uint32()  # 0
            Unk7 = writer.read_uint32()  # 0
            Unk8 = writer.read_uint32()  # 0
            Unk9 = writer.read_float()
        elif Magic == "BTCC":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint8()
            Unk3 = writer.read_uint8()
            Unk4 = writer.read_uint16()
        elif Magic == "BTTS":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_int32()  # 0xFF000000
        elif Magic == "TCCN":
            Unk1 = writer.read_uint32()
        else:
            for i in range(ContentSize): writer.read_uint8()

    pos = writer.pos()
    Prev_Magic = Magic

    while (writer.pos() - pos) < (ContainerSize - ContentSize):
        ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool)


def ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool):
    TStruct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool)


def PBRB_Struct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool):
    Magic = writer.read_str(4)  # PBRB
    if Magic != "PBRB":
        raise Exception("Not a proper mbv file?")

    Endianess0 = writer.read_uint8()
    Endianess1 = writer.read_uint8()
    endian_dict = {0: False, 1: True}
    writer.set_endian(endian_dict[Endianess1])

    Unused = writer.read_uint16()
    Version = writer.read_uint32()
    FileSize = writer.read_uint32()
    Prev_Magic = "TEMP"

    while writer.pos() + 16 <= FileSize:
        ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool)


def get_gmt_size(anim_path):
    with anim_path.open(mode='rb') as input_file:
        buffer = BinaryReader(input_file.read())
    buffer.seek(0x5)
    m_endian = buffer.read_uint8()
    if m_endian == 1: buffer.set_endian(Endian.BIG)
    buffer.seek(0x34)
    buffer.seek(buffer.read_uint32())
    buffer.read_uint32()
    anim_length = buffer.read_uint32()
    buffer.read_uint32()
    anim_framerate = int(buffer.read_float())
    output = anim_length * (30 / anim_framerate)
    return float(round(output, 0)) * 2


def create_mbv(mbv_path: Path, NameDict: dict, new_mbv_path: Path, anim_paths: list[Path]):
    filedict = OrderedDict()
    name_bool = False

    stances_dictionary = tree()
    mbv_dictionary = tree()
    pbml_dictionary = tree()
    frame_dictionary = tree()
    pbmp_list = []


    Anim_Stances = import_json(Path(mbv_path.parents[0]), mbv_path.stem)

    with mbv_path.open(mode='rb') as input_file:
        writer = BinaryReader(input_file.read())

    for entry in list(Anim_Stances.keys()):  # Goes through each Stance entry
        if "Frames" in Anim_Stances[entry]:
            frames = float(Anim_Stances[entry]["Frames"] * 2)
        else:
            frames = -1.0
        Anim_Stances[entry].pop("Frames", None)
        for movement_entry in list(Anim_Stances[entry].keys()):
            anim_identifier = int(movement_entry)
            if isinstance(Anim_Stances.get(entry, {}).get(movement_entry), dict): continue
            pbmp_list.append(anim_identifier)
            animation_name = Anim_Stances[entry][movement_entry]
            animation_used = NameDict[animation_name]
            stances_dictionary[anim_identifier] = [animation_used, frames, animation_name]

    writer.seek(0)
    FileSize = 0
    Prev_Frame_Number = 0
    Prev_Frame_Offset = 0
    Prev_Magic = "TEMP"
    PBRB_Struct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary, pbmp_list, mbv_path.stem, name_bool)

    for offset in list(frame_dictionary.keys()):
        cur_list = frame_dictionary[offset]

    for pbmp_id in list(stances_dictionary.keys()):  # Writes the new stances to file
        anim_used = stances_dictionary[pbmp_id][0]
        frames = stances_dictionary[pbmp_id][1]
        anim_name = stances_dictionary[pbmp_id][2]
        if not pbmp_id in mbv_dictionary:
            continue
        animation_offset = mbv_dictionary[pbmp_id]["Animation Offset"]

        if "Frame Offset" in mbv_dictionary[pbmp_id] and frames > 0:
            if len(anim_paths) > 0:
                anim_match = [file_path for file_path in anim_paths if file_path.stem.lower() == anim_name.lower()]
                if len(anim_match) > 0:
                    anim_match = anim_match[0]
                    frames = get_gmt_size(anim_match)
            frame_offset = mbv_dictionary[pbmp_id]["Frame Offset"]
            writer.seek(frame_offset)
            writer.write_float(frames)
        writer.seek(animation_offset)
        writer.write_uint32(anim_used)

    new_mbv_path.mkdir(exist_ok=True)
    new_file_path = new_mbv_path / f"{mbv_path.stem}.mbv"

    with open(new_file_path, 'wb') as new_file:
        new_file.write(writer.buffer())
