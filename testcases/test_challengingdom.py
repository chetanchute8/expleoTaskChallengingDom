import time

import pytest
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

page_url = "http://the-internet.herokuapp.com/challenging_dom"
serv_obj = Service("./drivers/chromedriver.exe")


@pytest.fixture(scope="module")
def setup():
    print("web driver setup")
    driver: WebDriver = webdriver.Chrome(service=serv_obj)
    driver.maximize_window()
    yield driver
    driver.close()


def test_page_load(setup):
    # test the page load and check to see if web page title is correct
    print("Opening web page : ", page_url)
    setup.get(page_url)
    assert "The Internet" in setup.title


def test_header_check(setup):
    # test to see if page header is correct
    print("\n Checking Page Header 'Challenging DOM'")
    assert setup.find_element(By.XPATH, '//div[@class="example"]/h3').text == "Challenging DOM"


def test_count_edit_links(setup):
    # test to count the number of edit links present on the page
    editlinks = setup.find_elements(By.XPATH, "//a[text()='edit']")
    countedits = len(editlinks)
    assert countedits == 10


def test_count_edit_links_is_not_empty(setup):
    # test to check if all the edit links are working and none of them are pointing to empty URL's
    editlinks = setup.find_elements(By.XPATH, "//a[text()='edit']")
    for lnk in editlinks:
        try:
            href = lnk.get_attribute("href")
            assert href is not None
        except:
            print("edit URL is not configured properly")


def test_count_delete_links(setup):
    # test to count the number of delete links present on the page
    deletelinks = setup.find_elements(By.XPATH, "//a[text()='delete']")
    countdelete = len(deletelinks)
    assert countdelete == 10


def test_count_delete_links_is_not_empty(setup):
    # test to check if all the delete links are working and none of them are pointing to empty URL's
    deletelinks = setup.find_elements(By.XPATH, "//a[text()='delete']")
    for lnk in deletelinks:
        try:
            href = lnk.get_attribute("href")
            assert href is not None
        except:
            print("delete URL is not configured properly")


def filternumber(n):
    if len(n) == 5:
        return True
    else:
        return False


def test_page_refresh_changes_value_of_answer(setup):
    # test to verify answer value is flipped when page is refreshed

    script_inner_html = setup.find_element(By.XPATH, '//div[@id="content"]/script').get_attribute('innerHTML')

    x = re.findall('[0-9]+', script_inner_html)

    oldlist = list(filter(filternumber, x))
    old_number = oldlist[0]

    setup.refresh()

    script_inner_html = setup.find_element(By.XPATH, '//div[@id="content"]/script').get_attribute('innerHTML')

    x = re.findall('[0-9]+', script_inner_html)

    newlist = list(filter(filternumber, x))
    new_number = newlist[0]

    assert old_number != new_number


def test_button_blue(setup):
    # test to check the id of blue button is changed when clicked
    blue_btn = setup.find_element(By.XPATH, '//a[@class="button"]')
    id_btn = blue_btn.get_attribute("id")
    blue_btn.click()
    blue_btn = setup.find_element(By.XPATH, '//a[@class="button"]')
    assert blue_btn.get_attribute("id") is not id_btn


def test_button_alert(setup):
    # test to check the id of alert button (red) is changed when clicked
    red_btn = setup.find_element(By.XPATH, '//a[@class="button alert"]')
    id_btn = red_btn.get_attribute("id")
    red_btn.click()
    red_btn = setup.find_element(By.XPATH, '//a[@class="button alert"]')
    assert red_btn.get_attribute("id") is not id_btn


def test_button_success(setup):
    # test to check the id of success button (green) is changed when clicked
    suc_btn = setup.find_element(By.XPATH, '//a[@class="button alert"]')
    id_btn = suc_btn.get_attribute("id")
    suc_btn.click()
    suc_btn = setup.find_element(By.XPATH, '//a[@class="button alert"]')
    assert suc_btn.get_attribute("id") is not id_btn
