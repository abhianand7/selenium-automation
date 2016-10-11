import unittest
from WalMart import Session

base_url = 'http://grocery.walmart.com/'
signout_url = 'usd-estore/register/signoutcontainer.jsp'
signin_url = 'usd-estore/m/register/signin-only.jsp'
home_url = 'usd-estore/m/home.jsp'
product_url = 'http://grocery.walmart.com/usd-estore/m/product-detail.jsp?skuId='


class TestWalmartMethods(unittest.TestCase):

    def test_login(self):
        walmart = Session(base_url, signin_url, home_url, signout_url, product_url)        
        self.assertTrue(walmart.login('jeffreylunt@gmail.com', 'temp_dev'))
        walmart.save_cookies('unit_test')
        walmart.close()

    def test_zcookies(self):    # the tests are run in alphabetical order, that's why zcookies is the test name
        walmart = Session(base_url, signin_url, home_url, signout_url, product_url)
        walmart.load_prev_session('unit_test')
        self.assertTrue(walmart.user_status())
        walmart.close()

if __name__ == '__main__':
    unittest.main()
