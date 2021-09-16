from datetime import datetime
import pandas
from useful_methods.ProjectPaths import *
from SeleniumBrowser_proxy.SeleniumBrowser import load_browser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from retry import retry
import random

def login(driver):
	login_url = 'https://www.myfitnesspal.com/account/login'
	driver.get(login_url)
	driver.find_element_by_class_name('got_it_button').click()
	username = "" # write yours here
	search = driver.find_element_by_name('username')
	search.send_keys(username)
	password = "" # write yours here
	search = driver.find_element_by_name('password')
	search.send_keys(password)
	search.send_keys(Keys.RETURN)
	time.sleep(5)
	url = 'https://www.myfitnesspal.com/measurements/edit'
	driver.get(url)
	time.sleep(5)

def readData(filename="test_data.csv"):
	df = pandas.read_csv(make_data_path("test_data.csv"))
	columns = df.columns.to_list()
	columns = [column.split("(")[0].strip() for column in columns]
	df.columns = columns
	df["Date"] = pandas.to_datetime(df["Date"], format="%Y.%m.%d")
	use_cols = columns[1:]
	return df, use_cols

def load_measurement_column(driver,column="Weight"):
	select = Select(driver.find_element_by_id('type'))
	select.select_by_visible_text(column)
	driver.find_element_by_xpath("//form[@action='" + "/measurements/edit" + "']").submit()
	sleeptime = random.randint(5,15)
	time.sleep(sleeptime)

@retry(tries =-1, delay=30)
def input_entry(driver,date,amount):
	select = Select(driver.find_element_by_id('measurement_entry_date_1i'))
	select.select_by_value(str(date.year))
	select = Select(driver.find_element_by_id('measurement_entry_date_2i'))
	select.select_by_value(str(date.month))
	select = Select(driver.find_element_by_id('measurement_entry_date_3i'))
	select.select_by_value(str(date.day))
	search = driver.find_element_by_id('measurement_display_value')
	search.send_keys(str(amount))
	search.send_keys(Keys.RETURN)

def main(start_col=0,
		 start_date="2005.12.31" #yyyy.mm.dd
		 ):
	driver = load_browser(browser="firefox")
	login(driver)
	df, use_cols = readData()
	use_cols = use_cols[start_col:]
	first_col = True
	start_date = datetime.strptime(start_date, "%Y.%m.%d")
	for cur_column in use_cols:
		load_measurement_column(driver,column=cur_column)
		selected = df[["Date",cur_column]].dropna()
		selected[cur_column] = selected[cur_column].map(lambda x: str(x).strip('%'))
		if cur_column != use_cols[0]:
			first_col = False
		for row in selected.itertuples():
			date = row[1]
			amount=row[2]
			if first_col:
				if date >= start_date:
					input_entry(driver,date,amount)
					sleeptime = random.randint(10,25)
					time.sleep(sleeptime)
			else:
				input_entry(driver,date,amount)
				sleeptime = random.randint(10,25)
				time.sleep(sleeptime)
		sleeptime = random.randint(20,50)
		time.sleep(sleeptime)
		print("Done with {} entries".format(cur_column))
	print("DONE")

if __name__ == '__main__':
	main()