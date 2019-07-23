"""
WebHTML

This class is used to get html data from urls
"""

import os
import time
import string
import random

from bs4 import BeautifulSoup
import html5lib
import urllib

from selenium import webdriver
from selenium.webdriver.firefox.options import Options # firefox options


class WebHTML:
    """
    Class gets HTML from web urls
    """
    download_folder = None

    tries_max = 3 # how many tries until give up ( connecting to url )

    headless = True # runs firefox headless mode ( no window )
    window_size = (1024,768) # sets window size that firefox should be opened in

    custom_user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
    proxies = { "http": "127.0.0.1:8888", "https": "127.0.0.1:8888"}
    headers = {
        "User-Agent": custom_user_agent,
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }
    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), '../geckodriver'))

    mime_types = [
        'text/plain', # .txt
        'application/pdf', # pdf
        'application/csv', # csv
        'application/vnd.ms-excel', #excel
        'application/zip' # zip
    ]

    def __init__(self):
        return

    @staticmethod
    def get_html( url, download=False, filename=None ):

        try_connect = True
        connection_tries = 0

        page_html = None
        final_url = None

        print(WebHTML.gecko)

        # browser version

        while try_connect and connection_tries < WebHTML.tries_max:
            print("connecting:" + url)
            try:
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", WebHTML.custom_user_agent)

                if WebHTML.headless:
                    options = Options()
                    options.add_argument('--headless')

                    profile.set_preference("browser.download.manager.showWhenStarting", False);

                    if WebHTML.download_folder == None:
                        profile.set_preference("browser.download.folderList",1)
                    else:
                        profile.set_preference("browser.download.folderList",2) # 0 = desktop, 1=downloads, 2=last specified location
                        profile.set_preference("browser.download.dir",WebHTML.download_folder)

                    profile.set_preference("browser.download.manager.closeWhenDone",True)
                    profile.set_preference("browser.download.manager.focusWhenStarting",True)

                    opt_str = "application/octet-stream"
                    for t in WebHTML.mime_types:
                        opt_str += ',' + t

                    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", opt_str)

                    #driver = webdriver.Firefox(firefox_options=self.options);


                    browser = webdriver.Firefox( firefox_profile=profile, executable_path=WebHTML.gecko, options=options )
                else:
                    browser = webdriver.Firefox( firefox_profile=profile, executable_path=WebHTML.gecko )

                # set browser window size
                browser.set_window_size(WebHTML.window_size[0], WebHTML.window_size[1])

                print("get url")
                if download:
                    if filename != None and WebHTML.download_folder != None:
                        urllib.request.urlretrieve(url, WebHTML.download_folder + '/' + filename)
                    else:
                        raise ValueError("download_folder and filename need to be set")
                else:
                    browser.get(url)

                print('got url')
                time.sleep(random.uniform(5,10))

                print('finished sleep')

                if download == False:
                    page_html = browser.page_source
                    final_url = browser.current_url

                browser.quit()

                try_connect = False

            except Exception as inst:
                print (inst)
                connection_tries += 1
                time.sleep(random.uniform(5,10))

        if page_html == None:
            print("No page_html")
            return None, None

        # make pretty html first
        soup = BeautifulSoup(page_html, 'html5lib')

        # remove tags
        [x.extract() for x in soup.findAll('script')] # remove scripts
        [x.extract() for x in soup.findAll('input')] # remove inputs
        [x.extract() for x in soup.findAll('style')] # remove style
        [x.extract() for x in soup.findAll('iframe')] # remove iframe

        # prettify
        prettyHTML = soup.prettify()

        # return soup with prettified html
        return BeautifulSoup(prettyHTML, 'html5lib'), final_url
