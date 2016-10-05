import os
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import sys
import time
import json
from lxml import html
# for saving cookies
import pickle
# for creating a virtual display
from pyvirtualdisplay import Display

# base_url = 'http://grocery.walmart.com/'
# signout_url = 'usd-estore/register/signoutcontainer.jsp'
# signin_url = 'usd-estore/m/register/signin-only.jsp'
# home_url = 'usd-estore/m/home.jsp'
display = Display(visible=0, size=(1024, 768))
display.start()

# flags used in this script
# this flag indicates whether the current session is a logged in session
session_active_flag = False
# if not logged in session, whether it is a cookie loaded session
cookies_loaded_flag = False

# some global variables used
login_attempt = 0


# base class setup for other objects to inherit
class WalMart:
    def __init__(self, base_url, signin_url, home_url, signout_url, product_url):
        self.base_url = base_url
        self.signin_url = signin_url
        self.signout_url = signout_url
        self.home_url = home_url
        self.product_url = product_url
        try:
            self.browser = webdriver.Firefox()
            # uncomment one of the following lines to test with a specific browser
            # in order to test with that particular browser you have it installed on your system
            # otherwise leave it as unchanged
            # uncomment the below line for PhantomJS a headless javascript enabled browser
            # self.browser = webdriver.PhantomJS()
            # uncomment the below line for Chrome Browser
            # self.browser = webdriver.Chrome()
            # uncomment the below line for Edge Browser
            # self.browser = webdriver.Edge()
            # uncomment the below line for Opera Browser
            # self.browser = webdriver.Opera()
            # uncomment the below line for Safari Browser
            # self.browser = webdriver.Safari()
            # uncomment the below line for Internet Explorer
            # self.browser = webdriver.Ie()
            self.browser.maximize_window()
            # self.browser.implicitly_wait(30)
        except selenium.common.exceptions.WebDriverException as e:
            print e
            print "browser error\ncheck if your browser is up-to-date"

    def setup(self):
        # future setups to come here
        pass


# this class has all the required methods

class Session(WalMart):
    # method login
    # call this method to login to the webpage with your credentials
    def login(self, username, password):
        global login_attempt, session_active_flag
        self.browser.get(self.base_url + self.signin_url)
        # wait for the element to be present
        try:
            element_present = EC.presence_of_element_located((By.ID, 'emailAddress'))
            WebDriverWait(self.browser, 10).until(element_present)
        except TimeoutException:
            print "Timed out waiting for page to load"
            self.close(1)
        else:
            # clear the username field of the signin page, if filled from before
            self.browser.find_element_by_id('emailAddress').clear()
            # clear any previous values prensent in password field
            self.browser.find_element_by_id('password').clear()
            # get the email input object
            email = self.browser.find_element_by_id('emailAddress')
            # get the password input object
            pwd = self.browser.find_element_by_id('password')
            # set the proper username
            email.send_keys(username)
            # set the proper password
            pwd.send_keys(password)
            # click to login
            self.browser.find_element_by_class_name('submit').click()
            user_name = self.get_name()
            # make sure that login is successful
            if user_name.lower() != 'guest':
                print 'logged in as %s' % user_name
                start = time.time()
                while time.time() - start < 5:
                    pass
                # save the cookies of this session
                pickle.dump(self.browser.get_cookies(), open("cookies.pkl", "wb"))
                session_active_flag = True
                return session_active_flag
            else:
                session_active_flag = False
                print "login failed\n retrying"
                if login_attempt == 3:
                    print 'exiting login failed\nplease try again\nverify your login credentials'
                    self.close()
                    return session_active_flag
                else:
                    self.login(username, password)
                    login_attempt += 1

    def search(self, query):
        try:
            element_present = EC.presence_of_element_located((By.ID, 'searchInput'))
            WebDriverWait(self.browser, 10).until(element_present)
        except TimeoutException:
            print "Timed out waiting for page to load\nPlease check your Internet Connection"
            self.close(1)
        except selenium.common.exceptions.ElementNotVisibleException as e:
            # handle this exception in case of error
            print e
        except selenium.common.exceptions.NoSuchElementException as e:
            # handle this exception when page loading fails
            print e
        else:
            # clear any pre-filled values
            self.browser.find_element_by_id('searchInput').clear()
            # assign search input object
            search_input = self.browser.find_element_by_id('searchInput')
            # get the search button
            button = self.browser.find_element_by_class_name('button')
            # send the query for search
            search_input.send_keys(query)
            # click it to start searching
            button.click()
            print 'search done'
            return True

    def save_cookies(self, file_name=''):
        # add more code to confirm that below process is successful
        pickle.dump(self.browser.get_cookies(), open(file_name + "cookies.pkl", "wb"))
        # further additions to be made to facilitate more options to play with cookies
        return True

    # method for resuming session
    def load_prev_session(self, file_name=''):
        try:
            # open the cookie file
            fobj = open(file_name + 'cookies.pkl', 'rb')
        # handle the error where cookie file does not exist
        except IOError:
            print 'cookies not present'
            print 'first login to create cookies\nredirecting to login'
            username = raw_input('Enter Your Email Address: ')
            password = raw_input('Enter Password: ')
            self.login(username, password)
        else:
            try:
                cookies = pickle.load(fobj)
            except EOFError:
                print 'cookies empty\nlogin first\nredirecting to login'
                username = raw_input('Enter Your Email Address: ')
                password = raw_input('Enter Password: ')
                self.login(username, password)
            else:
                try:
                    # get the url for which cookie was saved
                    self.browser.get(self.base_url+self.signin_url)
                    for cookie in cookies:
                        self.browser.add_cookie(cookie)
                    # get to the home
                    self.browser.get(self.base_url + self.home_url)
                # handle the exception where cookie is invalid or is of different url
                except selenium.common.exceptions.InvalidCookieDomainException:
                    print 'Invalid cookies\nredirecting to login'
                    username = raw_input('Enter Your Email Address: ')
                    password = raw_input('Enter Password: ')
                    self.login(username, password)

    def take_screenshot(self):
        self.browser.save_screenshot('screen.png')

    # call this method to get the current profile name of the logged person
    def get_user_info(self):
        self.browser.get(self.base_url + '/v0.1/api/profile')
        source = self.view_page_source()
        tree = html.fromstring(source)
        user_info = tree.xpath('/html/body/pre/text()')[0]
        return json.loads(str(user_info))

    # will remove get_name in the next version
    def get_name(self):
        return self.browser.find_element_by_class_name('navbar__callout-text').find_element_by_class_name(
            'ng-binding').text

    # get the current url of the webpage you are interacting with
    def get_url(self):
        url = self.browser.current_url
        # print url
        return url

    # print the source of the current web page
    def view_page_source(self):
        source = self.browser.page_source
        return source

    # call this method to sign out of your current session
    def sign_out(self):
        self.browser.get(self.base_url + self.signout_url)
        print 'signed out'

    # call this method to close the current session
    def close(self, status=0):
        print 'closing and quitting this session'
        self.browser.close()
        self.browser.quit()
        sys.exit(status)


class ItemProcess(Session):
    def get_items(self, sku_Ids):
        for i in sku_Ids:
            skuId = i[0]
            quantity = i[1]
            self.browser.get(self.product_url + skuId)
            self.add_item_to_cart(skuId, quantity)

    def get_cart(self):
        self.browser.get('https://grocery.walmart.com/v0.1/api/cart')
        json_response = self.browser.find_element_by_xpath("/html/head/body/pre").text
        return json_response

    # return human readable data for all the items present in the cart
    # with item name, item quantity, item unit price
    def list_cart_items(self):
        json_data = self.get_cart()
        parse_json_data = json.loads(json_data)
        items = parse_json_data.get('items')
        no_of_different_items = len(items)
        item_list = []
        if no_of_different_items:
            for item in items:
                data = item.get('data')
                item_name = data.get('name')
                item_id = data.get('id')
                status = data.get('status')
                max_allowed = data.get('maxAllowed')
                price = item.get('price')
                unit_price = price.get('unit')
                total_price = item.get('total')
                quantity = item.get('quantity')

                item_list.append([item_name, item_id, status, max_allowed, unit_price, total_price, quantity])
            total = parse_json_data.get('total')
            min_required = parse_json_data.get('minimumTotalForCheckout')
            return [item_list, total, min_required]

        else:
            print "Cart Empty"
            return None

    # add to cart method will be speeded up by using multithreading and multiprocessing,
    # so the same amount of time will be taken for 1 as for 10, depending upon number of threads,
    # right now its one at a time
    def add_item_to_cart(self, sku_Id, quantity):
        add_cart_button = self.browser.find_element_by_xpath("//shadow/form/button[contains(@class,'a2c__cta')]")
        add_cart_button.click()
        if quantity > 1:
            for i in quantity:
                inc_button = self.browser.find_element_by_xpath("//button[contains(@class,'a2c__inc')]")
                inc_button.click()