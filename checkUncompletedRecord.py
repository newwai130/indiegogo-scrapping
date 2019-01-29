import json
from pathlib import *
import traceback
from JSONwriter import *

def main():
	inputFile = Path("output") / "2018-12-14.json"
	outputFile = Path("output") / "notcompleted.json"
	fileWriter = JSONwriter(outputFile)

	try:
		print('start checking uncompleted record')
		with open(str(inputFile), newline='',encoding='UTF-8') as f:
			lines = f.readlines()
			for line in lines:
				content = json.loads(line)

				is_complete = True

				if('url' not in content):
					is_complete = False

				if('owner_name' not in content):
					is_complete = False

				if('owner_image_url' not in content):
					is_complete = False

				if('owner_image_name' not in content):
					is_complete = False

				if('funds_goal' not in content):
					is_complete = False

				if(is_complete == False):
					fileWriter.writeInfo(content)
		print('end checking uncompleted record')
	except Exception as e: 
		traceback.print_exc()
	finally:
		fileWriter.close()

if __name__ == "__main__":
	main()
