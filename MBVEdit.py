from collections import OrderedDict
from binary_reader import BinaryReader, Endian, Whence
from pathlib import Path
from util import tree, import_json


def TStruct(writer, Prev_Frame_Offset, Prev_Frame_Number, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool):
    Magic = writer.read_str(4)
    if Magic == "": return
    HeaderSize = writer.read_uint32()  # Always 0x10

    if HeaderSize != 16:
        raise Exception("Improper Header Size")

    ContainerSize = writer.read_uint32()
    ContentSize = writer.read_uint32()

    if ContentSize != 0:
        if Magic == "PBPJ":
            if not name_bool:
                writer.write_str_fixed(file_name, ContentSize)
                name_bool = True
            else:
                writer.seek(ContentSize, whence=Whence.CUR)
        elif Magic == "BSTL":
            Prev_Frame_Offset = writer.pos()
            Prev_Frame_Number = writer.read_float()  # Number of Frames * 2
            writer.seek(0x4, whence=Whence.CUR)
        elif Magic == "BTLT":
            writer.seek(0x4, whence=Whence.CUR)
            PBMPIdentifier = writer.read_uint32()
            mbv_dictionary[PBMPIdentifier].setdefault("Frame Offset", []).append(Prev_Frame_Offset)
            writer.seek(0xC, whence=Whence.CUR)
        elif Magic == "PBMP":
            PBMPIdentifier = writer.read_uint32()
            writer.seek(0x8, whence=Whence.CUR)
            AnimationName = writer.read_uint32()
            if PBMPIdentifier > 0:
                mbv_dictionary[PBMPIdentifier]["Animation Offset"] = writer.pos() - 4
        elif Magic == "BTTC":
            writer.seek(0x8, whence=Whence.CUR)
            Unk3 = writer.read_float()
            writer.seek(-4, whence=Whence.CUR)
            new_val = max(10000, int(Unk3))
            writer.write_float(new_val)
            writer.seek(0x18, whence=Whence.CUR)
        else:
            for i in range(ContentSize): writer.read_uint8()

    pos = writer.pos()

    while (writer.pos() - pos) < (ContainerSize - ContentSize):
        ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool)


def ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool):
    TStruct(writer, Prev_Frame_Offset, Prev_Frame_Number, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool)


def PBRB_Struct(writer, Prev_Frame_Offset, Prev_Frame_Number, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool):
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
        ReadEntry(writer, Prev_Frame_Offset, Prev_Frame_Number, NameDict, mbv_dictionary, pbmp_list, file_name, name_bool)


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
    name_bool = False

    stances_dictionary = tree()
    mbv_dictionary = tree()
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
    Prev_Frame_Number = 0
    Prev_Frame_Offset = 0
    PBRB_Struct(writer, Prev_Frame_Offset, Prev_Frame_Number, NameDict, mbv_dictionary, pbmp_list, mbv_path.stem, name_bool)

    for pbmp_id, (anim_used, frames, anim_name) in stances_dictionary.items():
        if pbmp_id not in mbv_dictionary or "Animation Offset" not in mbv_dictionary[pbmp_id]:
            continue

        animation_offset = mbv_dictionary[pbmp_id]["Animation Offset"]

        if "Frame Offset" in mbv_dictionary[pbmp_id] and frames > 0:
            for frame_offset in mbv_dictionary[pbmp_id]["Frame Offset"]:
                if anim_paths:
                    anim_match = next((file_path for file_path in anim_paths if file_path.stem.lower() == anim_name.lower()), None)
                    if anim_match:
                        frames = get_gmt_size(anim_match)
                writer.seek(frame_offset)
                writer.write_float(frames)

        writer.seek(animation_offset)
        writer.write_uint32(anim_used)

    new_mbv_path.mkdir(exist_ok=True)
    new_file_path = new_mbv_path / f"{mbv_path.stem}.mbv"

    with open(new_file_path, 'wb') as new_file:
        new_file.write(writer.buffer())
