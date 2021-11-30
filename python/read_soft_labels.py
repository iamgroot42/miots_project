import os
import json


if __name__ == "__main__":
    with open("medium_filedump.json") as f:
        filedump = json.load(f)
    
    bad_files = set()
    wanted_keys = ['line_range', 'test_id', 'filename']
    for result in filedump['results']:
        bad_files.add(result['filename'].split('/')[-1])

    good_files = list(os.listdir("filedump"))
    good_files = list(set(good_files) - bad_files)
    bad_files = list(bad_files)
    mapping = {
        'good': good_files,
        'bad': bad_files
    }
    # Save mapping
    with open("git_mapping.json", "w") as f:
        json.dump(mapping, f)
