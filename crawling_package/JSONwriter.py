import json
from pathlib import *

import traceback

class JSONwriter():
	def __init__(self, outputFile):
		self.outputFile = outputFile
		self.outputFile.parent.mkdir(exist_ok=True)
		self.outputFile.touch(mode=0o777, exist_ok=True)
		self.f = self.outputFile.open(mode='a+', newline='',encoding='UTF-8')

	def writeInfo(self, info):
		data = json.dumps(info)
		self.f.write(data)
		self.f.write('\r\n')

	def close(self):
		self.f.close()
