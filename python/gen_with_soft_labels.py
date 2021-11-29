import os
import json
from tqdm import tqdm
import subprocess


if __name__ == "__main__":
    mapping = {}
    sec_level = "low"
    corpus_dir = "filedump"
    iterator = tqdm(os.listdir(corpus_dir))
    found_count = 0
    for filename in iterator:
        # Make system-call for bandit
        joined_path = os.path.join(corpus_dir, filename)
        # Try processing results (won't work if parsing failed)
        try:
            result = subprocess.check_output(
                f"bandit --configfile bandit.yaml -q -f json -ii {joined_path}",
                shell=True)
            parsed_results = json.loads(result)['results']
        except:
            continue

        mapping[filename] = parsed_results
        if len(parsed_results) > 0:
            found_count += 1
        iterator.set_description(f"Found {found_count} files with vulnerabilities")
    
    # Save mapping to file
    with open(f'mapping_{sec_level}.json', 'w') as f:
        json.dump(mapping, f)
