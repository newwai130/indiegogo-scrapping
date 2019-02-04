import json
from pathlib import *
import traceback

class JSONreader():
	def __init__(self, inputFile):
		self.inputFile = inputFile

	def readJSONInfo(self):
		output = []
		count = 0
		with open(str(self.inputFile), newline='',encoding='UTF-8') as f:
			lines = f.readlines()
			for line in lines:
				content = json.loads(line)
				data = {}
				if(('project_type' in content['data'] and content['data']['project_type'] == "campaign") or ('card_type' in content['data'] and content['data']['card_type'] == "project")):
					
					count += 1
					
					title = content['data']['title']
					data['title'] = title
					
					data['project_type'] = "funding"
					
					if('clickthrough_url' in content['data']):
						url = content['data']['clickthrough_url']
						url = 'https://www.indiegogo.com'+url
						data['url'] = url;
					elif ('url' in content['data']):
						url = content['data']['url']
						url = 'https://www.indiegogo.com'+url
						data['url'] = url;
					
					if('project_id' in content['data']):
						project_id = content['data']['project_id']
						data['project_id'] = project_id;
					elif ('id' in content['data']):
						project_id = content['data']['id']
						data['project_id'] = project_id;
					
					if('category' in content['data']):
						category = content['data']['category']
						data['category'] = category;
					elif('category_name' in content['data']):
						category = content['data']['category_name']
						data['category'] = category;
						
					if('open_date' in content['data']):
						start_date = content['data']['open_date']
						data['start_date'] = start_date;
					
					if('close_date' in content['data']):
						close_date = content['data']['close_date']
						data['close_date'] = close_date;
						
				 
					output.append(data)
		print("total valid output from source: ",count)
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