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
				if(content['data']['project_type'] == "campaign"):
					title = content['data']['title']
					url = 'https://www.indiegogo.com'+content['data']['clickthrough_url']
					project_id = content['data']['project_id']
					category = content['data']['category']
					start_date = content['data']['open_date']
					close_date = content['data']['close_date']
					currency = content['data']['currency']
					amount_of_fund_raised = content['data']['funds_raised_amount']
					percentage_of_fund_raised = content['data']['funds_raised_percent']
					project_type = "funding"
				
					output.append({'title': title, 'url': url, 'project_id': project_id, 'category': category, 'start_date': start_date, 'close_date': close_date,'currency': currency,'amount_of_fund_raised': amount_of_fund_raised, 'percentage_of_fund_raised': percentage_of_fund_raised,  'project_type': project_type, })

		return output

	def close(self):
		return 0

if __name__ == "__main__":		
	try:
		inputFile = Path("input") / "Indiegogo_2018-12-14T10_41_01_757Z.json"
		print(str(inputFile))
		fileReader = JSONreader(inputFile)
		output = fileReader.readJSONInfo()
		print(output[0])

	except Exception as e: 
		traceback.print_exc()		