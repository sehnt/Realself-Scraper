import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver import ActionChains
from get_driver import proxy_chrome
import time

proxy_file = open("C:/Users/Steve/Desktop/Realself/proxies.txt", "r", encoding="utf-8")
proxies = []
for proxy in proxy_file.readlines():
    proxy = proxy.strip()
    proxy = proxy.split(":")
    proxies.append(proxy)
    

class Request():
    current_proxy = 0

    def __init__(self, url):
        self.url = url.strip()
        
    def get_data(self) -> list:
        if(Request.current_proxy < len(proxies)-1):
            Request.current_proxy += 1
        else:
            Request.current_proxy = 0
        unique_id = "default"
        if "realself.com/" in self.url:
            unique_id = self.url[self.url.find("realself.com/") + 13:]

        proxy = proxies[Request.current_proxy]
        
        try:
            driver = proxy_chrome(proxy[0], int(proxy[1]), proxy[2], proxy[3], unique_id)
            driver.set_page_load_timeout(60)
        
            driver.get(self.url)
            text = driver.page_source
            if "px-captcha" in text:
                element = driver.find_element_by_css_selector('#px-captcha')
                action = ActionChains(driver)
                click = ActionChains(driver)
                action.click_and_hold(element)
                action.perform()
                time.sleep(10)
                print(" captcha ")
                action.release(element)
                action.perform()
                time.sleep(0.2)
                action.release(element)
            print("Accessing: " + self.url + "\nUsing: " + proxy[0])
            driver.quit()
        
        except:
            # If there are connection failures or problems
            # with specific links, skip them.
            try:
                driver.quit()
            except:
                pass
            text = ""
            
        if "Cosmetic Procedure Reviews" in text:
            text = ""

        return text
        

    def test_data(self) -> list:
        test_path = Path("text.txt")
        return test_path.read_text(encoding="utf-8")
    
