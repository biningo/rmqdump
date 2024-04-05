def byte_to_int(byte_arr):
    return int.from_bytes(byte_arr, 'big')


def open_file_then(filepath, mode, callback, *args, **kwargs):
    with open(filepath, mode) as fp:
        callback(fp, *args, **kwargs)
