import time
import pandas as pd
from settings import config
from utils.chromeOperations import (
    LaunchChrome,UMGC_login, 
    CloseChrome, SearchForCourse, 
    NavigateToCoursePage, FetchEachCourseContent)


def UMGC_Script():
    driver = LaunchChrome(config)
    try:
        UMGC_login(config, driver)
        SearchForCourse(driver, "JAPN 111".upper(),"model 2235".upper())
        chapters_count = NavigateToCoursePage(driver)
        print(chapters_count)
        FetchEachCourseContent(driver)
        time.sleep(3000)
    except Exception as e:
        CloseChrome(driver)
        raise  
    CloseChrome(driver)

if __name__=='__main__':
    UMGC_Script()