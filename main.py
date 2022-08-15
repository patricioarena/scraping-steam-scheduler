import os
import sys
import json
import uuid
import time
import pymongo
import multiprocessing

from functools import partial
from pymongo import MongoClient
from datetime import datetime
from multiprocessing.dummy import Process
from apscheduler.schedulers.blocking import BlockingScheduler

from Models.Item import Item
from Utils.Convert import Convert
from Utils.MyUtils import MyUtils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if int(os.environ['DEVELOPMENT']) == 1:
    # <editor-fold desc="ChromeOptions for local development">
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-logging')
    options.add_argument('--log-level=0')
    options.add_argument('--v=99')
    options.add_argument('--data-path=/tmp/data-path')
    options.add_argument('--ignore-certificate-errors')
    # </editor-fold>
else:
    # <editor-fold desc="ChromeOptions for heroku">
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    # </editor-fold>


# https://saqibameen.com/blog/deploy-python-cron-job-scripts-on-heroku
# https://devcenter.heroku.com/articles/clock-processes-python
# https://www.youtube.com/watch?v=Ven-pqwk3ec
# https://www.andressevilla.com/running-chromedriver-with-python-selenium-on-heroku/


def multi_process(node: WebElement, nodes: list[WebElement], out_data: list, out_index_error: list, out_no_such_element_exception: list):
    _name = None
    _link = None
    _img = None
    _discount = None
    _priceWithoutDiscounted = None
    _priceWithDiscounted = None

    try:
        _name = node.find_element(By.XPATH, './/div[2]/div[1]/span').text
        _link = node.get_attribute('href')
        _img = node.find_element(By.XPATH, './/div/img').get_attribute('src')
        aux_discount = node.find_element(By.XPATH, './/div[2]/div[4]/div[1]/span').text
        arr = node.find_element(By.XPATH, './/div[2]/div[4]/div[2]').text.split("\n")
        _discount = aux_discount.removeprefix('-').removesuffix('%')
        _priceWithoutDiscounted = arr[0].removeprefix('$').replace(' ', '')
        _priceWithDiscounted = arr[1].removeprefix('$').replace(' ', '')

    except IndexError:
        # out_index_error[nodes.index(node)] = MyUtils().properties_to_object(node)
        out_index_error.append(MyUtils().properties_to_object(node))
        pass

    except NoSuchElementException:
        # out_no_such_element_exception[nodes.index(node)] = MyUtils().properties_to_object(node)
        out_no_such_element_exception.append(MyUtils().properties_to_object(node))
        pass

    item = Item(_name, _link, _img, _discount, _priceWithoutDiscounted, _priceWithDiscounted)
    # out_data[nodes.index(node)] = Convert().to_json(item)
    out_data.append(Convert().to_json(item))


def insert_documents_into_mongodb(documents: list, client: MongoClient, db_name: str, collection_name: str):
    print("--- Start mongo process ---")
    start_time_mongo_process = time.time()
    try:
        # print('You are connected!', client.server_info())
        # print(client.list_database_names())
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_many(documents)
        mongo_total_time = (time.time() - start_time_mongo_process)
        print("--- End of mongo process %s seconds ---" % mongo_total_time)
        return mongo_total_time

    except Exception as e:
        print(e)


def insert_document_into_mongodb(client: MongoClient, db_name: str, collection_name: str, scraping_total_time: float, mongo_total_time: float):
    try:
        # print('You are connected!', client.server_info())
        # print(client.list_database_names())
        db = client[db_name]
        collection = db[collection_name]

        aux_obj = {'scraping_total_time': scraping_total_time, 'mongo_total_time': mongo_total_time}
        collection.insert_one(aux_obj)
        # print(collection_name)

    except Exception as e:
        print(e)


def select_documents_into_mongodb(client: MongoClient, db_name: str):
    try:
        db = client[db_name]

        # recuperar historial
        history = db.list_collection_names()
        print(history)

        history.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)
        print(history)

        print(history[0])

        # tomar la coleccion de interes del historial para ver los juegos
        collection = db[history[0]]
        cursor = collection.find()
        for record in cursor:
            print(record)



    except Exception as e:
        print(e)


def scraping_process():
    print("--- Start scraping process ---")
    start_time_scraping_process = time.time()
    timeSleep = int(os.environ['TIME_SLEEP'])
    elements: list = []
    elements_index_error: list = []
    elements_no_such_element_exception: list = []
    # <editor-fold desc="Scraping process">

    if int(os.environ['DEVELOPMENT']) == 1:
        driver = webdriver.Chrome(service=Service(os.environ['PATH_DRIVER']), options=options)  # For local development
    else:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)  # For heroku

    driver.get(os.environ['SCRAPING_URL'])
    wait = WebDriverWait(driver, int(os.environ['DRIVER_WAIT']))
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search_result_row')))
    MyUtils().auto_Scroll(driver, timeSleep, eval(os.environ['AUTO_SCROLL_ACTIVE']), int(os.environ['LIMIT_ITERATION']))
    # MyUtils().take_pic(driver, os.environ['BASE_PATH'], not True)
    try:
        nodes = driver.find_elements(By.XPATH, '//a[@data-ds-itemkey]')
        # print('Number of elements: {}'.format(len(nodes)))
        # simple_for(nodes, elements, elements_index_error, elements_no_such_element_exception)
        pool = multiprocessing.dummy.Pool()
        pool.map(partial(multi_process, nodes=nodes, out_data=elements, out_index_error=elements_index_error,
                         out_no_such_element_exception=elements_no_such_element_exception), nodes)

        driver.quit()

    except TimeoutException:
        print('Timed out waiting for page to load')
    # MyUtils().write_json(os.environ['BASE_PATH'], elements)
    # MyUtils().write_json(os.environ['BASE_PATH'], elements_index_error, folderName='IndexError_Log')
    # MyUtils().write_json(os.environ['BASE_PATH'], elements_no_such_element_exception, folderName='NoSuchElementException_Log')
    scraping_total_time = (time.time() - start_time_scraping_process)
    print("--- End of scraping %s seconds ---" % scraping_total_time)

    # </editor-fold>
    return elements, scraping_total_time


def main():
    client = MongoClient(os.environ['CONNECTION_STRING'], serverSelectionTimeoutMS=5000)
    db_name = 'ScrapedData'
    collection_name = str(datetime.now().isoformat())
    elements, scraping_total_time = scraping_process()
    mongo_total_time = insert_documents_into_mongodb(documents=elements, client=client, db_name=db_name, collection_name=collection_name)
    insert_document_into_mongodb(client=client, db_name=db_name, collection_name=collection_name, scraping_total_time=scraping_total_time,
                                 mongo_total_time=mongo_total_time)
    # select_documents_into_mongodb(client=client, db_name=db_name)


if __name__ == '__main__':
    main()
