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
from pyvirtualdisplay import Display

# base_url = 'http://grocery.walmart.com/'
# signout_url = 'usd-estore/register/signoutcontainer.jsp'
# signin_url = 'usd-estore/m/register/signin-only.jsp'
# home_url = 'usd-estore/m/home.jsp'
display = Display(visible=0, size=(1024, 768))
display.start()


# base class setup for other objects to inherit
class WalMart:
    def __init__(self, base_url, signin_url, home_url, signout_url):
        self.base_url = base_url
        self.signin_url = signin_url
        self.signout_url = signout_url
        self.home_url = home_url
        try:
            # self.browser = webdriver.Firefox()
            # uncomment one of the following lines to test with a specific browser
            # in order to test with that particular browser you have it installed on your system
            # otherwise leave it as unchanged
            # uncomment the below line for PhantomJS a headless javascript enabled browser
            # self.browser = webdriver.PhantomJS()
            # uncomment the below line for Chrome Browser
            # self.browser = webdriver.Chrome()
            self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
            # uncomment the below line for Edge Browser
            # self.browser = webdriver.Edge()
            # uncomment the below line for Opera Browser
            # self.browser = webdriver.Opera()
            # uncomment the below line for Safari Browser
            # self.browser = webdriver.Safari()
            # uncomment the below line for Internet Explorer
            # self.browser = webdriver.Ie()
            # self.browser.maximize_window()
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

        self.browser.get(self.base_url + self.signin_url)
        # wait for the element to be present
        try:
            element_present = EC.presence_of_element_located((By.ID, 'emailAddress'))
            WebDriverWait(self.browser, 10).until(element_present)
        except TimeoutException:
            print "Timed out waiting for page to load"
            sys.exit(1)
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

            print 'logged in'
            start = time.time()
            while time.time() - start < 5:
                pass
            # save the cookies of this session
            pickle.dump(self.browser.get_cookies(), open("cookies.pkl", "wb"))

    def search(self, query):
        try:
            element_present = EC.presence_of_element_located((By.ID, 'searchInput'))
            WebDriverWait(self.browser, 10).until(element_present)
        except TimeoutException:
            print "Timed out waiting for page to load\nPlease check your Internet Connection"
            sys.exit(1)
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

    def save_cookies(self, file_name=''):
        pickle.dump(self.browser.get_cookies(), open(file_name + "cookies.pkl", "wb"))

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
        self.browser.save_screenshot('screen-{}.png'.format(datetime.datetime.now()))
    # call this method to get the current profile name of the logged person

    def get_user_info(self):
        self.browser.get(self.base_url + '/v0.1/api/profile')
        source = self.view_page_source()
        tree = html.fromstring(source)
        user_info = tree.xpath('/html/body/pre/text()')[0]
        return json.loads(str(user_info))

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
    def close(self):
        print 'closing and quitting this session'
        self.browser.close()
        self.browser.quit()

