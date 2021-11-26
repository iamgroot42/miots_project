# Mobile &amp; IoT Security: Course Project

## Setting up environment for featur extraction

Instructions are for maCOS

### Install Joern (version 0.3.1)

```bash
brew install sbt
brew install coreutils
git clone https://github.com/joernio/joern.git
cd joern
sbt stage
```

### Install neo4j (version 2.1.5)

You'll need to download and set it up on your machine (need sudo access)

### Install relevant python packages

```bash
pip install gensim==3.4
pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.6.0-py3-none-any.whl
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

## to run
### following command creates an oput file op
bash scrape.sh
#filers issues from op and cleans the data
bash opTorepo
python3 issueLabels.py 
creates the file labelout
python3 app.py
creates the file 

merge_commit is the final sha
base is the initial
