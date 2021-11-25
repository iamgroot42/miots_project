import requests
import json
import csv

	
	
def listIssues(repo):
	if(repo.strip() == ''):
		return "";
	#/apache/incubator-mxnet/
	
	response = requests.get("https://api.github.com/repos"+repo+"labels", headers={"Authorization":"token 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"})
	data = json.loads(response.text)
	label =[] 
	if ('message' in data) or len(data)==0 :
		return "";
	for f in data:
		label += [f["name"]]
	csv = ",".join(label);
	return csv

def main():
	file = open('repoPython','r')	
	topology_list = file.read().splitlines()
	f = open("allLabels.txt", "w")
	for i in topology_list:
		#print(i)
		#print(listIssues(i))
		f.write(i+"\t"+listIssues(i)+"\n")
	f.close()

if __name__=="__main__":
    main()
