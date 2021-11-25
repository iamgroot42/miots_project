import requests
import json
import csv
import re

	
	
def curl(repo):
	#/apache/incubator-mxnet/
	i = 1
	if(repo.strip() == ''):
		return "";
	while 1>0:
		response = requests.get("https://github.com"+repo+"issues?page="+str(i)+"&q=is%3Aissue+is%3Aclosed", headers={"Authorization":"token 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"})
		if response.text.find("Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title")==-1:
			break;
		location=response.text.find("octicon octicon-git-pull-request v-align-middle")
		if(location!=-1):
			x = re.search("a\shref=\".*?\"", response.text[location-700:location-100])
			if x!=None:
				f = open("output.txt", "a")
				f.write(x.group())
				f.write("\n")
				print(x.group())
		i += 1

def main():
	file = open('repoPython','r')	
	topology_list = file.read().splitlines()
	f = open("output.txt", "a")
	f.write("");
	f.close
	for i in topology_list:
		# print(i)
		curl(i);
	file.close()

if __name__=="__main__":
    main()
