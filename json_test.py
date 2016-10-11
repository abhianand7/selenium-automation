
from selenium import webdriver
import json
br = webdriver.PhantomJS()

br.get('https://grocery.walmart.com/v0.1/api/profile')

json_respn = br.find_element_by_xpath("//pre").text

json_data = json.loads(json_respn)
print json_data

print json_data['status']


br.get('http://grocery.walmart.com/usd-estore/m/register/signin-only.jsp')

