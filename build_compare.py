
import yaml
import json
from deepdiff import DeepDiff
import os

LOCAL_TABLES = "./local_tables/"
REMOTE_TABLES = "./remote_tables/"

def yaml_as_dict(my_file):
    my_dict = {}
    with open(my_file, 'r') as fp:
        docs = yaml.safe_load_all(fp)
        for doc in docs:
            for key, value in doc.items():
                my_dict[key] = value
    return my_dict

def compare_directories(dir1, dir2):
    """
    Compares two directories to find shared and unique files.

    Args:
        dir1 (str): Path to the first directory.
        dir2 (str): Path to the second directory.

    Returns:
        tuple: A tuple containing three sets:
               - shared_files: Files present in both directories.
               - only_in_dir1: Files present only in the first directory.
               - only_in_dir2: Files present only in the second directory.
    """
    try:
        set1 = set(os.listdir(dir1))
        set2 = set(os.listdir(dir2))
    except FileNotFoundError as e:
        print(f"Error: Directory not found - {e}")
        return set(), set(), set()

    shared_files = set1.intersection(set2)
    only_in_dir1 = set1.difference(set2)
    only_in_dir2 = set2.difference(set1)

    return shared_files, only_in_dir1, only_in_dir2





if __name__ == '__main__':

    shared_files, only_in_local, only_in_remote = compare_directories(LOCAL_TABLES, REMOTE_TABLES)
    print("Shared files:", shared_files)
    print("Only in local:", only_in_local)
    print("Only in remote:", only_in_remote)

    output = {
        "shared_files": {},
        "only_in_local": list(only_in_local),
        "only_in_remote": list(only_in_remote)
    }

    for file in sorted(shared_files):
        print(f"Comparing file: {file}")
        local_file_path = os.path.join(LOCAL_TABLES, file)
        remote_file_path = os.path.join(REMOTE_TABLES, file)
        a = yaml_as_dict(local_file_path)
        b = yaml_as_dict(remote_file_path)
        
        print(type(a))
        
        ddiff = DeepDiff(a, b, ignore_order=True)

        output['shared_files'][file] = {
            #"local": a,
            #"remote": b,
            "diff": ddiff
        }
        if len(ddiff) > 0:
            if 'dictionary_item_added' in ddiff:
                ddiff['dictionary_item_added'] = list(ddiff['dictionary_item_added'])
            if 'dictionary_item_removed' in ddiff:
                ddiff['dictionary_item_removed'] = list(ddiff['dictionary_item_removed'])
            # if 'values_changed' in ddiff:
                # ddiff['values_changed'] = list(ddiff['values_changed'])


    json.dump(output, open("compare_output.json", "w"), indent=4)