import requests
from pathlib import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import traceback

class PageContentExtractor():
	def __init__(self):

		option = Options()
		#option.add_argument('--headless')
		#option.add_argument('--log-level=3')

		self.driver = webdriver.Chrome(options=option)
		self.driver.set_window_size(1920, 800)
		self.imageOutputFolder = Path("image")
		self.imageOutputFolder.mkdir(parents=True, exist_ok=True)
		
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

		
		while (total_scroll_height <= webPage_height):
			webPage_height  = self.driver.execute_script("return document.body.scrollHeight")
			self.driver.execute_script("window.scrollBy(0, "+str(window_height)+");")
			total_scroll_height += window_height

			#print(total_scroll_height)
			sleep(0.5)
			
			
		advertisement_buttons = self.driver.find_elements_by_xpath("/svg[@class='ng-isolate-scope']")
		if(advertisement_buttons and len(advertisement_buttons) > 0 and advertisement_buttons[0].is_displayed()):
			advertisement_buttons[0].click()

		click_more_buttons = self.driver.find_elements_by_class_name('readMore')
		if(click_more_buttons and len(click_more_buttons) > 0 and click_more_buttons[0].is_displayed()):
			click_more_buttons[0].click()
		
		body_div = self.driver.find_element_by_xpath("//body")
		image_name = outputfileName + "_web.png"
		output_file = self.imageOutputFolder / image_name
		#body_div.screenshot(str(output_file))
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
		info = {}
		item_owner_name = ""
		item_owner_image_url = ""

		#re-try 3 times if the web request have no reponse
		try:
			
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
			
			info['url'] = url

			#get product title
			try:
				item_detail_div = self.driver.find_element_by_class_name('campaignHeaderBasics')
				item_name_div = item_detail_div.find_element_by_class_name('campaignHeaderBasics-title')
				item_name = item_name_div.get_attribute("innerText")
				#info['title'] = item_name
				print('1.item name: '+item_name)
			except Exception: 
				pass

			#get name of th creater/owner
			try:		
				item_owner_name_div = item_detail_div.find_element_by_class_name('campaignTrust-detailsName')
				item_owner_name = item_owner_name_div.get_attribute("innerText")
				#info['owner_name'] = item_owner_name
				print('2. owner name: '+item_owner_name)
			except Exception: 
				pass

			#get image url of the creater/owner
			try:		
				item_owner_image_url_div = item_detail_div.find_element_by_class_name('campaignTrust-avatar')
				item_owner_image_url = item_owner_image_url_div.get_attribute("src")
				#info['owner_image_url'] = item_owner_image_url
				print('3.owner image url: '+item_owner_image_url)
			except Exception: 
				pass

			#download the image of the owner
			try:
				if(item_owner_name != "" and item_owner_image_url != ""):
					owner_image_name = str(project_id) + "_" + item_owner_name
					self.storeOwnerImage(item_owner_image_url, owner_image_name)
					info['owner_image_name'] = owner_image_name
			except Exception: 
				pass

			#get the amount of total raised fund(1)
			try:
				item_rasied_amount_div = self.driver.find_element_by_class_name('indemandProgress-raisedAmount')
				item_rasied_amount = item_rasied_amount_div.get_attribute("innerText")
				info['raisedAmount'] = item_rasied_amount
				print('4.total raised amount: '+item_rasied_amount)
			except Exception: 
				pass

			#get the amount of total raised fund(2)
			try:
				item_rasied_amount_div = self.driver.find_element_by_class_name('campaignGoalProgress-raisedAmount')
				item_rasied_amount = item_rasied_amount_div.get_attribute("innerText")
				info['raisedAmount'] = item_rasied_amount
				print('4.total raised amount: '+item_rasied_amount)
			except Exception: 
				pass

			#get the percentage of total raised fund(1)	
			try:
				item_rasied_percentage_div = self.driver.find_element_by_class_name('indemandProgress-historyDetails')
				item_rasied_percentage = item_rasied_percentage_div.get_attribute("innerText").split('%')[0]
				info['raisedAmountPercentage'] = item_rasied_percentage
				print('5.raised percentage: '+item_rasied_percentage+'%')
			except Exception: 
				pass
			
			#get the percentage of total raised fund(2)	
			try:
				item_rasied_percentage_div = self.driver.find_element_by_class_name('campaignGoalProgress-detailsGoal')
				item_rasied_percentage = item_rasied_percentage_div.get_attribute("innerText").split('%')[0]
				info['raisedAmountPercentage'] = item_rasied_percentage
				print('5.raised percentage: '+item_rasied_percentage+'%')
			except Exception: 
				pass
			

			#get target goal of the fund
			try:
				item_goal_div = self.driver.find_element_by_class_name('campaignGoalProgress-detailsGoal')
				temp_item_goal_div_text = item_goal_div.get_attribute("innerText").encode('UTF-8').replace(b'\xc2\xa0', b' ').decode('UTF-8')
				#print(item_goal_div.get_attribute("innerText").encode('UTF-8'))
				#print(item_goal_div.get_attribute("innerText").encode('UTF-8').replace(b'\xc2\xa0', b' '))
				#rint(item_goal_div.get_attribute("innerText").encode('UTF-8').replace(b'\xc2\xa0', b' ').decode('UTF-8'))
				item_goal = temp_item_goal_div_text.split(" ")[2]
				info['funds_goal'] = item_goal
				print('6.fund goal: '+item_goal)
			except Exception:
				pass
			
				
		except Exception as e: 
			traceback.print_exc()
		finally:
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
		crawler.readingPageInforamtion(href, type, 123)
		#crawler.storeWebToImage(href, outputfileName)

	except Exception as e: 
		traceback.print_exc()
	finally:
		crawler.closeDriver()
