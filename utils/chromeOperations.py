import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException,TimeoutException as WebTimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from settings import xpath_chrome, xpath_shadow_root


def type_text(driver, actions, element_xpath, value):
    # Type in value in an element text box
    try:
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (element_xpath["condition"], 
                element_xpath["path"])
                ))
        element = driver.find_element(element_xpath["condition"], element_xpath["path"])
        actions.move_to_element(element).perform()
        element.clear()
        element.click()
        element.send_keys(value)
        # time.sleep(5)
    except WebDriverException as we:
        print(str(we))
        raise


def click_element(driver, actions, element_xpath, check_for_multi_elements=False):
    # Click on element
    try:
        element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (element_xpath["condition"], 
                element_xpath["path"])
                )) 
        if check_for_multi_elements:
            multi_elements = driver.find_elements(element_xpath["condition"], element_xpath["path"])
            if len(multi_elements)>1:
                element = multi_elements[1]
        actions.move_to_element(element).perform()
        element.click()
    except StaleElementReferenceException:
        print("Stale element exception found waiting for 5 sec")
        time.sleep(5)
        click_element(driver, actions, element_xpath)
    except WebDriverException as we:
        print(str(we))
        raise
    

def send_keys_to_element(element, key):
    element.send_keys(key)
    
    
def switch_to_iframe(driver, frame_element):
    wait_until_element_appear(driver, frame_element)
    element = WebDriverWait(driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it(
                (frame_element["condition"], 
                frame_element["path"])
                )) 
    time.sleep(2)
    return driver
    # element = driver.find_element(frame_element["condition"], frame_element["path"])
    # driver.switch_to


def wait_until_element_appear(driver, element_xpath):
    # Wait until element visible
    try:
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (element_xpath["condition"], 
                element_xpath["path"])
                ))
        return element
        # time.sleep(5)
    except WebDriverException as we:
        raise
    
    
def wait_until_elements_appear(driver, actions, element_xpath):
    # Wait until element visible
    try:
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_all_elements_located(
                (element_xpath["condition"], 
                element_xpath["path"])
                ))
        return element
        # time.sleep(5)
    except WebDriverException as we:
        raise
     
    
def move_to_element(driver, actions: ActionChains, element_xpath):
    # Wait until element visible
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (element_xpath["condition"], 
                element_xpath["path"])
                ))
        actions.move_to_element(element).perform()
        time.sleep(2)
        return element
        # time.sleep(5)
    except WebDriverException as we:
        raise


def fetch_multiple_elements(driver, element_xpath):
    wait_until_element_appear(driver,element_xpath)
    elements = driver.find_elements(element_xpath["condition"], element_xpath["path"])
    return elements


def shadow_root_element_click(driver, actions: ActionChains, element_xpath):
    element = driver.execute_script(element_xpath)
    actions.move_to_element(element).perform()
    element.click()
    return element


def shadow_root_element_type(driver, actions: ActionChains, element_xpath, value):
    shadow_root_element_wait(driver, element_xpath)
    element = driver.execute_script(element_xpath)
    actions.move_to_element(element).perform()
    element.clear()
    element.click()
    element.send_keys(value)
    return element


def shadow_root_element_wait(driver, element_xpath):
    # wait until element loads for 5 min
    wait_counter = 0
    while wait_counter<30:
        try:
            element=driver.execute_script(element_xpath)
            break
        except:
            time.sleep(5)
            wait_counter+=1
            
    if wait_counter==30:
        raise WebDriverException("Failed to load the element")
    else:
        return element


def LaunchChrome(config):
    driver = webdriver.Chrome("chromedriver")
    driver.get(config["platform_url"])
    driver.maximize_window()
    return driver


def UMGC_login(config: dict, driver: webdriver.Chrome):
    
    actions = ActionChains(driver)
    # Enter username
    type_text(driver, actions, xpath_chrome["login_username"], config["username"])
    # Enter password
    type_text(driver, actions, xpath_chrome["login_password"], config["password"])
    # Click login
    click_element(driver, actions, xpath_chrome["login_button"])
    #Wait for login page to load
    shadow_root_element_wait(driver, xpath_shadow_root["view_all_courses"])
    print("Login successful")


def CloseChrome(driver):
    driver.close()
    driver.quit()
      
    
def SearchForCourse(driver, course_name, model_name):
    actions = ActionChains(driver)
    shadow_root_element_click(driver, actions, xpath_shadow_root["view_all_courses"])
    print("Clicked on view course")
    element = shadow_root_element_type(driver, actions, xpath_shadow_root["course_name_text_box"], (course_name+" "+model_name))
    send_keys_to_element(element, Keys.ENTER)
    print("Hit enter")
    course_link_xpath = dict(xpath_chrome["course_link"])
    course_link_xpath["path"] = course_link_xpath["path"].format(course_name=course_name)
    wait_until_element_appear(driver, course_link_xpath)
    print("Course link loaded")
    time.sleep(1)
    click_element(driver, actions, course_link_xpath)
    print("Clicked on course link")
    
    
def NavigateToCoursePage(driver):
    actions = ActionChains(driver)
    time.sleep(5)
    
    # Expand Courses
    move_to_element(driver, actions, xpath_chrome["course_glance"])
    shadow_root_element_click(driver, actions, xpath_shadow_root["arrow_expand_course_content"])
    try:
        shadow_root_element_click(driver, actions, xpath_shadow_root["expand_course_content"])
        print("Expanded course")
    except WebDriverException:
        shadow_root_element_click(driver, actions, xpath_shadow_root["arrow_expand_course_content"])
        print("Course already expanded")
    
    # Switch to contents iframe
    driver = switch_to_iframe(driver, xpath_chrome["course_page_iframe_outer"])
    print("Switched to first iframe")
    driver = switch_to_iframe(driver, xpath_chrome["course_page_iframe_inner"])
    print("Switched to second iframe")
    
    # Calculate total number of chapter
    elements = fetch_multiple_elements(driver, xpath_chrome["fetch_number_of_chapters"])
    chapters_count = len(elements)
    
    # Navigate to all course page
    wait_until_element_appear(driver,xpath_chrome["first_content_link"])
    print("First chapter link visible")
    click_element(driver, actions,xpath_chrome["first_content_link"])
    print("Navigating to course main page")
    
    return chapters_count


def find_shadow_dom(driver):
    pass


def FetchEachCourseContent(driver):
    actions = ActionChains(driver)
    driver = switch_to_iframe(driver, xpath_chrome["each_course_iframe"])
    print("Switched to each course iframe")
    
    # Iterate over each chapter
    chapter_elements = fetch_multiple_elements(driver, xpath_chrome["chapter_elements"])
    start = True
    link_count = 0
    for chapter_ele in chapter_elements:
        #Fetch all chapter names
        chapter_names = chapter_ele.text.split("\n")
        
        # Clicking on main chapter
        main_chapter_name = chapter_names[0]
        chapter_xpath = dict(xpath_chrome["subchapter_elements"])
        chapter_xpath["path"] = chapter_xpath["path"].format(subchapter_name=main_chapter_name)
        print(f"Expanding chapter {main_chapter_name}")
        if not start:
            click_element(driver, actions, chapter_xpath)
        else:
            start = False
            
        # Click on each sub chapter
        sub_chapter_names = chapter_ele.text.split("\n")
        print(f"Number of subchapter: {len(sub_chapter_names)-1}")
        chapter_link_count = 0
        chapter_links = []
        try:
            for i in range(len(sub_chapter_names)):
                if str(sub_chapter_names[i]).startswith("Due:"):
                    continue
                subchapter_xpath = dict(xpath_chrome["subchapter_elements"])
                subchapter_xpath["path"] = subchapter_xpath["path"].format(subchapter_name=sub_chapter_names[i])
                print(f"Clicking on {sub_chapter_names[i]}")
                print(subchapter_xpath["path"])
                move_to_element(driver, actions, subchapter_xpath)
                click_element(driver, actions, subchapter_xpath, check_for_multi_elements=True)
                
                # Fetch subchapter content
                shadow_element = shadow_root_element_wait(driver, xpath_shadow_root["subchapter_content"])
                stat = WebDriverWait(driver, 30).until(
                    EC.frame_to_be_available_and_switch_to_it(shadow_element)) 
                link_element = xpath_chrome["link_element"]
                all_link_elements = driver.find_elements(link_element["condition"], link_element["path"])
                for each_link in all_link_elements:
                    link_attr = each_link.get_attribute('outerHTML').split(" ")
                    link_attr=[text for text in link_attr if "href" in text]
                    if len(link_attr)==1:
                        link_attr = link_attr[0]
                        link_attr = link_attr.split("href=")[1]
                        if "umgc" in link_attr and (not "https://umgc.edu/" in link_attr) and (not "mailto:" in link_attr):
                            chapter_links.append(link_attr)
                            chapter_link_count+=1
            
                driver.switch_to.default_content()
                driver = switch_to_iframe(driver, xpath_chrome["each_course_iframe"])  
        except WebDriverException as e:
            try:
                driver.switch_to.default_content()
                driver = switch_to_iframe(driver, xpath_chrome["each_course_iframe"])  
            except:
                pass
            print("Error found for chapter: ")
            print(e)
            continue        
        print(len(all_link_elements))
            # switch_to_iframe(iframe_driver, )
    
        subchapter_count = len(sub_chapter_names)-1
        link_count = link_count + chapter_link_count + subchapter_count
        print(f"Total links in chapter {main_chapter_name}: {chapter_link_count},chapters: {subchapter_count}")
        print(f"The links are :")
        print(chapter_links)
        print(f"Collapsing chapter {main_chapter_name}")
        click_element(driver, actions, chapter_xpath)
        click_element(driver, actions, chapter_xpath)
        
    