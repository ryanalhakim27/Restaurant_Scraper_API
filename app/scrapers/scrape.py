#Import Necessary Library
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time as waktu
import numpy as np
from tqdm import tqdm
from fake_useragent import UserAgent
import timeit
import re
from dataclasses import dataclass, field
import random
import string

def generate_id()-> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))

def get_user_agent():
    return UserAgent(verify_ssl=False).random

list_jam_basic = [
    'am6', 'am7', 'am8', 'am9', 'am10',
    'am11', 'pm12', 'pm13', 'pm14', 'pm15', 'pm16', 'pm17', 'pm18', 'pm19', 'pm20', 'pm21', 'pm22', 'pm23'
]

list_jam24_basic=[
    'am0', 'am1', 'am2', 'am3', 'am4', 'am5', 'am6', 'am7', 'am8', 'am9', 'am10',
    'am11', 'pm12', 'pm13', 'pm14', 'pm15', 'pm16', 'pm17', 'pm18', 'pm19', 'pm20', 'pm21', 'pm22', 'pm23'
]

list_hari_basic=[
    'minggu','senin', 'selasa',
    'rabu', 'kamis', 'jumat', 'sabtu'
]

@dataclass
class Scrape_Resto:
    kecamatan: str
    kota: str
    provinsi: str
    resto_id: int
    url: str = 'https://www.google.com/maps'
    user_id: str = field(default_factory=generate_id)
    list_jam: list[int] = field(default_factory=lambda: list_jam_basic)
    list_jam24: list[int] = field(default_factory=lambda:list_jam24_basic)
    list_hari: list[str] = field(default_factory=lambda: list_hari_basic)
    restos: list[WebElement]=field(default_factory=list)
    resto_list : list[dict] = field(default_factory=list)
    resto_with_review_list : list[dict]=field(default_factory=list)
    keyword : str=  None
    user_agent : str= None

    def __post_init__(self):
        self.keyword="restaurant di dekat Kecamatan {}, {}, {}".format(self.kecamatan,
                                                                      self.kota,
                                                                      self.provinsi)
        self.chrome_options=webdriver.ChromeOptions()
        self.services=Service(ChromeDriverManager().install())
        self.user_agent=get_user_agent()
        self.chrome_options.add_argument(f"user-agent={self.user_agent}")
        self.chrome_options.add_argument("--headless=new")
        self.chrome_options.add_argument("--no-sandbox")
        self.driver=webdriver.Chrome(service=self.services, options=self.chrome_options)

    def go_to_page(self):
        driver=self.driver
        #go to the url
        driver.get(self.url)
        #search search box
        search_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//form[@id="XmI62e"]//input[@id="searchboxinput"]'))
        )
        #input keyword
        search_box.send_keys(self.keyword)
        #Click seach button
        WebDriverWait(driver,60).until(
            EC.element_to_be_clickable((By.XPATH,'//button[@id="searchbox-searchbutton"]'))
        ).click()

    
    def preparation(self):
        self.go_to_page()
        driver=self.driver
        start_time=timeit.default_timer()
        #Wait resto page load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m6QErb .DxyBCb')))
        start=0
        start_id=self.resto_id
        while True:
            self.restos = driver.find_elements(By.CSS_SELECTOR,"div.Nv2PK.THOPZb.CpccDe")
            for resto in self.restos[start:len(self.restos)]:
                rests={
                    'resto_id':None,
                    'resto_name':None,
                    'resto_rating':None,
                    'rating_numbers':None,
                    'resto_kecamatan':self.kecamatan,
                    'resto_link':None
                }
                rests['resto_name']=resto.find_element(By.CSS_SELECTOR,'div.qBF1Pd.fontHeadlineSmall').text
                rests['resto_link']=resto.find_element(By.CSS_SELECTOR,'a.hfpxzc').get_attribute("href")
                resto_rating=resto.find_elements(By.CSS_SELECTOR,'span.MW4etd')
                if resto_rating:
                    rating=resto_rating[0].text
                    rests['resto_rating']=float(rating.replace(',','.'))
                    rating_numbers=resto.find_element(By.CSS_SELECTOR,'span.UY7F9').text
                    rating_numbers=rating_numbers.replace('.','')
                    rests['rating_numbers']=int(rating_numbers[1:-1])
                else:
                    rests['resto_rating']=None
                    rests['rating_numbers']=0
                
                start_id+=1
                rests['resto_id']=start_id
                start=len(self.restos)
                self.resto_list.append(rests)
            driver.execute_script("arguments[0].scrollIntoView();", self.restos[-1])
            waktu.sleep(3)

            # if scroll height has not changed - exit
            last = driver.find_elements(By.CSS_SELECTOR, 'span.HlvSq')
            if last:
                stop_time=timeit.default_timer()
                running_time= stop_time-start_time
                print(f'Data Preparation is Success in {running_time} second')
                return self.resto_list
            else:
                continue
        
        
    
    def get_resto_data(self):
        driver=self.driver
        print('Downloading Process')
        for resto in tqdm(self.resto_list):
            driver.get(resto['resto_link'])
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'div.Io6YTe.fontBodyMedium.kR99db'))
            )
            
            #Resto Type
            restotypes=driver.find_elements(By.CSS_SELECTOR, 'button.DkEaL')
            if restotypes:
                resto['resto_type']=driver.find_element(By.CSS_SELECTOR, 'button.DkEaL').text
            else:
                resto['resto_type']=np.nan
            
            #Resto Address
            resto_address=driver.find_elements(By.XPATH,'//div[@class="Io6YTe fontBodyMedium kR99db "]')
            resto['resto_address']=resto_address[0].get_attribute("textContent")
            
            #Operation Time
            resto_operation_time={}
            time_click_main=driver.find_elements(By.CSS_SELECTOR, 'div.OqCZI.fontBodyMedium.WVXvdc')
            if time_click_main:
                webdriver.ActionChains(driver).move_to_element(time_click_main[0]).click(time_click_main[0]).perform()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table.eK4R0e.fontBodyMedium'))
                )
                operation_day=[]
                
                #Find operation day
                operation=driver.find_elements(By.CSS_SELECTOR,'td.ylH6lf')
                for i in range(7):
                    ops=operation[i]
                    operation_day.append(ops.text.lower())
                for day in operation_day:
                    resto_operation_time[day]={}
                
                #Find operation hours
                open_time=[]
                close_time=[]
                operation_hours=driver.find_elements(By.CSS_SELECTOR,'li.G8aQO')
                for i in range(7):
                    ops_time=operation_hours[i]
                    if len(ops_time.text)>6:
                        if ops_time.text == 'Buka 24 jam': 
                            open_time.append('00:01')
                            close_time.append('23:59')
                        else:
                            open_time.append(ops_time.text[0:-6].replace('.',':'))
                            close_time.append(ops_time.text[-5:len(ops_time.text)].replace('.',':'))
                    else:
                        open_time.append('00:00')
                        close_time.append('00:00')
                for oper_day in range(7):
                    day=operation_day[oper_day]
                    resto_operation_time[day]['open_hour']=open_time[oper_day]
                    resto_operation_time[day]['close_hour']=close_time[oper_day]
                resto['operation_time']=resto_operation_time
            else:
                resto['operation_time']=np.nan
        
            #Crowd level
            resto['crowd_level']={}
            day_collection=driver.find_elements(By.CSS_SELECTOR,'div.g2BVhd')
        
            if day_collection:
                for i in range(len(day_collection)):
                    collect_day=day_collection[i]
                    collect_jam=collect_day.find_elements(By.CSS_SELECTOR,"div.dpoVLd")
                    duration=len(collect_jam)
                    crowd_per_day={}
                    resto['crowd_level'][self.list_hari[i]]=crowd_per_day
                    if duration == 18:
                        for j in range(duration):
                            proba=collect_jam[j].get_attribute("aria-label")
                            proba_new=re.findall('[0-9]+', proba)
                            crowd_per_day[self.list_jam[j]]=int(proba_new[0])
                    elif duration == 24:
                        for j in range(duration):
                            proba=collect_jam[j].get_attribute("aria-label")
                            proba_new=re.findall('[0-9]+', proba)
                            crowd_per_day[self.list_jam24[j]]=int(proba_new[0])
                    elif duration > 18 and duration <24:
                        resto['crowd_level']={}
                        break
                    elif duration == 1:
                        continue
            else:
                resto['crowd_level']={}

            #Find About Data    
            resto['about']={}    
            small_button=driver.find_elements(By.CSS_SELECTOR,'button.XJ8h0e.L6Bbsd')
            if small_button:
                webdriver.ActionChains(driver).move_to_element(small_button[0]).click(small_button[0]).perform()
                waktu.sleep(4)
                abouts_element=driver.find_elements(By.CSS_SELECTOR,'div.iP2t7d.fontBodyMedium')
                for about_element in abouts_element:
                    title=about_element.find_element(By.CSS_SELECTOR,'h2.iL3Qke.fontTitleSmall').text.lower().replace(' ','_')
                    contents=[]
                    about_contents=about_element.find_elements(By.CSS_SELECTOR,'li.hpLkke')
                    for content in about_contents:
                        contents.append(content.text)
                    resto['about'][title]=contents
            else:
                resto['about']={}
                
        driver.quit()
        print('All resto data has been downloaded')
  
    def scrape_resto_data(self):
        print('Please Wait for Data Preparation!')
        self.preparation()
        self.get_resto_data()
        return self.resto_list
    
    def resto_with_review(self):
        for resto in self.resto_list:
            rtw={}
            if resto['rating_numbers'] != 0:
                rtw['resto_id']=resto['resto_id']
                rtw['resto_name']=resto['resto_name']
                rtw['resto_link']=resto['resto_link']
                rtw['rating_numbers']=resto['rating_numbers']
                self.resto_with_review_list.append(rtw)
            else:
                continue
        return self.resto_with_review_list
             