# test script for WalMart.py module

from WalMart import Session, ItemProcess
import atexit
base_url = 'http://grocery.walmart.com/'
signout_url = 'usd-estore/register/signoutcontainer.jsp'
signin_url = 'usd-estore/m/register/signin-only.jsp'
home_url = 'usd-estore/m/home.jsp'
product_url = 'http://grocery.walmart.com/usd-estore/m/product-detail.jsp?skuId='
# initialize the session
walmart = Session(base_url, signin_url, home_url, signout_url, product_url)


# use this method when you are accessing the web page for the first time
# now while logging in, it will itself display, which user has logged in and
# also if login fails for any reason, the script will try three more times before quitting
# and it will also make sure the correct user has logged in
walmart.login('jeffreylunt@gmail.com', 'temp_dev')

# uncomment the below line and comment the above line if you are coming back to this website again
# now you can enter the particular session to resume
# walmart.load_prev_session()
# walmart.load_prev_session('cookies.pkl')

# below is the method to add items to cart
# you have to provide data in list of sku id
# [[skuid, quantity], [skuid, quantity]]
process_items = ItemProcess()

# by using below method you can fetch the contents of cart and verify
process_items.add_item_to_cart([[3000038027, 2], [1025774, 2]])

# you can fetch the items added to your cart and verify
process_items.list_cart_items()
#
# for searching any item
# walmart.search('banana')

# for saving the current state of the session
# this will save the cookie in the default file, thus overwriting the previous one
walmart.save_cookies()
# here you can save different state of the same website and resume any of the session
# walmart.save_cookies('your_session_name')

# get the name of the user currently logged in
print walmart.get_user_info()

# get the current web page url
print walmart.get_url()

# use the below method to take and save a screenshot of the current window
walmart.take_screenshot()

# uncomment the below line to print page source
# source = walmart.view_page_source()
# print source

# sign out of your current session
# walmart.sign_out()

# close the session and browser
walmart.close()


# use below code to save your cookies automatically
def exit_handler():
    walmart.save_cookies()
    return

#atexit.register(exit_handler())