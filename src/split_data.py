import json
import random
from pathlib import Path

SEED = 42
random.seed(SEED)

job_data = []

#Reading in JSON data 
with open("data/interim/labels_draft.jsonl", "r") as f:
    for line in f:
        clean_line = line.strip()
        if clean_line:
            job_data.append(json.loads(clean_line))

#Shuffle data in place
random.shuffle(job_data)

#splitting records into train/val/test
#70/15/15 respectively
n_train = int(0.70 * len(job_data))
n_val = int(0.15 * len(job_data))

train = job_data[:n_train]
val = job_data[n_train: n_train + n_val]
test = job_data[n_train + n_val:]

#Make sure the folder exists
Path("data/processed").mkdir(parents = True, exist_ok = True)

#Writing each set to jsonl in the data/processed folder
with open("data/processed/train.jsonl", "w") as f:
    for record in train:
        f.write(json.dumps(record) + "\n")
    
with open("data/processed/val.jsonl", "w") as f:
    for record in val:
        f.write(json.dumps(record) + "\n")

with open("data/processed/test.jsonl", "w") as f:
    for record in test:
        f.write(json.dumps(record) + "\n")

#Confirming sucessfull output
print(f'{len(train)} training records were sucessfully saved to data/processed/train.jsonl')
print(f'{len(val)} val records were sucessfully saved to data/processed/val.jsonl')
print(f'{len(test)} test records were sucessfully saved to data/processed/test.jsonl')
