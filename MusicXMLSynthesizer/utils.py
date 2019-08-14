from pathlib import Path

def parse_notes_meta_to_list(file_path):

    result_list = []
    # detect non-exist file path
    fp = Path(file_path)
    if not fp.is_file():
        print("Path:{}, Contnet: {}".format("Invalid", ""))
        return 

    with open(file_path, 'r') as f:
        result_list = f.readlines()
    return result_list


def write_file(output_path, xml=""):
    fp = Path(output_path)
    print()

    parent_dir_path = fp.parents[0]
    if not parent_dir_path.exists() and not parent_dir_path.is_dir():
        print('not exist')
        Path.mkdir(parent_dir_path)

    file = open(output_path, "w+")
    file.write(xml)

    print('done')
