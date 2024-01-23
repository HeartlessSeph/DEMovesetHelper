from binary_reader import BinaryReader, Whence
from pathlib import Path
from util import tree, export_json


def TStruct(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary):
    Magic = writer.read_str(4)
    if Magic == "": return
    HeaderSize = writer.read_uint32()  # Always 0x10

    if HeaderSize != 16:
        raise Exception("Improper Header Size")

    ContainerSize = writer.read_uint32()
    ContentSize = writer.read_uint32()

    if ContentSize != 0:
        if Magic == "BSTL":
            Prev_Frame_Offset = writer.pos()
            Prev_Frame_Number = writer.read_float() / 2  # Number of Frames * 2
            writer.seek(0x4, whence=Whence.CUR)
        elif Magic == "BTLT":
            writer.seek(0x4, whence=Whence.CUR)
            PBMPIdentifier = writer.read_uint32()
            if PBMPIdentifier > 0:
                mbv_dictionary[PBMPIdentifier]["Frames"] = int(Prev_Frame_Number)
            if Prev_Frame_Offset in frame_dictionary and PBMPIdentifier > 0:
                frame_dictionary[Prev_Frame_Offset].append(str(PBMPIdentifier))
            elif PBMPIdentifier > 0:
                frame_dictionary[Prev_Frame_Offset] = [str(PBMPIdentifier)]
            writer.seek(0xC, whence=Whence.CUR)
        elif Magic == "PBMP":
            PBMPIdentifier = writer.read_uint32()
            writer.seek(0x8, whence=Whence.CUR)
            AnimationName = writer.read_uint32()
            if PBMPIdentifier > 0:
                mbv_dictionary[PBMPIdentifier][PBMPIdentifier] = NameDict[AnimationName]
        else:
            for i in range(ContentSize): writer.read_uint8()

    pos = writer.pos()

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

    writer.seek(0x6, whence=Whence.CUR)
    FileSize = writer.read_uint32()

    while writer.pos() + 16 <= FileSize:
        ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, frame_dictionary, NameDict, mbv_dictionary)


def create_mbv_json(mbv_path, NameDict):
    mbv_dictionary = tree()
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
            group_name = f"Anim Group {iterator} (Offset: {hex(offset)})"
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
