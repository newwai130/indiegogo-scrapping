import json
from pathlib import *

import traceback

class JSONwriter():
	def __init__(self, outputFile):
		self.outputFile = outputFile
		self.outputFile.touch(mode=0o777, exist_ok=True)
		self.f = open(str(self.outputFile), 'a+', newline='',encoding='UTF-8')

	def writeInfo(self, info):
		data = json.dumps(info)
		self.f.write(data)
		self.f.write('\r\n')

	def close(self):
		self.close()

if __name__ == "__main__":
	try:	
		info = {"123":{'a':'1','b':'2'},"456":{'a':'1','b':'2'}}
		outputFile = Path("output") / "2018-12-14.json"
		print(str(outputFile))
		fileWriter = JSONwriter(outputFile)
		fileWriter.writeInfo(info)
	except Exception as e: 
		traceback.print_exc()