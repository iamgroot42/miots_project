import requests
import json
import pickle
from tqdm import tqdm
import time


def getDiscussion(token, url):
	"""
		Get all discussion threads of a PR
	"""

	if len(url) == 0:
		return []

	print(url)
	response = requests.get(url, headers={"Authorization": "token %s" % token})
	ts = int(response.headers['X-RateLimit-Reset'])
	retobj = json.loads(response.text)
	comments = []
	for comment in retobj:
		comments.append(comment["body"])
	return comments, ts


def main(token, keyword):
	# Read old data
	with open("pr_information/[%s].pkl" % keyword, "rb") as f:
		data = pickle.load(f)
	
	# Get discussion threads
	iterator = tqdm(data, total=len(data))
	for pr in iterator:
		comments_url = pr['comments_url']
		comments, ts = getDiscussion(token, comments_url)
		iterator.set_description("Remaining: %d" % ts)
		time.sleep(1)
	
		pr["comments"] = comments

	# Save data
	with open('pr_information_with_comments/[%s].pkl' % keyword, 'wb') as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
	import sys
	keyword = "vulnerability"
	if len(sys.argv) > 1:
		keyword = sys.argv[1]
	tokens = [
		"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",
		"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",
		"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",
		"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"
		"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",
		"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",
		"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",
	]
	main(tokens[0], keyword)
