import requests
import json
import csv

	
	
def listIssues(repo):
	if(repo.strip() == ''):
		return "";
	#/apache/incubator-mxnet/
	
	response = requests.get("https://api.github.com/repos"+repo+"labels", headers={"Authorization":"token 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"})
	#response = requests.get("https://api.github.com/repos/apache/incubator-mxnet/labels", headers={"Authorization":"token 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"})
	data = json.loads(response.text)
	label =[] 
	for f in data:
		label += [f["name"]]
	csv = ",".join(label);
	return csv

def main():
	file = open('repo3','r')	
	topology_list = file.read().splitlines()
	f = open("demofile3.txt", "w")
	for i in topology_list:
		#print(i)
		#print(listIssues(i))
		f.write(i+"\t"+listIssues(i)+"\n")
	f.close()

if __name__=="__main__":
    main()
