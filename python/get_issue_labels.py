import requests
import json
from tqdm import tqdm
import time
import os


def listIssues(repo, token):
	"""
		Get list of issues for a given repository
	"""
	if(repo.strip() == ''):
		return ""
	
	if repo[-1] != '/':
		repo = repo + '/'
	# Expects data to be in owner_name/repo_name format
	
	response = requests.get("https://api.github.com/repos/" + repo + "labels", headers={"Authorization": "token: %s" % token})
	data = json.loads(response.text)
	label =[] 

	# Bad repo
	if len(data) == 0:
		return ""

	if ('message' in data):
		print("Paused at %s" % repo)
		print(data["message"])
		time.sleep(1)
		if "API rate limit exceeded" in data['message']:
			time.sleep(34)
		return ""

	for f in data:
		label += [f["name"]]
	csv = ",".join(label)
	print(csv)

	return csv

def main(token):
	file = open('python_repos.txt','r')	

	# Read file, get list of duplicates
	repo_list = file.read().splitlines()
	repo_list = list(set(repo_list))

	# Read file if exists
	all_labels = []
	if os.path.exists('all_labels.txt'):
		prev_names = []
		file = open('all_labels.txt','r')
		all_labels = file.read().splitlines()
		prev_names = [x.split('\t')[0] for x in all_labels]

		print(len(repo_list), ":", len(prev_names))
		repo_list = list(set(repo_list) - set(prev_names))

	# Get labels for each repo
	with open("all_labels.txt", "a") as f:
		for i in tqdm(repo_list):
			listed_labels = listIssues(i, token)
			f.write(i + "\t" + listed_labels + "\n")
			if len(listed_labels) > 0:
				repo_list.append(listed_labels)
				time.sleep(2)


if __name__=="__main__":
	token = "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"
	main(token)
