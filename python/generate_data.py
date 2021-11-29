"""
  Based on https://github.com/LauraWartschinski/VulnerabilityDetection
  With modifications for file format
"""
import time
import pickle
import os
from pydriller import Repository
from git import Repo
import requests
from tqdm import tqdm
import numpy as np
from myutils import getBadpart, removeDoubleSeperatorsString, stripComments, get_filename_from_url


class Constants:
  # Words that should not appear in the filename, because it's a sign that the file is actually part of a demo, a hacking tool or something like that
  suspicious_words = set(["injection", "vulnerability", "exploit", " ctf",
                     "capture the flag", "ctf", "burp", "capture", "flag", "attack", "hack"])
  #words that should not appear in the commit message
  bad_words = set(["sqlmap", "sql-map", "sql_map", "ctf ", " ctf"])
  # pydriller DB cache path
  pydriller_cache_path = "pydriller_cache"
  # Authorization token
  token = "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"
  # Git dirs cache path
  git_dirs_cache_path = "git_dirs_cache"


def getChanges(rest):
  """
    Extracts the changes from pure .diff file
  """
  
  changes = []
  # Start by parsing diff header
  while ("diff --git" in rest):
    start = rest.find("diff --git") + 1
    secondpart = rest.find("index") + 1

    # Get the title line which contains the file name
    titleline = rest[start:secondpart]
    if not (".py") in titleline:
      # No python file changed in this part of the commit
      rest = rest[secondpart + 1]
      continue

    # Use start of next diff to get the changes
    if "diff --git" in rest[start:]:
      end = rest[start:].find("diff --git")
      filechange = rest[start:end]
      rest = rest[end:]
    else:
      end = len(rest)
      filechange = rest[start:end]
      rest = ""

    filechangerest = filechange

    # Extract all singular changes, which are recognizable by the @@ marking the line number
    while ("@@" in filechangerest):
      
      change = ""
      start = filechangerest.find("@@")+2
      start2 = filechangerest[start:start+50].find("@@")+2
      start = start+start2
      filechangerest=filechangerest[start:]
      
      if ("class" in filechangerest or "def" in filechangerest) and "\n" in filechangerest:
        filechangerest = filechangerest[filechangerest.find("\n"):]
      
      if "@@" in filechangerest:
          end = filechangerest.find("@@")
          change = filechangerest[:end]
          filechangerest = filechangerest[end+2:]
          
      else:
        end = len(filechangerest)
        change = filechangerest[:end]
        filechangerest = ""
        
      if len(change) > 0:
        # Replace titleline with filename
        changes.append([change, titleline])
  
  return changes


def getFilename(titleline):
  """
    Extracts the filename from the title line of a diff file
  """
  s = titleline.find(" a/")+2
  e = titleline.find(" b/")
  name = titleline[s:e]
  
  if titleline.count(name) == 2:
    return name
  elif ".py" in name and (" a"+name+" " in titleline):
    return name
  else:
    print(titleline, "wow!")
    print("couldn't find name")
    print(titleline)
    print(name)


def makeChangeObj(change, titleline):
  """
    For a single chamge consisting of titleline and change, create a usable object by extracting relevant information
  """
  
  # Ignore HTML changes
  if "<html" in change:
    print("HTML Change: Ignore")
    return None
  
  # Ignore SAGE-based changes
  if "sage:" in change or "sage :" in change:
    print("Sage Change: Ignore")
    return None
  
  thischange = {}

  if getBadpart(change) is not None:      
    badparts = getBadpart(change)[0]
    goodparts = getBadpart(change)[1]
    linesadded = change.count("\n+")
    linesremoved = change.count("\n-")
    thischange["diff"] = change
    thischange["add"] = linesadded
    thischange["remove"] = linesremoved
    thischange["filename"] = getFilename(titleline)
    thischange["badparts"] = badparts
    thischange["goodparts"] = []
    if goodparts is not None:
      thischange["goodparts"] = goodparts
    if thischange["filename"] is not None:
      return thischange

  return None


def get_start_end_commits(datum, filenames):
  """
    Look up commits for given PR, get identifiers
    for first commit, use that code as starting point.
  """
  pr_url = datum["url"]

  # Extract repo name from diff url
  repo_name = pr_url.split("/repos/")[1].split("/pulls")[0]
  repo_link = "https://github.com/" + repo_name + ".git"

  # Use cached repo, if available
  repo_dir = os.path.join(Constants.git_dirs_cache_path, repo_name.replace("/", "_"))
  if not os.path.exists(repo_dir):
    Repo.clone_from(repo_link, repo_dir)
  else:
    print("[Using cached repository]")

  # Get sha hashes for given PR
  # merge_sha, first_commit_sha = get_relevant_sha(pr_url)
  merge_sha = get_relevant_sha(pr_url)

  first_commit_hash = None
  # Iterate through repossitory commits
  repo = Repository(repo_dir, to_commit=first_commit_hash)
  for commit in tqdm(repo.traverse_commits()):
    # First case: commits were squashed
    # Second case: commits were not squashed
    # if commit.hash == merge_sha or commit.hash == first_commit_sha:
    if commit.hash == merge_sha:
      files = {}
      # This is the real before-after stage for code
      for m in commit.modified_files:
        # Care about file modifications, not new/deleted ones
        if m.source_code_before == None or m.source_code == None:
          print("[New/Delete file]")
          continue
        # Do not look at files that are too large
        elif len(m.source_code_before) > 30000:
          print("[File too long]")
          continue
        # We only care about python files that were modified
        elif ("/" + m.old_path) in filenames:
          # Keep track of 'before without comments', 'before', 'after'
          source = "\n" + \
              removeDoubleSeperatorsString(
                  stripComments(m.source_code_before))
          sourceWithComments = m.source_code_before
          sourcecodeafter = m.source_code

          files[m.old_path] = {
            "source": source,
            "sourceWithComments": sourceWithComments,
            "sourcecodeafter": sourcecodeafter
          }
      return files

  raise ValueError("Could not find commit with sha {}".format(merge_sha))


def get_relevant_sha(pr_url):
  """
    Using PR link, get sha hash for commit just at the beginning of the PR.
    If commits are squashed, corresponds to merge-sha.
    If commits are not squashed, corresponds to first commit's hash.
    Consider whichchever sha appears first while downloading repository.
  """
  commits_url = pr_url + "/commits"
  # Get merge commit hash (for the case where commits were merged)
  response = requests.get(pr_url, headers={
                          "Authorization": "token %s" % Constants.token})
  merge_hash = response.json()["merge_commit_sha"]
  time.sleep(0.5)
  # response = requests.get(commits_url, headers={
  #                         "Authorization": "token %s" % Constants.token})
  # diffcontent = response.json()
  # time.sleep(0.5)
  # # Get hash of earliest commit in PR
  # first_commit_hash = diffcontent[0]["sha"]
  return merge_hash
  return merge_hash, first_commit_hash


def load_diffs_with_labels(dir, diffs_dir):
  """
    Load per-keyword (or label) data, and fetch corresponding diff from database
  """
  per_label_data = {}
  for tag_file in tqdm(os.listdir(dir)):
    data_for_this_label = pickle.load(open(os.path.join(dir, tag_file), 'rb'))
    if len(data_for_this_label) == 0:
      continue
  
    data = []
    if len(per_label_data) == 10:
      break

    # All PRs with this category
    for datum in data_for_this_label:
      # Fetch diff_file from diffs_dir
      diff_file_path = os.path.join(
          diffs_dir, get_filename_from_url(datum["diff_url"]))
      with open(diff_file_path, 'r') as diff_file:
        diff = diff_file.read()
    
      # If diff is empty, simply ignore datapoint
      if len(diff.strip()) == 0:
        continue

      # Remove 'diff_url', replace with 'diff' content
      del datum["diff_url"]
      datum["diff"] = diff

      # Add to data
      data.append(datum)
      break
    
    per_label_data[tag_file] = data

  return per_label_data


def get_relevant_prs(data):
  """
    Filter out pull requests before downloading relevant code repositories
  """
  # Only look at files that do not have bad words in title/body of PR
  check_bad_presence = lambda x: len(set(x.lower().split()).intersection(Constants.bad_words)) > 0
  if np.any([check_bad_presence(x['title']) for x in data]):
    return None
  if np.any([check_bad_presence(x['body']) for x in data]):
    return None

  for i, entry in enumerate(data):
    # Process diff file
    entries = getChanges(entry["diff"])

    if len(entries) == 0:
      continue

    # Only look at files that do not have suspicious words in the filename
    check_sus_presence = lambda x: np.any([c in x for c in Constants.suspicious_words])
    if np.any([check_sus_presence(x[1].lower()) for x in entries]):
      return None
    
    # Only care about python files changes
    entries = [x for x in entries if ".py" in x[1]]

    # Convert to change objects
    entries = [makeChangeObj(*x) for x in entries]
    entries = [x for x in entries if x is not None]

    if len(entries) == 0:
      continue

    data[i]["changes"] = entries

  # Filter out PRs that do not have changes
  data = [x for x in data if "changes" in x]
  return data


if __name__ == "__main__":
  # Load list of all repositories and pull request diffs
  label_wise_data = load_diffs_with_labels("pr_information", "diffs")
  # keyword: [PR1, PR2, ...]

  # Filter and keep desired PRs
  for label, data in label_wise_data.items():
    label_wise_data[label] = get_relevant_prs(data)
  
  # Delete labels with no data
  for label, data in list(label_wise_data.items()):
    if data is None:
      del label_wise_data[label]

  # Get final before/after dataset
  for label, data in label_wise_data.items():
    for i, datum in tqdm(enumerate(data), total=len(data)):
      filenames = [x['filename'] for x in datum["changes"]]
      files = get_start_end_commits(datum, filenames)
      # Store file information in data
      label_wise_data[label][i]["files"] = files
  
    # Save data (per label, to avoid failures)
    if len(label_wise_data[label]) > 0:
      with open('final_data/%s' % label, 'wb') as f:
        pickle.dump(label_wise_data[label], f, pickle.HIGHEST_PROTOCOL)
        print("Done with %s [Saved] | %d datapoints" %
              (label, len(label_wise_data[label])))
    else:
      print("Skipped %s" % label)
