from JSONwriter import *
from JSONreader import *
from PageContentExtractor import *
from pathlib import *
import traceback

inputFile = Path("input") / "Indiegogo_2018-12-14T10_41_01_757Z.json"
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

			web_image_name = crawler.storeWebToImage(inputSourc['url'], str(inputSourc['project_id']))
			info['web_image_name'] = web_image_name

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