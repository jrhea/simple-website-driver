#!/usr/bin/env python3
# Prerequisites:
# sudo apt-get install python3
# wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && tar -xvf phantomjs-2.1.1-linux-x86_64.tar.bz2
# sudo pip3 install selenium
# sudo pip3 install click
# sudo pip3 install wget
# 
# Setup env: 
# > source websiteDriver.env
# Usage:
# > ./websiteDriver < commands.txt

import click
import signal
import time
import requests

from sys import argv
from http.client import IncompleteRead
from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from contextlib import contextmanager

class WebsiteDriver:

  @contextmanager
  def wait_for_page_load(self, timeout=30):
    old_page = self.__driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(self.__driver, timeout).until(
      staleness_of(old_page)
    )

  def __init__(self):
    DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
    self.__driver = webdriver.PhantomJS() #executable_path='/Users/jrhea1980/Documents/projects/phantomjs/bin/phantomjs')
    self.__driver.maximize_window()

  def cleanup(self):
    result = 0
    #self.__driver.service.process.send_signal(signal.SIGTERM)   # kill the child process
    self.__driver.quit()                                 # quit the node process
    return result

  def navigate(self,url):
    result = 0
    try:
      self.__driver.get(url)
      print("navigated to: " + url)
    except TimeoutException:
      print("Webpage timed out.")
      result = 1  
    except Exception as e:
      print("Error: ",e)
      self.screenshot('screenshot.png')
      result = 1 
    return result

  def getElementByXPath(self,xpath,delay):
    result = 0
    element = None
    try:
      driver = self.__driver
      element = WebDriverWait(driver, delay).until(
                lambda driver : driver.find_element_by_xpath(xpath))
    except TimeoutException:
       print("Timed out waiting for element to load.")
       result = 1  
    except Exception as e:
      print("Error: ",e)
      self.screenshot('screenshot.png')
      result = 1
    return [result,element]

  def inputText(self,element,text):
    result = 0
    if element is not None:
      element.send_keys(text)
    else:
      result = 1
    return result

  def click(self,element):
    result = 0
    if element is not None:
      element.click()
      self.wait_for_page_load(timeout=30)
    else:
      result = 1
    return result
    
  def downloadFile(self,url,filename,wait=0):
    result = 0
    try:
      session = requests.Session()
      cookies = self.__driver.get_cookies()
      for cookie in cookies: 
        session.cookies.set(cookie['name'], cookie['value'])
      response = session.get(url)
      contentLength = int(response.headers['content-length'])
      counter = 0
      while counter < 3 and wait == 1:
        print("Waiting for report to be generated: ",str(contentLength))
        time.sleep(5)
        response = session.get(url)
        prevContentLength = contentLength
        contentLength = int(response.headers['content-length'])
        if contentLength > 0 and contentLength == prevContentLength:
          counter = counter + 1
        
      file = open(filename,"wb")
      file.write(response.content)
      file.close()
    except Exception as e:
      result = 1
      print ("Error: ", e)
      
    return result

  def screenshot(self,file):
    result = 0
    retries = 10
    count = 0
    while count < retries:
      try:
        self.wait_for_page_load(timeout=30)
        self.__driver.save_screenshot(file)
        result = 0
        break;
      except IncompleteRead as er: 
        count = count + 1
        if count >= retries:
          print("Retries: ", count,". Error: ",er)
        result = 1
      except Exception as e:
        result = 1
        
    return result


@click.command()
@click.pass_context
def cli(ctx):
  ctx.obj=WebsiteDriver()
  startCommandLoop()

@click.pass_context
def startCommandLoop(ctx):
  element = None

  while True:
    command = input("Enter a command: ")

    if command == "navigate":
      url = input("-->Enter url: ")
      result = ctx.obj.navigate(url)

    elif command == "getElementByXPath":
      xpath = input("-->Enter xpath: ")
      delay = input("-->Enter delay: ")
      try: 
        delay = int(delay)
        [result,element] = ctx.obj.getElementByXPath(xpath,delay)
      except ValueError:
        continue

    elif command == "inputText":
      text = input("-->Enter text: ")
      result = ctx.obj.inputText(element, text)
      element = None #reset for next pass

    elif command == "click":
      result = ctx.obj.click(element)
      element = None #reset for next pass

    elif command == "waitCondition":
      condition = input("-->Enter condition: ")
      while element.text != condition:
        time.sleep(5)
        print(element.text)
        ctx.obj.navigate(url)
      element = None    
      
    elif command == "downloadFile":
      url = input("-->Enter url: ")
      url = url.replace("FILE_ID",element.text)
      filename = "../output/" + element.text + ".csv"
      result = ctx.obj.downloadFile(url,filename,1)
      element = None
      
    elif command == "screenshot":
       file = input("-->Enter filename for screenshot: ")
       result = ctx.obj.screenshot(file)

    elif command == "exit":
      ctx.obj.cleanup()
      break;
      
    else: 
      print("Invalid command")

    print(result)

if __name__ == '__main__':
    cli(obj={})