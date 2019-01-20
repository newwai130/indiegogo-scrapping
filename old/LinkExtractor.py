import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

class LinkExtractor():
	def __init__(self):

		option = Options()
		option.add_argument('--headless')

		self.driver = webdriver.Chrome(chrome_options=option)
		self.driver.set_window_size(1920, 800)
		self.urls = []
		self.counter = 1;
		
	def extrateEachProductURL(self, initialURL):
		
		self.allProductPage = self.driver.get(initialURL)
		self.allItems = self.driver.find_elements_by_class_name('discoverableCard')

		"""
		for item in self.allItems:
			
			item_hrefs = item.find_element_by_xpath('.//a').get_attribute('href')

			if(len(item.find_elements_by_class_name('discoverableCard-type--crowdfunding')) > 0):
				item_type = 'funding'
			elif(len(item.find_elements_by_class_name('discoverableCard-type--marketplace')) > 0):
				item_type = 'marketplace'
			elif(len(item.find_elements_by_class_name('discoverableCard-type--offering')) > 0):
				item_type = 'investing'
			else:
				item_type = 'undefined'
		"""

		window_size = self.driver.get_window_size()
		window_height = window_size["height"]
		total_scroll_height = 0
		webPage_height = 1
		while True:
			"""
			#score website from top to bottom
			while (total_scroll_height <= webPage_height):
				webPage_height  = self.driver.execute_script("return document.body.scrollHeight")
				self.driver.execute_script("window.scrollBy(0, "+str(window_height)+");")
				total_scroll_height += window_height

				print(total_scroll_height)
				sleep(0.2)
			"""

			#iterate to the buttom of the the page
			try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".i-cta-1.ng-binding.ng-isolate-scope")))
				more_button = self.driver.find_element_by_css_selector('.i-cta-1.ng-binding.ng-isolate-scope')
				more_button.click()
				print('=>',len(self.allItems))
				sleep(1)
				self.allItems = self.driver.find_elements_by_class_name('discoverableCard')
				
			except Exception as e: 
				print(e)
				break

		#extracte the link
		for item in self.allItems:
			item_hrefs = item.find_element_by_xpath('.//a').get_attribute('href')
			print(self.allItems.index(item),': ',item_hrefs)
	
	def setInitialURL(self, initialURL):
		self.initialURL = initialURL

	def closeDriver(self):
		self.driver.quit()
		
	def storeToQueue(self):
		return 


try:
	initialURL = "https://www.indiegogo.com/explore/audio?project_type=all&project_timing=all&sort=trending"
	crawler = LinkExtractor()    
	crawler.extrateEachProductURL(initialURL)
	crawler.closeDriver()

finally:
	crawler.closeDriver()
