import unittest
from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024,768))
display.start()


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_url(self):
        self.driver.get("https://grocery.walmart.com/usd-estore/m/register/signin-only.jsp")
        self.driver.find_element_by_id(
            'emailAddress').send_keys("jeffreylunt@gmail.com")
        self.driver.find_element_by_id("password").send_keys('temp_dev')
        self.driver.find_element_by_class_name("submit").click()

    def tearDown(self):
        self.driver.quit()


# class TestTwo(unittest.TestCase):
#
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.driver.set_window_size(1120, 550)
#
#     def test_url(self):
#         self.driver.get("https://grocery.walmart.com/usd-estore/m/register/signin-only.jsp")
#         self.driver.find_element_by_id(
#             'emailAddress').send_keys("jeffreylunt@gmail.com")
#         self.driver.find_element_by_id("password").send_keys('temp_dev')
#         self.driver.find_element_by_class_name("submit").click()
#
#     def tearDown(self):
#         self.driver.quit()

if __name__ == '__main__':
    unittest.main()
