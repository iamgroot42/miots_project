import json
import os
import git
from tqdm import tqdm
from pydriller import Repository
from myutils import removeDoubleSeperatorsString, stripComments


class Constants:
  # Words that should not appear in the filename, because it's a sign that the file is actually part of a demo, a hacking tool or something like that
  suspicious_words = set(["injection", "vulnerability", "exploit", " ctf",
                          "capture the flag", "ctf", "burp", "capture", "flag", "attack", "hack"])
  #words that should not appear in the commit message
  bad_words = set(["sqlmap", "sql-map", "sql_map", "ctf ", " ctf"])
  # Git dirs cache path
  git_dirs_cache_path = "git_dirs_cache"
  # Repos to skip (private/no longer exist)
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


def get_start_end_commits(repo_dir, merge_sha, filenames):
  """
    Look up commits for given PR, get identifiers
    for first commit, use that code as starting point.
  """
  # Iterate through repossitory commits
  repo = Repository(repo_dir)
  for commit in repo.traverse_commits():
    if commit.hash == merge_sha:
      files = {}
      # This is the real before-after stage for code
      for m in commit.modified_files:
        # Care about file modifications, not new/deleted ones
        if m.source_code_before == None or m.source_code == None:
          continue
        # Do not look at files that are too large
        elif len(m.source_code_before) > 30000:
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

  #Could not find commit with SHA hash
  return None


def dump_all_data(focus, counter=1):
    with open(f"vudenc/{focus}.json") as f:
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
            git.Repo.clone_from(url + ".git", repo_dir)

    save_dir_before = "vudenc_raw/before/"
    save_dir_after = "vudenc_raw/after/"
    # Now that repos have been all downloaded, process code to generate before/after snippets
    for url, value in tqdm(mapping.items()):
        repo_name = url.split("https://github.com/")[1]
        # Skip if bad repo
        if repo_name in Constants.bad_repos:
            continue
        repo_dir = os.path.join(Constants.git_dirs_cache_path, repo_name.replace("/", "_"))

        # For each before/after commit within this repository
        for commit_val in value.values():

            # Get SHA commit hash, filenames
            filenames = list(commit_val['files'].keys())
            sha_hash = commit_val['sha']

            files = get_start_end_commits(repo_dir, sha_hash, filenames)
            if files is not None:
                for v in files.values():
                    before_code = v['sourceWithComments']
                    after_code = v['sourcecodeafter']
                    # Save before/after files to disk
                    with open(save_dir_before + str(counter) + ".py", 'w') as f:
                        f.write(before_code)
                    with open(save_dir_after + str(counter) + ".py", 'w') as f:
                        f.write(after_code)
                    counter += 1
    return counter


if __name__ == "__main__":
    focus_trials = [x.split(".json")[0] for x in os.listdir("vudenc")]
    counter = 1

    for focus in focus_trials:
        counter = dump_all_data(focus, counter)
        print(f"Cumulative counter after {focus}: {counter}")
  