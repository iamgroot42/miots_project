import requests
import json
import pickle
import time
from datetime import datetime, timedelta


def listIssues(tokens, keyword):
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
		'comments': '>3',
		'is': 'merged'
	}
	params_string = "+".join(["%s:%s" % (k, v) for k, v in wanted_params.items()])
	use_token = 0

	while True:
		get_url = f"https://api.github.com/search/issues?q={keyword}+{params_string}&per_page=99&page={page}"
		response = requests.get(
			get_url, headers={"Authorization": "token %s" % tokens[use_token]})
		retobj = json.loads(response.text)
		remaining = int(response.headers['X-RateLimit-Remaining'])
		print("Remaining: %d" % remaining)
		ts = int(response.headers['X-RateLimit-Reset'])
		hours_adjust_utc = timedelta(hours=5)
		print((datetime.utcfromtimestamp(ts)-hours_adjust_utc).strftime('%Y-%m-%d %H:%M:%S'))
		if remaining < 2:
			use_token = (use_token + 1)
			print(f"Switching to token {use_token}")
			if use_token == len(tokens):
				raise Exception("All tokens used!")
		
		# If maximum allowance reached, break
		if 'message' in retobj:
			if "only the first 1000 search results are available" in retobj['message'].lower():
				break

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
		time.sleep(2)

	return data


def main(token, keyword):
	# Get all data
	data = listIssues(token, keyword)

	# Save data
	with open('pr_information/[%s].pkl' % keyword, 'wb') as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	import sys
	keyword = "vulnerability"
	if len(sys.argv) > 1:
		keyword = sys.argv[1]
	tokens = [
		# "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",
		# "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",
		"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",
		"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"
		"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",
		"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",
		"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",
	]
	main(tokens, keyword)
