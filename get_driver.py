# Taken from https://gist.github.com/rajat-np/5d901702a33e7b4b5132b1acee5d778e
# Modified a bit to fit the use case

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import zipfile
import main

def proxy_chrome(PROXY_HOST,PROXY_PORT,PROXY_USER,PROXY_PASS,unique_id="default"):
    manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%(host)s",
                port: parseInt(%(port)d)
              },
              bypassList: ["foobar.com"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%(user)s",
                password: "%(pass)s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
        """ % {
            "host": PROXY_HOST,
            "port": PROXY_PORT,
            "user": PROXY_USER,
            "pass": PROXY_PASS,
        }

    extension_path = main.BASE_PATH / "extension"
    extension_path.mkdir(parents=True, exist_ok=True)
    pluginfile = (main.BASE_PATH / "extension") / (str(hash(unique_id)) + '.zip')

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    co = Options()

    co.add_argument('--disable-gpu')
    #disable infobars
    co.add_argument('--disable-infobars')
    co.add_argument('--window-size=500,500')
    co.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])

    #location of chromedriver, please change it according to your project.
    chromedriver = (main.BASE_PATH / "chromedriver") / "chromedriver.exe"
    
    co.add_extension(pluginfile)
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',desired_capabilities=co.to_capabilities())

    #return the driver with added proxy configuration.
    return driver
