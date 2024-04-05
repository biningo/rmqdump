import os
from typing import TextIO

import utils

EMPTY_ITEM = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

ITEM_BYTE_SIZE = 20
ITEM_COUNT = 30 * 10000


def parse_consume_queue(fp: TextIO):
    for idx in range(ITEM_COUNT):
        item = fp.read(ITEM_BYTE_SIZE)
        if not item or item == EMPTY_ITEM:
            return
        offset = utils.byte_to_int(item[0:8])
        size = utils.byte_to_int(item[8:12])
        tag_hash_code = utils.byte_to_int(item[12:20])
        print(offset, size, tag_hash_code)


def parse_topic_path(store_path, topic):
    return os.path.join(store_path, 'consumequeue', topic)


def parse_queue_ids(store_path, topic):
    queue_ids = []
    topic_path = parse_topic_path(store_path, topic)
    for queue_id in os.listdir(topic_path):
        queue_ids.append(queue_id)
    queue_ids.sort()
    return queue_ids


def read_consume_queue(store_path, topic):
    topic_path = parse_topic_path(store_path, topic)
    queue_ids = parse_queue_ids(store_path, topic)
    for queue_id in queue_ids:
        queue_path = os.path.join(topic_path, queue_id)
        print(queue_path)
        for name in os.listdir(queue_path):
            filepath = os.path.join(queue_path, name)
            utils.open_file_then(filepath, 'rb', parse_consume_queue)


if __name__ == '__main__':
    read_consume_queue('files', 'pb')
