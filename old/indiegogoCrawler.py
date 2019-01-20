import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

class indiegogoCrawler():
	def __init__(self):

		#option = webdriver.ChromeOptions()
		option = Options()
		option.add_argument('--headless')

		self.driver = webdriver.Chrome(chrome_options=option)
		self.driver.set_window_size(1920, 800)
		self.initialURL = "https://www.indiegogo.com/explore/tech-innovation?project_type=all&project_timing=all&sort=trending"
		self.urls = []
		self.counter = 1;
		
	def extrateEachProductURL(self):
		self.allProductPage = self.driver.get(self.initialURL )
		self.allItems = self.driver.find_elements_by_class_name('discoverableCard')
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

			self.urls.append([item_hrefs,item_type])

	def readingPageInforamtion(self):
		for url in self.urls:
			href = url[0]
			item_type = url[1]
			
			
			#return

			if(item_type == 'funding'):
				#self.readItemPageInformationFundingType(href)
				self.storeWebToPDF(href)
			elif(item_type == 'marketplace'):
				#self.readItemPageInformationMarketingType(href)
				self.storeWebToPDF(href)

	def storeWebToPDF(self, href):
		self.driver.get(href)
		#self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		window_size = self.driver.get_window_size()
		window_height = window_size["height"]
		total_scroll_height = 0
		webPage_height = 1

		while (total_scroll_height <= webPage_height):
			webPage_height  = self.driver.execute_script("return document.body.scrollHeight")
			self.driver.execute_script("window.scrollBy(0, "+str(window_height)+");")
			total_scroll_height += window_height

			print(total_scroll_height)
			sleep(0.5)
		
		body_div = self.driver.find_element_by_xpath("//body")
		#body_div.screenshot("D:\Github\python\indiegogoCrawler"+str(self.counter)+".png")
		body_div.screenshot('images\\'+str(self.counter)+".png")
		self.counter = self.counter + 1
		print('counter: ',self.counter)


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
		
		except:
			print('fail to get information')
		finally:
			print()

	def readItemPageInformationFundingType(self, url):
		try:
			print (url)
			self.driver.get(url)
			item_detail_div = self.driver.find_element_by_class_name('campaignHeaderBasics')
			item_name_div = item_detail_div.find_element_by_class_name('campaignHeaderBasics-title')
			item_name = item_name_div.get_attribute("innerText")
			print('item name: '+item_name)
					
			item_owner_name_div = item_detail_div.find_element_by_class_name('campaignTrust-detailsName')
			item_owner_name = item_owner_name_div.get_attribute("innerText")
			print('owner: '+item_owner_name)

			item_rasied_amount_div = self.driver.find_element_by_class_name('campaignGoalProgress-raisedAmount')
			item_rasied_amount = item_rasied_amount_div.get_attribute("innerText")
			print('total raised amount: '+item_rasied_amount)

			item_rasied_percentage_div = self.driver.find_element_by_class_name('campaignGoalProgress-detailsGoal')
			item_rasied_percentage = item_rasied_percentage_div.get_attribute("innerText").split('%')[0]
			print('raised percentage: '+item_rasied_percentage+'%')

			item_rasied_oringal_amount = item_rasied_percentage_div.get_attribute("innerText").split('$')[1].split('\n')[0].strip()
			print('oringal amount: '+item_rasied_oringal_amount)

			item_goal_div = self.driver.find_element_by_class_name('campaignGoalProgress-detailsGoal-popover')
			item_goal = item_goal_div.get_attribute("innerText")
			print('goal: '+ item_goal)
				
		except:
			print('fail to get information')
		finally:
			print()
		
	def closeDriver(self):
		self.driver.quit()
		
		
try:
	crawler = indiegogoCrawler()    
	crawler.extrateEachProductURL()
	crawler.readingPageInforamtion()
finally:
	crawler.closeDriver()
