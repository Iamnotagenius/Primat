import json
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import simplex as sim

with open('examples.json', 'r') as f:
    examples = json.load(f)

def json_to_str(jdata):
    return json.dumps(jdata, ensure_ascii=False).replace("'", '"')

for example in examples:
    print(json_to_str(example["task"]))