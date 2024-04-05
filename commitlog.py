from typing import BinaryIO

import utils


class CommitLog:
    def __init__(self, fp: BinaryIO):
        self.msg_size = utils.byte_to_int(fp.read(4))
        self.magic_code = fp.read(4)
        self.body_crc = fp.read(4)
        self.queue_id = utils.byte_to_int(fp.read(4))
        self.msg_flag = fp.read(4)
        self.queue_offset = utils.byte_to_int(fp.read(8))
        self.physical_offset = utils.byte_to_int(fp.read(8))
        self.sys_flag = fp.read(4)
        self.msg_born_timestamp = utils.byte_to_int(fp.read(8))
        self.born_addr = fp.read(8)
        self.msg_store_timestamp = utils.byte_to_int(fp.read(8))
        self.broker_addr = fp.read(8)
        self.reconsume_times = utils.byte_to_int(fp.read(4))
        self.transaction_offset = utils.byte_to_int(fp.read(8))
        self.msg_body_length = utils.byte_to_int(fp.read(4))
        self.msg_body = fp.read(self.msg_body_length).decode()
        self.topic_length = utils.byte_to_int(fp.read(1))
        self.topic = fp.read(self.topic_length).decode()
        self.properties_length = utils.byte_to_int(fp.read(2))
        self.properties = fp.read(self.properties_length).decode()


def parse_commitlog(fp: BinaryIO, offset):
    fp.seek(offset)
    commit_log = CommitLog(fp)
    print(commit_log.msg_body)


if __name__ == '__main__':
    commitlog_path = 'files/commitlog/00000000000000000000'
    utils.open_file_then(commitlog_path, 'rb', parse_commitlog, 312)
