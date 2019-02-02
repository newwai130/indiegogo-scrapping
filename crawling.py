from JSONwriter import *
from JSONreader import *
from PageContentExtractor import *
from pathlib import *
import traceback
import configparser

config = configparser.ConfigParser()
config.read('Config.ini')
input_folder_path = Path(config.get('DEFAULT', 'Input_Folder_Directory'))
output_folder_path = Path(config.get('DEFAULT', 'Output_Folder_Directory'))
image_folder_path = Path(config.get('DEFAULT', 'Image_Output_Directory'))

"""
print(str(input_folder_path))
print(str(output_folder_path))
print(str(image_folder_path))

input()
"""

inputFile = Path("input") / "source.json"
outputFile = Path("output") / "2018-12-14.json"

fileReader = JSONreader(inputFile)
inputSourceInfo = fileReader.readJSONInfo()
fileWriter = JSONwriter(outputFile)

crawler = PageContentExtractor()

try:
	
	for inputSourc in inputSourceInfo:
		try:
			info = {}
			
			crawlerOutput = crawler.readingPageInforamtion(inputSourc['url'], inputSourc['project_type'], inputSourc['project_id'])

			#web_image_name = crawler.storeWebToImage(inputSourc['url'], str(inputSourc['project_id']))
			#info['web_image_name'] = web_image_name

			info.update(inputSourc)
			info.update(crawlerOutput)
			
			#fileWriter.writeInfo(info)
			print("----------------------------------------")
		except Exception as e: 
			traceback.print_exc()

except Exception as e: 
		traceback.print_exc()
finally:
	crawler.closeDriver()
	fileReader.close()
	fileWriter.close()