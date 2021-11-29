# Mobile &amp; IoT Security: Course Project

## Setting up environment for feature extraction

Instructions are for maCOS

### Install relevant python packages

```bash
pip install pydriller
pip install gensim
pip install bytecode
pip install bandit
```

## Preparing Data

## Preparing issue-based dataset

1. Get list of popular repositories

`python get_popular_repos.py`

2. Fetch issue labels for all repositories

`python get_issue_labels.py`

3. Fetch closed PRs with specified keywords

`python get_matching_prs.py`

4. Fetch closed PRs with specified issue labels

`python get_issue_match_prs.py`

5. Combine keyword-wise PRs (information) into single pickle file

`python combine_pr_info.py`

7. Fetch diffs corresponding to each PR

`python fetch_diffs.py`

8. Download relevant files, retrieve dataset using diffs

`python generate_data.py`

9. Save files to disk, to be used with soft-label generation

`python retrieve_and_dump.py`

10. Generate soft-labels for each file

`python gen_with_soft_labels.py`


## Training LM for language-based analysis

1. Collect repository data

`python w2v_pythoncorpus.py`

2. Clean corpus

`python w2v_cleancorpus.py`

3. Finetune CodeBERT LM

`python lm_trainmodel.py`


# Updates in the pipeline

1. Doubled the dataset size (number of repos) for the Language Model, based on various sources: Github Trending, GitMostWanted
2. Explore Transformer-based language model: trainining from scratch, as well as existing CodeBERT (finetune and raw)
