from selenium.webdriver.chrome.webdriver import WebDriver
from .driver import Driver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Spider(Driver):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.copart.com"

    def login(self):
        self.driver.get(self.base_url + "/login/")
        self.driver.find_element_by_id("username").send_keys("")
        self.driver.find_element_by_id("password").send_keys("")
        self.driver.find_element_by_css_selector(".loginfloatright.margin15").click()

    def get_car_info(self, lot_id, member=False):
        if member:
            self.login()

        self.driver.get(f"{self.base_url}/lot/{lot_id}")

        car_info = None
        try:
            if self.driver.find_element_by_css_selector('[alt="404"]').is_displayed():
                return 404
        except NoSuchElementException:
            keys = [
                k.text
                for k in self.driver.find_elements_by_css_selector("label.left.bold")
            ]
            values = [
                v.text
                for v in self.driver.find_elements_by_css_selector(
                    "span.lot-details-desc.right"
                )
            ]
            car_info = dict(zip(keys, values))
            car_info["Bid Price"] = self.get_element_text(".panel.clr span.bid-price")
            car_info["Sale Location"] = self.get_element_text(
                '.panel.clr [data-uname="lotdetailSaleinformationlocationvalue"]'
            )
            car_info["Sale Date"] = self.get_element_text(
                "span.lot-sale-date [ng-if^=validateDate]"
            )
            car_info["Sale Status"] = self.get_element_text(
                "div.clearfix.pt-5.clr .lot-details-desc"
            )
        except StaleElementReferenceException:
            self.get_car_info(lot_id, member)
        finally:
            self.driver.delete_all_cookies()
            self.driver.quit()
            self.display.stop()
        return car_info

    def get_car_list(self, url=None, is_all_pages=False):
        self.driver.get(url)
        car_list = []
        try:
            car_list = self.get_row_data(car_list)
            while (
                self.driver.find_element_by_id(
                    "serverSideDataTable_next"
                ).get_attribute("class")
                != "paginate_button next disabled"
            ):
                if not is_all_pages:
                    break
                self.driver.find_element_by_css_selector(
                    "#serverSideDataTable_next>a"
                ).click()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            '#serverSideDataTable_processing[style="display: none;"]',
                        )
                    )
                )
                car_list = self.get_row_data(car_list)
        except NoSuchElementException:
            return 404
        except StaleElementReferenceException:
            car_list = self.get_row_data(car_list)
        finally:
            self.driver.delete_all_cookies()
            self.driver.quit()
            self.display.stop()
        return car_list

    def get_row_data(self, car_list):
        self.scroll_until_loaded()
        for r in self.driver.find_elements_by_css_selector(
            "#serverSideDataTable tbody>tr"
        ):
            r.location_once_scrolled_into_view
            topr = r.find_element_by_css_selector("td:nth-child(2)>div:nth-child(1)")
            car_list.append(
                {
                    "lot_id": topr.get_attribute("lot-id"),
                    "description": topr.get_attribute("lot-desc").strip(),
                    "bid": topr.get_attribute("bid-string"),
                    "img_url": topr.find_element_by_css_selector("a>img").get_attribute(
                        "src"
                    ),
                    "sale_date": " ".join(
                        r.find_element_by_css_selector(
                            'td>[data-uname="lotsearchLotauctiondate"]'
                        ).text.split("\n")
                    ),
                    "location": r.find_element_by_css_selector(
                        'td [data-uname="lotsearchLotyardname"]'
                    ).text,
                    "odometer": r.find_element_by_css_selector(
                        'td>[data-uname="lotsearchLotodometerreading"]'
                    ).text,
                    "doc_type": r.find_element_by_css_selector(
                        'td>[data-uname="lotsearchSaletitletype"]'
                    ).text,
                    "damage": r.find_element_by_css_selector(
                        'td>[data-uname="lotsearchLotdamagedescription"]'
                    ).text,
                    "est_retail_value": r.find_element_by_css_selector(
                        'td>[data-uname="lotsearchLotestimatedretailvalue"]'
                    ).text,
                }
            )
        return car_list

    def scroll_until_loaded(self):
        check_height = self.driver.execute_script("return document.body.scrollHeight;")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            try:
                self.wait.until(
                    lambda driver: self.driver.execute_script(
                        "return document.body.scrollHeight;"
                    )
                    > check_height
                )
                check_height = self.driver.execute_script(
                    "return document.body.scrollHeight;"
                )
            except Exception:
                break

    def get_element_text(self, selector):
        element_text = ""
        try:
            return self.driver.find_element_by_css_selector(selector).text
        except NoSuchElementException:
            return element_text
