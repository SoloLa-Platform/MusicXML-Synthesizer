from pathlib import Path


def parse_notes_meta_to_list(file_path):

    result_list = []
    # detect non-exist file path
    fp = Path(file_path)
    if not fp.is_file():
        print("Path:{}, Contnet: {}".format("Invalid", ""))
    with open(file_path, 'r') as f:
        result_list = f.readlines()
    return result_list
