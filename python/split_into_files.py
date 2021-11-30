"""
    Read large corpus and split into individual files.
    For analyzing file-wise data
"""
import os
from tqdm import tqdm


if __name__ == "__main__":
    corpus_path = "../VulnerabilityDetection/Code/w2v/pythontraining_edit_all.txt"
    corpus_save_dir = "corpus_dir"

    # Read main corpus file
    with open(corpus_path, 'r') as f:
        all_data = f.read()
    
    # Split by double newline
    all_data = all_data.split('\n\n\n\n')

    # Save to file
    for i, datum in tqdm(enumerate(all_data), total=len(all_data)):
        with open(os.path.join(corpus_save_dir, str(i+1) + '.txt'), 'w') as f:
            f.write(datum)
