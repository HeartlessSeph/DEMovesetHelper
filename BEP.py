from binary_reader import BinaryReader, Endian, Whence
import argparse
from pathlib import Path
import random


def bep_read_pib(buffer, m_dict):
    loop_end = False
    buffer.read_bytes(0x10)
    while loop_end is False:
        save_file = read_pib_prop(buffer, m_dict)
        loop_end = end_check(buffer)
    return save_file


def read_pib_prop(buffer, m_dict):
    save_file = False
    prop_start = buffer.pos()
    guid = buffer.read_bytes(0x20)  # Skip GUID
    bone = buffer.read_bytes(0x20)
    prop_sect = buffer.read_uint16()
    prop_type = buffer.read_uint16()
    prop_size = buffer.read_uint32()
    buffer.read_uint64()  # Skip non-important data
    prop_end = buffer.pos() + prop_size

    if prop_sect == 12 and prop_type == 18 and prop_size == 288:
        buffer.seek(prop_start + 0x13C)
        pib_name = buffer.read_str()
        buffer.seek(prop_start + 0x74)
        if pib_name in m_dict:
            save_file = True
            buffer.write_uint32(m_dict[pib_name])
    buffer.seek(prop_end)
    return save_file


def end_check(buffer):
    if buffer.pos() + 80 >= buffer.size():
        return True
    return False


def update_bep_particles(file_jsons, mpath):
    m_dict = file_jsons["puid"]["particle_p"]
    my_files = [x for x in mpath.glob(f'**/*.bep') if x.is_file()]
    print("Patching bep file Particle IDs")
    for my_file in my_files:
        with my_file.open('rb') as f:
            buffer = BinaryReader(f.read())
        save_file = bep_read_pib(buffer, m_dict)
        if save_file:
            with my_file.open('wb') as f:
                f.write(buffer.buffer())
