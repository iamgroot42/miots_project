from transformers import AutoTokenizer, AutoModelForMaskedLM
from torch.utils.data import DataLoader
import torch as ch
import os
import numpy as np
import json
from tqdm import tqdm
import torch.nn as nn
from sklearn.model_selection import train_test_split


def read_crossvul_data(dir):
    """
        Read CrossVul dataset 
    """
    X, Y = [], []
    for dp in os.listdir(dir):
        # Check if dp is directory
        if not os.path.isdir(os.path.join(dir, dp)):
            continue
        for fp in os.listdir(os.path.join(dir, dp, "py")):
            if fp.startswith("good_"):
                Y.append(1)
            else:
                Y.append(0)
            with open(os.path.join(dir, dp, "py", fp,), "r") as f:
                X.append(f.read())
    return X, Y


def read_custom_data(filedir="filedump", label_path="git_mapping.json"):
    """
        Read cusom git data
    """
    with open(label_path, 'r') as f:
        git_mapping = json.load(f)
    X, Y = [], []
    # Load good files
    for fpath in git_mapping["good"]:
        with open(os.path.join(filedir, fpath), 'r') as f:
            code = f.read()
            X.append(code)
            Y.append(0)
    # Load bad files
    for fpath in git_mapping["good"]:
        with open(os.path.join(filedir, fpath), 'r') as f:
            code = f.read()
            X.append(code)
            Y.append(1)
    return X, Y


class BasicDataset(ch.utils.data.Dataset):
    """
        Basic dataset wrapper
    """

    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def get_model_and_tokenizer(path):
    """
        Load and prepare language model and tokenizer
    """
    model = AutoModelForMaskedLM.from_pretrained(
        "huggingface/CodeBERTa-small-v1")
    model = nn.DataParallel(model)
    model.load_state_dict(ch.load(path))
    model.cuda()
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained("huggingface/CodeBERTa-small-v1")
    return model, tokenizer


def get_embedding(code, model, tokenizer):
    """
        Get embeddings for given code using LM
    """
    # Read code in chunks of tokenizer size
    max_length = 512
    # Divide file into chunks
    at_most_chunks = 5

    result = tokenizer(
            code,
            return_tensors="pt",
            return_attention_mask=True)

    start = 0
    embeddings = []
    at_most_chunks = min(5, int(np.ceil(len(result["input_ids"]) / max_length)))
    for i in range(at_most_chunks):
        iid = result['input_ids'][:, start: start + max_length].cuda()
        am = result['attention_mask'][:, start: start + max_length].cuda()

        # Run LM
        embedding = model(input_ids=iid,
                          attention_mask=am,
                          output_hidden_states=True)
        # Last layer, last token
        embedding = embedding['hidden_states'][-1][:, -1].detach().cpu()
        embeddings.append(embedding)
        start += max_length

    # Get mean (across dim) embedding across all tokens
    embeddings = ch.cat(embeddings, 0)

    return embedding


def basic_model(dim=768):
    """
        Build basic model
    """
    return nn.Sequential(
        nn.Linear(dim, 128),
        nn.ReLU(),
        nn.Linear(128, 16),
        nn.ReLU(),
        nn.Linear(16, 1),
    )


def get_dataset(X, Y, lm_model, tokenizer):
    """
        Make dataset object using code and labels
    """
    X_emb = []
    for code in tqdm(X):
        embedding = get_embedding(code, lm_model, tokenizer)
        X_emb.append(embedding)
    X_emb = ch.cat(X_emb, 0)
    ds = BasicDataset(X_emb, Y)
    return ds


def prepare_loaders(code_train, y_train, code_val, y_val, lm_model, tokenizer, batch_size=32):
    """
        Make Dataset objects from given data, and then prepare dataloaders
    """
    ds_train = get_dataset(code_train, y_train, lm_model, tokenizer)
    ds_val = get_dataset(code_val, y_val, lm_model, tokenizer)
    # Make loaders
    train_loader = DataLoader(ds_train, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(ds_val, batch_size=batch_size, shuffle=False)
    return train_loader, val_loader


def epoch(model, e, loader, optim, is_train=True):
    """
        Single epoch (train or validation)
    """
    if is_train:
        model.train()
        optim.zero_grad()
        prefix = "Train"
    else:
        model.eval()
        prefix = "Val"

    loss_fn = nn.BCEWithLogitsLoss()
    iterator = tqdm(loader)
    total_loss, total_items, total_acc = 0, 0, 0
    with ch.set_grad_enabled(is_train):
        for batch in iterator:
            X, y = batch
            X = X.cuda()
            y = y.float().cuda()

            # Forward pass
            logits = model(X)[:, 0]
            loss = loss_fn(logits, y)

            if is_train:
                # Backprop
                loss.backward()
                optim.step()
                optim.zero_grad()

            # Get predictions and then accuracy
            preds = (logits.sigmoid() > 0.5).float()
            acc = (preds == y).float().sum()
            # print(y, preds)

            total_loss += loss.item() * X.shape[0]
            total_acc += acc.item()
            total_items += len(X)

            iterator.set_description(
                f"Epoch {e}: {prefix} | Loss: {total_loss / total_items:.4f} | Accuracy: {100 * total_acc / total_items:.2f}")

    return total_loss / total_items


def train(train_loader, val_loader, epochs=10, lr=1e-2):
    """
        Train model using given data-loaders
    """
    # Build model
    model = basic_model().cuda()
    optim = ch.optim.Adam(model.parameters(), lr=lr)

    print("[Env] Training")
    for e in range(1, epochs+1):
        train_loss = epoch(model, e, train_loader, optim, is_train=True)
        val_loss = epoch(model, e, val_loader, optim, is_train=False)
        print()


if __name__ == "__main__":
    print("[Model] Loading LM model")
    model_path = "relevant_lm.pt"
    lm_model, tokenizer = get_model_and_tokenizer(model_path)
    # content = open("filedump/1.py").read()
    # get_embedding(content, lm_model, tokenizer)

    # Read CrossVul dataset
    print("[Data] Reading datasets")
    X_1, Y_1 = read_crossvul_data("../crossvul_dataset/dataset_final_sorted")
    X_2, Y_2 = read_custom_data()
    print("[Data] Label balance: %.2f" % (sum(Y_1) / len(Y_1)))
    print("[Data] Label balance: %.2f" % (sum(Y_2) / len(Y_2)))
    X = X_1 + X_2
    Y = Y_1 + Y_2

    # Split into train,val data
    print("[Data] Tokenizing dataset and preparing loaders")
    X_train, X_val, Y_train, Y_val = train_test_split(
        X, Y, test_size=0.2, random_state=42)
    train_loader, test_loader = prepare_loaders(
        X_train, Y_train, X_val, Y_val, lm_model, tokenizer,
        batch_size=4)

    # Train model
    train(train_loader, test_loader, epochs=100, lr=1e-4)
