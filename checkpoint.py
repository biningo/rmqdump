import os
import time
from typing import BinaryIO

import utils

TIMESTAMP_BYTE_SIZE = 8


def parse_checkpoint_file(fp: BinaryIO):
    physic_msg_ts = int.from_bytes(fp.read(TIMESTAMP_BYTE_SIZE), 'big')
    logics_msg_ts = int.from_bytes(fp.read(TIMESTAMP_BYTE_SIZE), 'big')
    index_msg_ts = int.from_bytes(fp.read(TIMESTAMP_BYTE_SIZE), 'big')
    print(physic_msg_ts, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(physic_msg_ts / 1000)))
    print(logics_msg_ts, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(logics_msg_ts / 1000)))
    print(index_msg_ts, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(index_msg_ts / 1000)))


def read_checkpoint(store_path):
    checkpoint_filepath = os.path.join(store_path, 'checkpoint')
    utils.open_file_then(checkpoint_filepath, 'rb', parse_checkpoint_file)


if __name__ == '__main__':
    read_checkpoint('files')
