import json
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import simplex as sim
from prettytable import PrettyTable

with open('examples.json', 'r') as f:
    examples = json.load(f)

def json_to_str(jdata):
    return json.dumps(jdata, ensure_ascii=False).replace("'", '"')

def to_red(text):
    return "\033[31m {}" .format(text)

def to_green(text):
    return "\033[32m {}" .format(text)

def make_color_boolean(boolean_data):
    if (boolean_data):
        return to_green('true')
    else:
        return to_red('false')

task_number = 0
th = ["task number","correct answer", "our answer", "equal"]
table = PrettyTable(th)

for example in examples:
    result = sim.simplex(*sim.parse_problem(json_to_str(example["task"])))
    correct_answer = example["correct_answer"]
    equal = make_color_boolean(result == correct_answer)
    table.add_row([task_number, correct_answer, result, equal])
    task_number+=1

print(table)