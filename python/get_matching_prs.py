import requests
import json
import pickle
import time


def listIssues(token, word_list):
	"""
		Get pull requests that have desired labels (in issues they fix) or words in their titles/descriptions
		TODO: Add support for label list
	"""

	combined_words = " ".join(word_list)
	page = 1
	data = []

	while True:
		get_url = f"https://api.github.com/search/issues?q={combined_words}+language:python+type:pr+state:closed+linked:issue&per_page=100&page={page}"
		response = requests.get(
			get_url, headers={"Authorization": "token: %s" % token})
		retobj = json.loads(response.text)
		
		# Keep track of data so far
		print(len(retobj), retobj['total_count'])
		
		# If no data, break
		if len(retobj["items"]) == 0:
			break
			
		# If there are data, append to list
		for item in retobj["items"]:
			title = item["title"]
			# labels = [x['name'] for x in item["labels"]]
			diff_url = item['pull_request']['diff_url']
			url = item['pull_request']['url']
			body = item['body']
			datum = [title, diff_url, url, body]
			data.append(datum)
			print(url)
		page += 1
		time.sleep(5)
	
	return data


def main(token):
	data = listIssues(token, ["security", "vulnerability"])

	# Save data
	with open('pr_information.pkl', 'wb') as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	token = "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"
	listIssues(token, ["security", "vulnerability"])
