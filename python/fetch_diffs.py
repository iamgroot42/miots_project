import pickle
import requests
from tqdm import tqdm
import os
import time


def get_filename_from_url(url):
    prefix = "https://github.com/"
    url = url.replace(prefix, "")
    url = url.replace("/", "_")
    return url


def get_diff(datum, token, store_folder):
    # Extract URL for the diff
    url = datum['diff_url']

    response = requests.get(url, headers={"Authorization": "token %s" % token})
    diffcontent = response.content.decode('utf-8', errors='ignore')
    
    if ".py" not in diffcontent:
        # Treat as blank diff (will purge later)
        diffcontent = ""
    
    # Write diff to file
    filename = os.path.join(store_folder, get_filename_from_url(url))
    with open(filename, 'w') as f:
        f.write(diffcontent)


if __name__ == "__main__":
    store_folder = "diffs"
    token = "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"

    with open('all_pr_info.pkl', 'rb') as f:
        data = pickle.load(f)

    # Skip diffs that have already been downloaded
    data = [x for x in data if not os.path.exists(
        os.path.join(store_folder, get_filename_from_url(x['diff_url'])))]

    for d in tqdm(data):
        get_diff(d, token, store_folder)
        time.sleep(0.5)
