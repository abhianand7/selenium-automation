import unittest
from WalMart import Session

base_url = 'http://grocery.walmart.com/'
signout_url = 'usd-estore/register/signoutcontainer.jsp'
signin_url = 'usd-estore/m/register/signin-only.jsp'
home_url = 'usd-estore/m/home.jsp'
product_url = 'http://grocery.walmart.com/usd-estore/m/product-detail.jsp?skuId='

skus = {'banana':3000014678}

class WalmartMethods(unittest.TestCase):

    def login(self):
        walmart = Session(base_url, signin_url, home_url, signout_url, product_url)        
        self.assertTrue(walmart.login('xxxx@gmail.com', 'xxxxx'))
        walmart.save_cookies('unit_test')
        walmart.close()

    def zcookies(self):    # the tests are run in alphabetical order, that's why zcookies is the test name
        walmart = Session(base_url, signin_url, home_url, signout_url, product_url)
        walmart.load_prev_session('unit_test')
        self.assertTrue(walmart.user_status())
        walmart.close()

    def single_add_to_cart(self):
        walmart = Session(base_url, signin_url, home_url, signout_url, product_url)
        walmart.login('xxxxx@gmail.com', 'xxxx')
        quantity = walmart.quantity_in_cart(skus['banana'])
        walmart.add_item_to_cart([[skus['banana'], 1]])
        self.assertEqual(quantity+1, walmart.quantity_in_cart(skus['banana']))
        walmart.close()

    def multiple_add_to_cart(self):
        walmart = Session(base_url, signin_url, home_url, signout_url, product_url)
        walmart.login('xxxxx@xxxx.com', 'xxxx')
        quantity = walmart.quantity_in_cart(skus['banana'])
        walmart.add_item_to_cart([[skus['banana'], 2]])
        self.assertEqual(quantity+2, walmart.quantity_in_cart(skus['banana']))
        walmart.close()

if __name__ == '__main__':
    unittest.main()
