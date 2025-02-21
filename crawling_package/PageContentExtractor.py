import requests
from pathlib import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import traceback

class PageContentExtractor():
	def __init__(self, imageFolderPath):

		option = Options()
		option.add_argument('--headless')
		option.add_argument('--log-level=3')
		option.add_argument('--incognito')

		self.driver = webdriver.Chrome(options=option)
		self.driver.set_window_size(1920, 800)
		self.imageOutputFolder = imageFolderPath
		self.imageOutputFolder.mkdir(parents=True, exist_ok=True)
		self.countTotalWebsite = 0
		self.countTotalFailWebsite = 0
		
	def readingPageInforamtion(self, href, type, project_id):
		if(type == 'funding'):
			#print("transforming funding project")
			output = self.readItemPageInformationFundingType(href, project_id)
			return output
		elif(type == 'marketplace'):
			#print("transforming marketplace project")
			return {}
		else:
			#print("no project type is found")
			return {}

	def storeWebToImage(self, url, outputfileName):
		print("start to store web image")
		self.driver.get(url)
		window_size = self.driver.get_window_size()
		window_height = window_size["height"]
		total_scroll_height = 0
		webPage_height = 1

		
		#scroll website from top to bottom
		while (total_scroll_height <= webPage_height):
			webPage_height  = self.driver.execute_script("return document.body.scrollHeight")
			self.driver.execute_script("window.scrollBy(0, "+str(window_height)+");")
			total_scroll_height += window_height
			sleep(0.5)
			
			
		advertisement_buttons = self.driver.find_elements_by_xpath("/svg[@class='ng-isolate-scope']")
		if(advertisement_buttons and len(advertisement_buttons) > 0 and advertisement_buttons[0].is_displayed()):
			advertisement_buttons[0].click()

		click_more_buttons = self.driver.find_elements_by_class_name('readMore')
		if(click_more_buttons and len(click_more_buttons) > 0 and click_more_buttons[0].is_displayed()):
			click_more_buttons[0].click()
		
		#save the web image
		body_div = self.driver.find_element_by_xpath("//body")
		image_name = outputfileName + "_web.png"
		output_file = self.imageOutputFolder / image_name
		element_png = body_div.screenshot_as_png
		with open(str(output_file), 'wb+') as f:
			f.write(element_png)

		return image_name

	def storeOwnerImage(self, href, outputfileName):
		response = requests.get(href)
		image_name = outputfileName
		output_file = self.imageOutputFolder / image_name
		if response.status_code == 200:
			with open(str(output_file), 'wb') as f:
				f.write(response.content)

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

	def readItemPageInformationFundingType(self, url, project_id):
		print("start browsing ")
		print("project id: ", project_id)
		print("url: ", url)
		self.countTotalWebsite += 1
		info = {}
		item_owner_name = ""
		item_owner_image_url = ""

		#re-try 3 times if the web request have no reponse
		try:
			
			try_times = 0;
			while(True):
				self.driver.get(url)
				if (len(self.driver.find_elements_by_class_name("i-error-container")) > 0 and try_times <= 5 ):
					print("retry to load the web page, wait for ", 2*try_times, " seconds")
					sleep(2*try_times)
					try_times += 1
					continue
				else:
					break
						
			print("start to get field")
			
			info['url'] = url
			
			isGetAllInformation = True

			#get product title
			try:
				item_name = self.driver.find_element_by_xpath("//meta[@name='sailthru.title']").get_attribute("content")
				#item_detail_div = self.driver.find_element_by_class_name('campaignHeaderBasics')
				#item_name_div = item_detail_div.find_element_by_class_name('campaignHeaderBasics-title')
				#item_name = item_name_div.get_attribute("innerText")
				info['title'] = item_name
				print('1.item name: '+item_name)
			except Exception:
				isGetAllInformation = False 
				pass

			#get product type
			try:
				item_type = self.driver.find_element_by_xpath("//meta[@name='sailthru.displayed_category']").get_attribute("content")
				info['type'] = item_type
				print('2.item type: '+item_type)
			except Exception:
				isGetAllInformation = False 
				pass

			#get creattion date
			try:
				item_creattion_date = self.driver.find_element_by_xpath("//meta[@name='sailthru.date']").get_attribute("content")
				info['project_create_date'] = item_creattion_date
				print('3.project_start_date: '+item_creattion_date)
			except Exception:
				isGetAllInformation = False 
				pass

			#get ends date
			try:
				item_expire_date = self.driver.find_element_by_xpath("//meta[@name='sailthru.expire_date']").get_attribute("content")
				info['project_expire_date'] = item_expire_date
				print('4.project_end_date: '+item_expire_date)
			except Exception:
				isGetAllInformation = False 
				pass

			#get name of th creater/owner
			try:
				item_owner_name = self.driver.find_element_by_xpath("//meta[@name='sailthru.author']").get_attribute("content")
				#item_detail_div = self.driver.find_element_by_class_name('campaignHeaderBasics')		
				#item_owner_name_div = item_detail_div.find_element_by_class_name('campaignTrust-detailsName')
				#item_owner_name = item_owner_name_div.get_attribute("innerText")
				info['owner_name'] = item_owner_name
				print('5 owner name: '+item_owner_name)
			except Exception:
				isGetAllInformation = False  
				pass

			#get location of th creater/owner
			try:
				item_owner_location_div = self.driver.find_element_by_class_name('basicsCampaignOwner-details-city')
				item_owner_location = item_owner_location_div.get_attribute("innerText")
				info['owner_location'] = item_owner_location
				print('6 owner location: '+ item_owner_location)
			except Exception as e:
				isGetAllInformation = False 
				print(traceback.format_exc())
				pass
			
			#get image url of the creater/owner
			try:
				item_owner_image_url_div = self.driver.find_element_by_class_name('campaignTrust-avatar').find_element_by_tag_name('img')
				item_owner_image_url = item_owner_image_url_div.get_attribute("src")
				info['owner_image_url'] = item_owner_image_url
				print('7 owner image url: '+str(item_owner_image_url))
			except Exception as e:
				isGetAllInformation = False 
				print(traceback.format_exc())
				pass

			#download the image of the owner
			try:
				if(item_owner_name != "" and item_owner_image_url != ""):
					owner_image_name = str(project_id) + "_" + item_owner_name
					self.storeOwnerImage(item_owner_image_url, owner_image_name)
					info['owner_image_name'] = owner_image_name
					print('8 owner_image_name: '+ owner_image_name)
			except Exception:
				isGetAllInformation = False 
				pass	

		
			#get the amount of total raised fund(1)
			try:
				item_rasied_amount_div = self.driver.find_element_by_class_name('basicsGoalProgress-amountSold')
				item_rasied_amount = item_rasied_amount_div.get_attribute("innerText")

				item_rasied_amount_currency_div = self.driver.find_element_by_class_name('basicsGoalProgress-raisedCurrency')
				item_rasied_amount_currency = item_rasied_amount_currency_div.get_attribute("innerText")

				info['raisedAmount'] = item_rasied_amount
				info['currency'] = item_rasied_amount_currency
				print('9.total raised amount: '+item_rasied_amount+" "+item_rasied_amount_currency)
			except Exception:
				pass


			"""
			#get the amount of total raised fund(2)
			try:
				item_rasied_amount_div = self.driver.find_element_by_class_name('campaignGoalProgress-raisedAmount')
				item_rasied_amount = item_rasied_amount_div.get_attribute("innerText")
				info['raisedAmount'] = item_rasied_amount
				print('9.total raised amount: '+item_rasied_amount)
			except Exception:
				pass
			"""


			#get the percentage of total raised fund	
			try:
				item_rasied_percentage = self.driver.find_element_by_xpath("//meta[@name='sailthru.displayed_pct_funded']").get_attribute("content")
				info['raisedAmountPercentage'] = item_rasied_percentage
				print('10.raised percentage: '+item_rasied_percentage)
			except Exception:
				pass

			
			#get target goal of the fund
			try:
				item_goal_div = self.driver.find_element_by_class_name('basicsGoalProgress-progressDetails-detailsGoal')
				temp_item_goal_div_text = item_goal_div.get_attribute("innerText").encode('UTF-8').replace(b'\xc2\xa0', b' ').decode('UTF-8')
				item_goal = temp_item_goal_div_text.split(" ")[2]
				info['funds_goal'] = item_goal
				print('11.fund goal: '+item_goal)
			except Exception:
				isGetAllInformation = False
				pass


			if(not isGetAllInformation):
				self.countTotalFailWebsite += 1	

		except Exception:
			self.countTotalFailWebsite += 1 
			traceback.print_exc()
		finally:
			print("success rate: ", self.countTotalWebsite - self.countTotalFailWebsite, "/", self.countTotalWebsite)
			return info
		
	def closeDriver(self):
		self.driver.quit()
		
if __name__ == "__main__":		
	try:
		#href = 'https://www.indiegogo.com/projects/pollyanna-publishing#/' 
		#href = 'https://www.indiegogo.com/projects/the-eyal-vilner-big-band-new-swing-album#/'
		href = 'https://www.indiegogo.com/projects/re-visions-creating-mosaics-and-economic-opportunity'
		type = "funding"
		outputfileName = "testing.png"

		crawler = PageContentExtractor()    
		output = crawler.readingPageInforamtion(href, type, 123)
		print(output)
		#crawler.storeWebToImage(href, outputfileName)

	except Exception: 
		traceback.print_exc()
	finally:
		crawler.closeDriver()
