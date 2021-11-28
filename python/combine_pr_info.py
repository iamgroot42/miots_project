import pickle
import os


def get_pr_files(dir, all_data):
    # Open all the files in the directory
    for file in os.listdir(dir):
        try:
            data = pickle.load(open(os.path.join(dir, file), 'rb'))
            for datum in data:
                all_data[datum['url']] = datum
        except:
            print("Skipping", file)
    return all_data


if __name__ == "__main__":
    # Get the data from the directory
    data = {}
    paths = ['pr_information', 'pr_information_labels']
    for path in paths:
        data = get_pr_files(path, data)
    
    data = list(data.values())

    # Save back into one big pickle file
    with open('all_pr_info.pkl', 'wb') as f:
	    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
