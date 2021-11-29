import os
import pickle
from tqdm import tqdm

counter = 1
for fn in os.listdir('final_data'):
    with open('final_data/' + fn, 'rb') as f:
        data = pickle.load(f)
        for d in tqdm(data):
            for _, fc in d['files'].items():
                relevant_content = fc['sourcecodeafter']
                # Save file to filedump folder
                with open(f'filedump/{counter}.py', 'w') as f:
                    f.write(relevant_content)
                    counter += 1
