import requests
from pathlib import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import traceback

class PageContentExtractor():
	def __init__(self):

		option = Options()
		option.add_argument('--headless')
		option.add_argument('--log-level=3')

		self.driver = webdriver.Chrome(chrome_options=option)
		#self.driver.set_page_load_timeout(30)
		self.driver.set_window_size(1920, 800)
		self.imageOutputFolder = Path("image")
		self.imageOutputFolder.mkdir(parents=True, exist_ok=True)
		
	def readingPageInforamtion(self, href, type):
		if(type == 'funding'):
			print("transforming funding project")
			output = self.readItemPageInformationFundingType(href)
			return output
		elif(type == 'marketplace'):
			print("transforming marketplace project")
		else:
			print("no project type is found")

	def storeWebToImage(self, href, outputfileName):
		self.driver.get(href)
		window_size = self.driver.get_window_size()
		window_height = window_size["height"]
		total_scroll_height = 0
		webPage_height = 1

		while (total_scroll_height <= webPage_height):
			webPage_height  = self.driver.execute_script("return document.body.scrollHeight")
			self.driver.execute_script("window.scrollBy(0, "+str(window_height)+");")
			total_scroll_height += window_height

			#print(total_scroll_height)
			sleep(0.5)
		
		body_div = self.driver.find_element_by_xpath("//body")
		image_name = outputfileName + ".png"
		output_file = self.imageOutputFolder / image_name
		body_div.screenshot(str(output_file))

	"""
	def readItemPageInformationMarketingType(self, url):
		try:
			print (url)
			self.driver.get(url)
			item_detail_div = self.driver.find_element_by_class_name('productPage-info')
			item_name_div = item_detail_div.find_element_by_class_name('product-title')
			item_name = item_name_div.get_attribute("innerText")
			print('item name: '+item_name)

			item_owner_name_div = item_detail_div.find_element_by_class_name('campaignTrust-detailsName')
			item_owner_name = item_owner_name_div.get_attribute("innerText")
			print('owner: '+item_owner_name)

			item_price_div = item_detail_div.find_element_by_class_name('campaignNextPerk-amount')
			item_price = item_price_div.get_attribute("innerText")
			print('price: '+item_price)
		
		except Exception as e: 
			print(e)
		finally:
			print()
	"""

	def readItemPageInformationFundingType(self, url):
		print("start reading webpage")
		info = {}

		#re-try 3 times if the web request have no reponse
		try:
			print (url)
			try_times = 0;
			while(True):
				try:
					self.driver.get(url)
					item_detail_div = self.driver.find_element_by_class_name('campaignHeaderBasics')
					item_name_div = item_detail_div.find_element_by_class_name('campaignHeaderBasics-title')
					item_name = item_name_div.get_attribute("innerText")
					break
				except Exception: 
					print("retry")
					continue
				finally:
					try_times += 1
					if(try_times>1):
						break
					else:
						sleep(3)
			
			try:
				item_detail_div = self.driver.find_element_by_class_name('campaignHeaderBasics')
				item_name_div = item_detail_div.find_element_by_class_name('campaignHeaderBasics-title')
				item_name = item_name_div.get_attribute("innerText")
				info['title'] = item_name
				print('1.item name: '+item_name)
			except Exception: 
				print("retry")

			try:		
				item_owner_name_div = item_detail_div.find_element_by_class_name('campaignTrust-detailsName')
				item_owner_name = item_owner_name_div.get_attribute("innerText")
				info['owner'] = item_owner_name
				print('2.owner: '+item_owner_name)
			except Exception: 
				pass

			try:
				item_rasied_amount_div = self.driver.find_element_by_class_name('indemandProgress-raisedAmount')
				item_rasied_amount = item_rasied_amount_div.get_attribute("innerText")
				info['raisedAmount'] = item_rasied_amount
				print('3.total raised amount: '+item_rasied_amount)
			except Exception: 
				pass

			try:
				item_rasied_amount_div = self.driver.find_element_by_class_name('campaignGoalProgress-raisedAmount')
				item_rasied_amount = item_rasied_amount_div.get_attribute("innerText")
				info['raisedAmount'] = item_rasied_amount
				print('3.total raised amount: '+item_rasied_amount)
			except Exception: 
				pass

			try:
				item_rasied_percentage_div = self.driver.find_element_by_class_name('indemandProgress-historyDetails')
				item_rasied_percentage = item_rasied_percentage_div.get_attribute("innerText").split('%')[0]
				info['raisedAmountPercentage'] = item_rasied_percentage
				print('4.raised percentage: '+item_rasied_percentage+'%')
			except Exception: 
				pass

			try:
				item_rasied_percentage_div = self.driver.find_element_by_class_name('campaignGoalProgress-detailsGoal')
				item_rasied_percentage = item_rasied_percentage_div.get_attribute("innerText").split('%')[0]
				info['raisedAmountPercentage'] = item_rasied_percentage
				print('4.raised percentage: '+item_rasied_percentage+'%')
			except Exception: 
				pass

			
			#item_rasied_oringal_amount = item_rasied_percentage_div.get_attribute("innerText").split('$')[1].split('\n')[0].strip()
			#print('oringal amount: '+item_rasied_oringal_amount)

			#item_goal_div = self.driver.find_element_by_class_name('campaignGoalProgress-detailsGoal-popover')
			#item_goal = item_goal_div.get_attribute("innerText")
			#print('goal: '+ item_goal)
				
		except Exception as e: 
			print(e)
		finally:
			print("end reading webpage")
			return info
		
	def closeDriver(self):
		self.driver.quit()
		
if __name__ == "__main__":		
	try:
		href = 'https://www.indiegogo.com/projects/funcl-wireless-headphones-affordable-awesomeness#/'
		type = "funding"
		outputfileName = "testing"

		crawler = PageContentExtractor()    
		crawler.readingPageInforamtion(href, type)
		crawler.storeWebToImage(href, outputfileName)
		crawler.closeDriver()

	except Exception as e: 
		print(e)
	finally:
		crawler.closeDriver()
