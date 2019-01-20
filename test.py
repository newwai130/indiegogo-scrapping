import json
from pathlib import *
import traceback

inputFile = Path("output") / "2018-12-14.json"
with open(str(inputFile), newline='',encoding='UTF-8') as f:
	lines = f.readlines()
	for line in lines:
		content = json.loads(line)
		print(str(content))

