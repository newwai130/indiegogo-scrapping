from JSONwriter import *
from JSONreader import *
from PageContentExtractor import *
from pathlib import *
import traceback

try:
	inputFile = Path("input") / "Indiegogo_2018-12-14T10_41_01_757Z.json"
	outputFile = Path("output") / "2018-12-14.json"

	fileReader = JSONreader(inputFile)
	inputPageInfo = fileReader.readJSONInfo()
	fileWriter = JSONwriter(outputFile)

	crawler = PageContentExtractor()
	for inputPage in inputPageInfo:
		info = crawler.readingPageInforamtion(inputPage['href'], inputPage['type'])
		print("info: ",info)
		crawler.storeWebToImage(inputPage['href'], inputPage['title'])
		fileWriter.writeInfo(info)

except Exception as e: 
		traceback.print_exc()
finally:
	crawler.closeDriver()
	fileWriter.close()