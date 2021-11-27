import requests
import json
import pickle


def listIssues(token, keyword):
	"""
		Get pull requests that have desired labels (in issues they fix) or words in their titles/descriptions
		TODO: Add support for label list
	"""

	page = 1
	data = []

	wanted_params = {
		'language': 'python',
		'archived': 'false',
		'type': 'pr',
		'state': 'closed',
		'linked': 'issue',
		'comments': '>2',
		'is': 'merged'
	}
	params_string = "+".join(["%s:%s" % (k, v) for k, v in wanted_params.items()])

	while True:
		get_url = f"https://api.github.com/search/issues?q={keyword}+{params_string}&per_page=100&page={page}"
		response = requests.get(
			get_url, headers={"Authorization": "token: %s" % token})
		retobj = json.loads(response.text)
		
		# If no data, break
		if 'items' not in retobj:
			print(retobj)
			exit(0)

		if len(retobj["items"]) == 0:
			break
		
		# Keep track of data so far
		print("%d / %d" % (len(data), retobj['total_count']))
			
		# If there are data, append to list
		for item in retobj["items"]:
			title = item["title"]
			# labels = [x['name'] for x in item["labels"]]
			diff_url = item['pull_request']['diff_url']
			url = item['pull_request']['url']
			body = item['body']
			issue_url = item.get('issue_url', "")
			comments_url = item.get('comments_url', "")
			datum = {
				'title': title,
				'diff_url': diff_url,
				'url': url,
				'body': body,
				'issue_url': issue_url,
				'comments_url': comments_url
			}
			data.append(datum)
		page += 1

	return data


def main(token, keyword):
	# Get all data
	data = listIssues(token, keyword)

	# Save data
	with open('pr_information/[%s].pkl' % keyword, 'wb') as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	keyword = "security"
	token = "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"
	main(token, keyword)
