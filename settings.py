import json
from selenium.webdriver.common.by import By

config = {
    "platform_url": "https://learn.umgc.edu/d2l/login?noRedirect=1",
    "username": "vprasanna_continualengine",
    "password": "vikramPrasanna"
}

xpath_chrome = {
    "login_username":{
        "condition": By.ID,
        "path": "userName"},
    "login_password":{
        "condition": By.ID,
        "path": "password"},
    "login_button":{
        "condition": By.XPATH,
        "path": "//*[text()='Log In']"},
    "course_link":{
        "condition": By.XPATH,
        "path": "//*[@class='d2l-link d2l-datalist-item-actioncontrol'][contains(text(),'{course_name}')]"
    },
    "course_glance":{
        "condition": By.XPATH,
        "path": "//*[text()='Course at a Glance']"
    },
    "course_page_iframe_outer":{
      "condition": By.XPATH,
      "path": "//*[@class='d2l-widget-iframe-wrapper']/iframe[@title='Course at a Glance']"  
    },
    "course_page_iframe_inner":{
      "condition": By.XPATH,
      "path": "//iframe[@title='Course at a Glance']"  
    },
    "fetch_number_of_chapters":{
        "condition": By.XPATH,
        "path": "//*[@class='alltiles']/div"
    },
    "first_content_link":{
        "condition": By.XPATH,
        "path": "//*[@class='alltiles']/div[@id='milestone0']/div/div/div[@class='headerarea']/a[1]"
    },
    "each_course_iframe":{
        "condition": By.XPATH,
        "path": "//iframe"
    },
    "chapter_elements": {
        "condition": By.XPATH,
        "path": "//*[@class='navigation-tree']/div[@class='navigation-item']"
    },
    "subchapter_elements": {
        "condition": By.XPATH,
        "path": "//*[@class='title-text']/span[contains(text(), '{subchapter_name}')]"
    },
    "link_element": {
        "condition": By.XPATH,
        "path": "//a"
    }
}


xpath_shadow_root = {
    "home_page_load": "return document.querySelector('d2l-expand-collapse-content div d2l-my-courses').shadowRoot.querySelector('d2l-my-courses-container').shadowRoot.querySelector('d2l-tabs d2l-tab-panel d2l-my-courses-content').shadowRoot.querySelector('div d2l-link h3')",
    "view_all_courses": "return document.querySelector('d2l-navigation-main-header div.d2l-navigation-header-right div d2l-navigation-dropdown-button-icon').shadowRoot.querySelector('button d2l-icon')",
    "course_name_text_box":"return document.querySelector('d2l-input-search').shadowRoot.querySelector('d2l-input-text').shadowRoot.querySelector('div div input')",
    "arrow_expand_course_content": "return document.querySelector('[text=\"Actions for Course at a Glance\"]').shadowRoot.querySelector('d2l-button-icon').shadowRoot.querySelector('button')",
    "expand_course_content": "return document.querySelector('d2l-menu-item[text=\"Expand this widget\"]')",
    "subchapter_content": "return document.querySelector('div.resizing-iframe-container d2l-iframe-wrapper-for-react').shadowRoot.querySelector('iframe')",
}