import json
from pathlib import *
import traceback

class JSONreader():
	def __init__(self, inputFile):
		self.inputFile = inputFile

	def readJSONInfo(self):
		output = []
		with open(str(self.inputFile), newline='',encoding='UTF-8') as f:
			lines = f.readlines()
			for line in lines:
				content = json.loads(line)
				href = 'https://www.indiegogo.com'+content['data']['clickthrough_url']
				if(content['data']['project_type'] == "campaign"):
					type = "funding"
				elif(content['data']['project_type'] == "product"):
					type = "marketplace"
				title = content['data']['title']
				output.append({'title': title, 'href': href, 'type': type})

		return output

	def close(self):
		return

if __name__ == "__main__":		
	try:
		inputFile = Path("input") / "Indiegogo_2018-12-14T10_41_01_757Z.json"
		print(str(inputFile))
		fileReader = JSONreader(inputFile)
		output = fileReader.readJSONInfo()
		print(output)

	except Exception as e: 
		traceback.print_exc()		