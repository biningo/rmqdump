import os.path
import sys
from typing import BinaryIO

import utils

HEAD_BYTE_SIZE = 40
INDEX_ITEM_SIZE = 20
SLOT_BYTE_SIZE = 4
SLOT_COUNT = 500 * 10000

sys.setrecursionlimit(10000)


def parse_index_file(fp: BinaryIO):
    header = fp.read(HEAD_BYTE_SIZE)
    first_msg_time = utils.byte_to_int(header[0:8])
    last_msg_time = utils.byte_to_int(header[8:16])
    first_msg_offset = utils.byte_to_int(header[16:24])
    last_msg_offset = utils.byte_to_int(header[24:32])
    hash_slot_count = utils.byte_to_int(header[32:36])
    index_count = utils.byte_to_int(header[36:40])

    print(first_msg_time)
    print(last_msg_time)
    print(first_msg_offset)
    print(last_msg_offset)
    print(hash_slot_count)
    print(index_count)

    print("------------------")
    slots = []
    for slot_index in range(SLOT_COUNT):
        fp.seek(HEAD_BYTE_SIZE + slot_index * SLOT_BYTE_SIZE)
        index_pos = utils.byte_to_int(fp.read(SLOT_BYTE_SIZE))
        if index_pos > 0:
            slots.append((slot_index, index_pos))

    for slot in slots:
        print(slot[0], slot[1])
        index_pos = slot[1]
        parse_index_item(fp, index_pos)


def parse_index_item(fp: BinaryIO, index_pos):
    # 第0号位置全0 这里不用-1
    fp.seek(HEAD_BYTE_SIZE + SLOT_BYTE_SIZE * SLOT_COUNT + index_pos * INDEX_ITEM_SIZE)
    index_item = fp.read(INDEX_ITEM_SIZE)

    hashcode = utils.byte_to_int(index_item[0:4])
    offset = utils.byte_to_int(index_item[4:12])
    time_diff = utils.byte_to_int(index_item[12:16])
    next_index_pos = utils.byte_to_int(index_item[16:20])
    print(hashcode, offset, time_diff, next_index_pos)

    if next_index_pos > 0:
        parse_index_item(fp, next_index_pos)


def read_index_file(store_path):
    index_dir = os.path.join(store_path, 'index')
    for filename in os.listdir(index_dir):
        index_filepath = os.path.join(index_dir, filename)
        print(index_filepath)
        utils.open_file_then(index_filepath, 'rb', parse_index_file)


if __name__ == '__main__':
    read_index_file('files')
