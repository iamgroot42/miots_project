import json
import os
import git
from tqdm import tqdm
from pydriller import Repository
from subprocess import call, STDOUT

class Constants:
  # Words that should not appear in the filename, because it's a sign that the file is actually part of a demo, a hacking tool or something like that
  suspicious_words = set(["injection", "vulnerability", "exploit", " ctf",
                          "capture the flag", "ctf", "burp", "capture", "flag", "attack", "hack"])
  #words that should not appear in the commit message
  bad_words = set(["sqlmap", "sql-map", "sql_map", "ctf ", " ctf"])
  # Git dirs cache path
  git_dirs_cache_path = "git_dirs_cache"
  # Repos to skip
  bad_repos = ["h4ppyy/m-mooc", "cjbd/src",
               "pardeep11/frappe", "Benefactors/rosling", "aknoormohamed/engagex-frappe",
               "aknoormohamed/gsod-community-frappe", "philarin/Todo",
               "aknoormohamed/srilankan-frappe", "Renondedju/Uso-Bot",
               "kaitorecca/vafrappe", "Optimus922/shadowsocks", "attendanceproject/djattendance",
               "JustDoIt174/Memcrash", "moriarity1/sql", "pyreact0923/Django",
               "globaleaks/GLBackend-outdated", "LucidUnicorn/BUCSS-CTF-Framework",
               "HJoentgen/crawler_for_new_users", "AbsoluteVirtue/newsreel", 
               "wbrxcorp/forgetthespiltmilk", "deepnote/notebook", "globaleaks/GLBackend-outdated",
               "JuneLUNLV/mynote", "cjbd/swarming_client", "arturojosejr/mtgheirloom",
               "Halo4356/CSC3428", "r3valkyrie/vishnu", "kelvintsangwk/Software-Engineering-Project",
               "sjd8078/PDM-Project", "Kuki98/CecoZad-Flask", "starkajs/udacity_fswd_tournament",
               "BerentM/crimemap", "JulianneCrea/Relational-Database-Ebola-Data",
               "dandua98/291-Mini-Project-I", "xoes-oca/budget", "RyanYoung25/CS377",
               "max-neverov/stop", "dsrikrishna/fuzzy-fortnight", "pardeep11/erpnext",
               "willis62/Bolt", "LoHiiiiiii/FightCollector", "mw10178/ctplot_iw",
               "mw10178/ctplot-tuto", "cvdv87/cvdv_home_assistant", "bix29/ast",
               "Wenisatgithub/tng", "glipR/2DGraphics", "KeepyJ/odm", "caowencomeon/tng"
               ]


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
  repo_dir = os.path.join(Constants.git_dirs_cache_path,
                          repo_name.replace("/", "_"))
  if not os.path.exists(repo_dir):
    git.Repo.clone_from(repo_link, repo_dir)
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

  #Could not find commit with
  return None


# def prepare_file_data():
#     list(list(list(mapping.values())[0].values())[0]['files'].values())[0]['sourceWithComments']


if __name__ == "__main__":
    with open("vudenc/command_injection.json") as f:
        mapping = json.load(f)

    # Pull repos, etc
    for url, v in tqdm(mapping.items()):
        repo_name = url.split("https://github.com/")[1]

        # Skip if bad repo
        if repo_name in Constants.bad_repos:
            continue

        # Pull repo
        repo_dir = os.path.join(Constants.git_dirs_cache_path, repo_name.replace("/", "_"))
        if not os.path.exists(repo_dir):
            print(repo_name)
            git.Repo.clone_from(url + ".git", repo_dir)
        # for commit, datum in v.items():
        #     print(datum.keys())
        #     exit(0)
    # exit(0)
        
    for value in mapping.values():
        for commit_val in value.values():
            for file_content in commit_val['files'].values():
                print(file_content.keys())
                # print(file_content['sourceWithComments'])
                print(file_content['changes'][0]['remove'])
                exit(0)
                # before = file_content['sourceWithComments']
                # after = file_content['changes']
                # print(before)
                # print(after )
                # exit(0)
            # for file_ in commit_val['files'].values():
            #     print(file_.values())
            #     exit(0)
