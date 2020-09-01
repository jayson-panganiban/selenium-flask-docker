import shadow_useragent 
import os
import zipfile

from selenium import webdriver
from pyvirtualdisplay import Display


class Driver:

    def __init__(self):
        self.display = Display(visible=False, size=(800,600))
        self.driver = self.get_driver()
            
    def get_driver(self):
        self.display.start()
        user_agent = shadow_useragent.ShadowUserAgent()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--user-agent=%s' % user_agent.most_common)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_extension(self.proxy_extension())

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(15)

        return driver

    def proxy_extension(self):
        PROXY_HOST = ''
        PROXY_PORT = 8080
        PROXY_USER = ''
        PROXY_PASS = ''

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
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };
            chrome.proxy.settings.set({value: config, scope: "regular"}, 
            function() {});
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        dir_path = "assets/chrome_extensions"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        pluginfile = "%s/proxy_auth_%s:%s.zip" % (dir_path, PROXY_HOST, PROXY_PORT)
        with zipfile.ZipFile(pluginfile, "w") as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return pluginfile