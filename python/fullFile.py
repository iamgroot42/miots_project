import json
import re
import requests

def curl(line):
	f = open("fullfile.txt", "a")
	w=line.split("\t");
	x = re.sub("pulls.*","commits",w[0]);
	print(w[0]);
	print(w[1]);
	f.write(w[0]);
	f.write("\n");
	f.write(w[1]);
	f.write("\n");
	response = requests.get(x+"/"+w[1], headers={"Authorization":"token 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"})
	data = json.loads(response.text)
	if ('files' in data):
		for item in data['files']:
			if(item["status"]=="modified"):
				if(item['raw_url']==None):
					return
				f.write(item['raw_url']);
				f.write("\n");
				print(item['raw_url']);
	f.write(w[2])
	f.write("\n");
	print(w[2])

	response = requests.get(x+"/"+w[2], headers={"Authorization":"token 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"})
	data = json.loads(response.text)
	if ('files' in data):
		for item in data['files']:
			if(item["status"]=="modified"):
				if(item['raw_url']==None):
					return
				f.write(item['raw_url']);
				f.write("\n");
				print(item['raw_url']);


def main():
	file = open('pullDiff.tsv','r')	
	topology_list = file.read().splitlines()
	for i in topology_list:
		# print(i)
		curl(i);
	
if __name__=="__main__":
    main()

