#!python3

# -*- coding: utf-8 -*-
import os
import json
import argparse
from collections import defaultdict
from collections import OrderedDict
import struct
from binary_reader import BinaryReader
from pathlib import Path
from util import tree, import_json, export_json, get_entries


def TStruct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary):
    Magic = writer.read_str(4)
    if Magic == "": return
    # print("Current Magic: " + Magic + "(" + str(hex(writer.pos() - 4)) + ")")
    HeaderSize = writer.read_uint32()  # Always 0x10

    if HeaderSize != 16:
        raise Exception("Improper Header Size")

    ContainerSize = writer.read_uint32()
    ContentSize = writer.read_uint32()

    if ContentSize != 0:
        struct_dict = {}
        if Magic == "PBBN":
            NameCount = writer.read_uint32()
            if NameCount != 0:
                for i in range(NameCount): writer.read_str(32)
            else:
                writer.read_str(32)  # One entry still exists if the count is 0
        elif Magic == "PBPJ":
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
            Prev_Frame_Number = writer.read_float() / 2  # Number of Frames * 2
            Unk2 = writer.read_uint32()
        elif Magic == "BSBM":
            Unk1 = writer.read_uint32()
            Unk2 = writer.read_uint32()
            Unk3 = writer.read_uint32()
            Unk4 = writer.read_uint32()
        elif Magic == "BTLT":
            Unk1 = writer.read_uint32()  # 0
            PBMPIdentifier = writer.read_uint32()
            if PBMPIdentifier > 0:
                mbv_dictionary[PBMPIdentifier]["Frames"] = int(Prev_Frame_Number)
            if Prev_Frame_Offset in frame_dictionary and PBMPIdentifier > 0:
                frame_dictionary[Prev_Frame_Offset].append(str(PBMPIdentifier))
            elif PBMPIdentifier > 0:
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
                mbv_dictionary[PBMPIdentifier][PBMPIdentifier] = NameDict[AnimationName]
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
        ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary)


def ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary):
    TStruct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary)


def PBRB_Struct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary):
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
        ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary)


def create_mbv_json(mbv_path, NameDict):
    mbv_dictionary = tree()
    pbml_dictionary = tree()
    frame_dictionary = tree()

    with mbv_path.open(mode='rb') as input_file:
        writer = BinaryReader(input_file.read())

    writer.seek(0)
    Prev_Frame_Number = 0
    Prev_Frame_Offset = 0
    PBRB_Struct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary)

    iterator = 0
    for offset in list(frame_dictionary.keys()):
        cur_list = frame_dictionary[offset]
        if len(cur_list) > 1:
            iterator += 1
            group_name = "Anim Group " + str(iterator) + " (Offset: " + str(hex(offset)) + ")"
            mbv_dictionary[group_name]["Frames"] = mbv_dictionary[int(cur_list[0])]["Frames"]
            for identifier in cur_list:
                iden = int(identifier)
                mbv_dictionary[group_name][iden] = mbv_dictionary[iden][iden]

    for offset in list(frame_dictionary.keys()):
        cur_list = frame_dictionary[offset]
        if len(cur_list) > 1:
            for identifier in cur_list:
                iden = int(identifier)
                if iden in mbv_dictionary: mbv_dictionary.pop(iden)

    export_json(Path(mbv_path.parents[0]), mbv_path.stem, mbv_dictionary)
