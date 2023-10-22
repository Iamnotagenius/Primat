import simplex as sim
import json

with open('examples.json', 'r') as f:
    examples = json.load(f)

def json_to_str(jdata):
    return json.dumps(jdata, ensure_ascii=False).replace("'", '"')

for example in examples:
    print(json_to_str(example["task"]))