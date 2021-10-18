import requests
import json
import csv

def listIssueNumber(repo):
	if(repo.strip() == ''):
		return "";
	response = requests.get("https://api.github.com/repos"+repo+"issues", headers={"Authorization":"token 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"})
	data = json.loads(response.text)
	label =[] 
	for f in data:
		label.append(f["number"])
	return label 


def listLabels(repo, iss):
	if(repo.strip() == ''):
		return "";
	labelSet = set() 
	response = requests.get("https://api.github.com/repos"+repo+"issues/"+str(iss)+"/labels", headers={"Authorization":"token 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"})
	data = json.loads(response.text)
	if(len(data)==0):
		return labelSet 
	for name in data:
		#issueName.append(name["name"])
		labelSet.add(name["name"])
	return labelSet;

def main():
	file = open('repo3','r')	
	repo_list= file.read().splitlines()
	f = open("labelout", "w")
	for repo in repo_list:
		csv =listIssueNumber(repo)
		print(repo)
		f.write(repo+"\n")
		for iss in csv:
			label = str(listLabels(repo,iss))
			print(str(iss)+"\t"+label+"\n")
			f.write(str(iss)+"\t"+label+"\n")
	f.close();
if __name__=="__main__":
	main()
