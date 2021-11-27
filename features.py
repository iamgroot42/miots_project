import ast
import torch as ch
from transformers import AutoTokenizer, AutoModel
  

# Make AST for given code
def ast_feature(path):
    with open(path, 'r') as f:
        abstract_tree = ast.parse(f.read())
    


def get_codeberta_transformation(text):
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")
    nl_tokens = tokenizer.tokenize(text)
    tokens=[tokenizer.cls_token]+nl_tokens+[tokenizer.sep_token]+code_tokens+[tokenizer.sep_token]
    tokens_ids=tokenizer.convert_tokens_to_ids(tokens)
    context_embeddings=model(ch.tensor(tokens_ids)[None,:])[0]


def get_dfg_representation(text):