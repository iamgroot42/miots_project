# Mobile &amp; IoT Security: Course Project

## Setting up environment for feature extraction

Instructions are for maCOS

### Install relevant python packages

```bash
pip install pydriller


```

## Preparing Data

### Parsing files using Joern

1. Start server in one terminal

```bash
cd $JOERN
./joern-server
```

2. Import code in second terminal

```bash
cd $JOERN
tar -cvf testCode.tar.gz testCode
joern-import testCode.tar.gz
```

# Set up tree parsing for Python

1. `pip install tree_sitter`

2. First you'll need a Tree-sitter language implementation for each language that you want to parse.
    `git clone https://github.com/tree-sitter/tree-sitter-python`

3. Use the `Language.build_library` method to compile these into a library that's usable from Python.

    `Language.build_library('build/my-languages.so', ['./tree-sitter-python'])`


# Preparing issue-based dataset

1. Get list of popular repositories

`python get_popular_repos.py`

2. Fetch issue labels for all repositories

`python get_issue_labels.py`

## to run
### following command creates an oput file op
bash scrape.sh
#filers issues from op and cleans the data
bash opTorepo
python3 issueLabels.py 
creates the file labelout
python3 app.py
creates the file allLabels.txt
python3 pullScarper consumes repoPython and out puts output.txt
need to do a bit more data wrangling to get pullDiff.tsv
the files are filterOutput2.txt.sh  filterOutput.txt.sh   


example of issueLabelmicro
/actionless/pikaur/
601 set()
600 set()

allLabels.txt
/actionless/pikaur/ bug,discussion,duplicate,enhancement,feature,good first issue,hacktoberfest-accepted,help wanted,in progress,info,invalid,need info,not a bug,question,submitter gone,upstream issue,wontfix,z_#3E0982,z_light_purple



example of output.txt
/horovod/horovod/issues/146/linked_closing_reference?reference_location=REPO_ISSUES_INDEX


example of pull diff
https://api.github.com/repos/actionless/pikaur/pulls/593    c7a99109a268c8be07ff1a42bbc798fee2c3a214    cbad87e3e44c27df85f8ba7c5d1a455906c8c764    https://github.com/actionless/pikaur/compare/c7a99109a268c8be07ff1a42bbc798fee2c3a214...cbad87e3e44c27df85f8ba7c5d1a455906c8c764.diff



form is like 
pull
initial sha
list of files
final sha
list of files

https://api.github.com/repos/actionless/pikaur/pulls/593
c7a99109a268c8be07ff1a42bbc798fee2c3a214
https://github.com/actionless/pikaur/raw/c7a99109a268c8be07ff1a42bbc798fee2c3a214/pikaur/aur.py
...
cbad87e3e44c27df85f8ba7c5d1a455906c8c764
https://github.com/actionless/pikaur/raw/cbad87e3e44c27df85f8ba7c5d1a455906c8c764/packaging/usr/share/zsh/site-functions/_pikaur


merge_commit is the final sha
base is the initial


# Updates in the pipeline

1. Doubled the dataset size (number of repos) for the Language Model, based on various sources: Github Trending, GitMostWanted
2. Explore Transformer-based language model: trainining from scratch, as well as existing CodeBERT (finetune and raw)
