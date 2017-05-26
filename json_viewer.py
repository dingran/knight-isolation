import json
from pprint import pprint

with open('isolation-result-26654.json') as data_file:
    data = json.load(data_file)


a=data['critiques']['680']['rubric_items']['5510']['observation']

print(a)
