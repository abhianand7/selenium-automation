import os
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# very important to make it work with firefox
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import time
import json
import logging

# from lxml import html
# for saving cookies
import pickle
# for creating a virtual display
# from pyvirtualdisplay import Display
# display = Display(visible=0, size=(1024, 768))
# display.start()


# flags used in this script
# this flag indicates whether the current session is a logged in session
session_active_flag = False
# if not logged in session, whether it is a cookie loaded session
cookies_loaded_flag = False

# some global variables used
login_attempt = 0

# Firefox selenium update
# currently from firefox version 48, the support for firefox webdriver has been depricated
# firefox now provides a separate webdriver built by itself that runs along with firefox and it is called
# marionette and its driver are called geckodriver but still selenium looks for wires executable
# so download the geckodriver from url 'https://github.com/mozilla/geckodriver/releases' and rename it to 'wires'
# put it onto system PATH variable or simply put it into bin directory inside home as .profile automatically identifies
# bin directory inside home
caps = DesiredCapabilities.FIREFOX
caps["marionette"] = True
caps["binary"] = "/usr/bin/firefox"
dcaps = DesiredCapabilities.PHANTOMJS
dcaps['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
# Phantomjs working solution
# download the phantomjs from
# http://phantomjs.org/download.html
# don't install it directly from ubuntu repo, as that has bugs in it
# again put it into your bin directory of home
# and logout and login again, phantomjs will work


# base class setup for other objects to inherit
class WalMart:
    def __init__(self, base_url, signin_url, home_url, signout_url, product_url):
        self.base_url = base_url
        self.signin_url = signin_url
        self.signout_url = signout_url
        self.home_url = home_url
        self.product_url = product_url
        try:
            self.browser = webdriver.Firefox(capabilities=caps)
            # uncomment one of the following lines to test with a specific browser
            # in order to test with that particular browser you have it installed on your system
            # otherwise leave it as unchanged
            # uncomment the below line for PhantomJS a headless javascript enabled browser
            # self.browser = webdriver.PhantomJS(
            #     desired_capabilities=dcaps,
            #     service_args=['--ignore-ssl-errors=true', '--ssl-protocol=ANY'],
            #     # executable_path= '/home/trusty/bin/phantomjs'
            #     # '/home/trusty/.nvm/versions/node/v5.0.0/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs'
            # )
            # uncomment the below line for Chrome Browser
            # self.browser = webdriver.Chrome()
            # self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
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
            logging.error('selenium exception: {}'.format(e))
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
            logging.error('Session.login - page load timeout')
            print "Timed out waiting for page to load"
            self.close(1)
        else:
            self.take_screenshot(name='login_page')
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
<<<<<<< HEAD
            time.sleep(10)
            self.take_screenshot(name='filled_login')
=======
            time.sleep(10) #TODO: make sure this needs to be here
>>>>>>> 3875d5e0accb8fca3c555e05afaacd379d07a262
            # make sure that login is successful
            if self.user_status():
                logging.debug('Session.login - logged in as {}'.format(self.parse_user_info(FirstName=True)['FirstName']))
                print 'logged in as %s' % self.parse_user_info(FirstName=True)['FirstName']
                # time.sleep(5)
                # save the cookies of this session
                pickle.dump(self.browser.get_cookies(), open("cookies.pkl", "wb"))
                session_active_flag = True
                return session_active_flag
            else:
                session_active_flag = False
                if login_attempt == 3:
                    logging.error('Session.login - giving up after login attempts')
                    print 'exiting, login failed\nplease try again\nverify your login credentials'
                    self.close(1)
                    return session_active_flag
                else:
                    login_attempt += 1
                    logging.warning('Session.login - login failure, retrying')
                    print "login failed\nretrying"
                    self.login(username, password)

    def search(self, query):
        try:
            element_present = EC.presence_of_element_located((By.ID, 'searchInput'))
            WebDriverWait(self.browser, 10).until(element_present)
        except TimeoutException:
            logging.error('Session.search - page load timeout')
            print "Timed out waiting for page to load\nPlease check your Internet Connection"
            self.close(1)
        except selenium.common.exceptions.ElementNotVisibleException as e:
            # handle this exception in case of error
            logging.error('Sessin.search - ElementNotVisibleException: {}'.format(e))
            print e
        except selenium.common.exceptions.NoSuchElementException as e:
            # handle this exception when page loading fails
            logging.error('Sessin.search - NoSuchElementException: {}'.format(e))
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
            logging.error('Session.load_prev_session - IOError, cookies not present')
            print 'cookies not present'
            return False #assume no direct console access
            #print 'first login to create cookies\nredirecting to login'
            #username = raw_input('Enter Your Email Address: ')
            #password = raw_input('Enter Password: ')
            #self.login(username, password)
        else:
            try:
                cookies = pickle.load(fobj)
            except EOFError:
                logging.error('Session.load_prev_session - EOFError, cookies not valid')
                return False
                #print 'cookies empty\nlogin first\nredirecting to login'
                #username = raw_input('Enter Your Email Address: ')
                #password = raw_input('Enter Password: ')
                #self.login(username, password)
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
                    logging.error('Session.load_prev_session - InvalidCookieDomainException')
                    return False
                    #print 'Invalid cookies\nredirecting to login'
                    #username = raw_input('Enter Your Email Address: ')
                    #password = raw_input('Enter Password: ')
                    #self.login(username, password)

    def take_screenshot(self, name=''):
        self.browser.save_screenshot(name + 'screen.png')

    # load the user profile
    def get_profile(self):
        # request needs to be used here as there is no need for selenium for this particular action
        self.browser.get(self.base_url + '/v0.1/api/profile')
        json_resp = self.browser.find_element_by_xpath("//pre").text
        return json.loads(json_resp)  # no need to use str method, it is already in unicode format

    # get status if user is logged in
    def user_status(self):
        profile = self.get_profile()
        # print profile
        status = True if profile['status'] == 'registered' else False
<<<<<<< HEAD
        # print status
=======
        if not status:
            logging.warning('Session.user_status: {}'.format(status))
>>>>>>> 3875d5e0accb8fca3c555e05afaacd379d07a262
        return status

    # to be replaced by json_parser(upcoming)

    def parse_user_info(self, FirstName=False, LastName=False, Email=False, Status=False, Id=False, Addresses=False):
        user_data = self.get_profile()
        # print json_data
        req_details = [FirstName, LastName, Email, Status, Id, Addresses]
        status = user_data['status']
        if status == 'registered':
            first_name = user_data['firstName']
            last_name = user_data['lastName']
            email_address = user_data['emailAddress']
            id = user_data['id']
            address = user_data['addresses']
            store_details = [first_name, last_name, email_address, status, id, address]
            # this will return all the fields requested by you in form of dictionary
            return {['FirstName', 'LastName', 'Email', 'Status', 'Id', 'Address'][index]: store_details[index]
                    for index, i in enumerate(req_details) if i}
        else:
            return {'Status': status}
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
        logging.debug('Session.sign_out - signed out')
        print 'signed out'

    # call this method to close the current session
    def close(self, status=0):
        logging.debug('closing and quitting this session')
        print 'closing and quitting this session'
        self.browser.close()
        self.browser.quit()
        # sys.exit(status) #I don't know if we want to exit when we close the browser


class ItemProcess(WalMart):
    def add_item_to_cart(self, sku_Ids):
        for i in sku_Ids:
            skuId = str(i[0])
            quantity = i[1]
            self.browser.get(self.product_url + skuId)
            self.add(skuId, quantity)

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
    def add(self, sku_Id, quantity):
        add_cart_button = self.browser.find_element_by_xpath("//shadow/form/button[contains(@class,'a2c__cta')]")
        add_cart_button.click()
        if quantity > 1:
            for i in quantity:
                inc_button = self.browser.find_element_by_xpath("//button[contains(@class,'a2c__inc')]")
                inc_button.click()