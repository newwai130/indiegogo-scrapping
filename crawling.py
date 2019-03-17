from crawling_package.JSONwriter import *
from crawling_package.JSONreader import *
from crawling_package.PageContentExtractor import *
from pathlib import *
import traceback
import configparser

def main():

	config = configparser.ConfigParser()
	config.read('Config.ini')

	input_folder_path 	= Path(config.get('DEFAULT', 'Input_Folder_Directory'))
	output_folder_path 	= Path(config.get('DEFAULT', 'Output_Folder_Directory'))
	image_folder_path 	= Path(config.get('DEFAULT', 'Image_Output_Directory'))

	inputFile	= input_folder_path / Path(config.get('DEFAULT', 'Input_File_Name'))
	outputFile 	= output_folder_path / Path(config.get('DEFAULT', 'Output_File_Name'))

	print("json input file: ", str(inputFile))
	print("json output file: ", str(outputFile))
	print("image output folder: ", str(image_folder_path))

	fileReader = JSONreader(inputFile)
	fileWriter = JSONwriter(outputFile)

	crawler = PageContentExtractor(image_folder_path)

	inputSourceInfo = fileReader.readJSONInfo()

	try:
		
		for inputSourc in inputSourceInfo:
			try:
				info = {}
				
				crawlerOutput = crawler.readingPageInforamtion(inputSourc['url'], inputSourc['project_type'], inputSourc['project_id'])

				web_image_name = crawler.storeWebToImage(inputSourc['url'], str(inputSourc['project_id']))
				info['web_image_name'] = web_image_name

				info.update(inputSourc)
				info.update(crawlerOutput)
				
				fileWriter.writeInfo(info)
				print("----------------------------------------")
			except Exception as e: 
				traceback.print_exc()

	except Exception as e: 
			traceback.print_exc()
	finally:
		crawler.closeDriver()
		fileReader.close()
		fileWriter.close()

if __name__ == "__main__":
	main()