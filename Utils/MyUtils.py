import json
import time
import uuid

from selenium.webdriver.common.by import By


class MyUtils(object):
    def __init__(self):
        pass

    def auto_Scroll(self, driver, timeSleep, active=False, limit_iteration=None):
        cant = 0
        if active:
            time.sleep(timeSleep)
            last_height = driver.execute_script('return document.body.scrollHeight')

            while True:
                driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(timeSleep)
                new_height = driver.execute_script('return document.body.scrollHeight')

                if new_height == last_height:
                    break

                if cant == limit_iteration:
                    break

                last_height = new_height
                cant = cant + 1
            return True

    def take_pic(self, driver, path, active=False):
        if active:
            myUuid = uuid.uuid1()
            el = driver.find_element(By.TAG_NAME, 'body')
            # el.screenshot('{}{}.png'.format(path, myUuid))  #colab
            el.screenshot('{}\\Screenshots\\{}.png'.format(path, myUuid))

    def write_text(self, path, text):
        myUuid = uuid.uuid1()
        with  open('{}\\Files\\Text\\{}.txt'.format(path, myUuid), "w") as file:
            file.write(text)
            file.close()

    def write_json(self, path, JObject, folderName=''):
        if folderName != '':
            folderName = '\\{}'.format(folderName)

        myUuid = uuid.uuid1()
        with  open('{}\\Files{}\\{}.json'.format(path, folderName, myUuid), "w") as file:
            json.dump(JObject, file, indent=4, sort_keys=True)

    def properties_to_object(self, element):
        obj = {}
        for attr in element.get_property('attributes'):
            obj[attr['name']] = attr['value']
        return obj

