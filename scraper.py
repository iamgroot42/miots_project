import requests
import json
import csv
import re
	
	
def curl(url):
	if(url.strip() == ''):
		return "";
	#/apache/incubator-mxnet/
	
	response = requests.get(url, headers={"Authorization":"token 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"})
	data = json.loads(response.text)
	if ('message' in data) or len(data)==0 :
		return "";
	first = (data[0]["sha"])
	last = (data[len(data)-1]["parents"][0]["sha"])
	x = re.search("\/repos\/.*?\/.*?\/", url)
	diff = "null"
	if x!=None:
		diff = "https://github.com"+x.group()[6:]+"compare/"+first+"..."+last+".diff";
	ans =(url+"\t"+first+",\t"+last+",\t"+diff+"\n")
	print(ans)
	return ans

def main():
	file = open('testOutII','r')	
	topology_list = file.read().splitlines()
	f = open("akash.tsv", "w")
	for i in topology_list:
		f.write(curl(i))
	f.close()

if __name__=="__main__":
    main()
