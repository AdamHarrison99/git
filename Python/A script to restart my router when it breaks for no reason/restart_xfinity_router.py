import geckodriver_autoinstaller
import logging
import sys
import time
import os
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

DEBUG=False

logging.basicConfig(
#    filename="selenium-test.log",
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
    level=logging.INFO
)

# credentials
username = "admin"
password = "xxx" # put your own password

if __name__ == "__main__":
    logging.info("STARTING application")

    logging.info("Pinging Servers")
    param = '-n'
    hostname = "google.com" #example
    response = os.system(f"ping {param} 1 {hostname}")

    #and then check the response...
    if response == 0:
      logging.info(f"{hostname} is up!")
    else:
      logging.info(f"{hostname} is down!")

      hostname = "amazon.com" 
      response = os.system(f"ping {param} 1 {hostname}")

      #and then check the response...
      if response == 0:
        logging.info(f"{hostname} is up!")
      else:
        logging.info(f"{hostname} is down!")

        hostname = "1.1.1.1" 
        response = os.system(f"ping {param} 1 {hostname}")

        #and then check the response...
        if response == 0:
          logging.info(f"{hostname} is up!")
        else:
          logging.info(f"{hostname} is down!")

          hostname = "4.2.2.2" 
          response = os.system(f"ping {param} 1 {hostname}")

          #and then check the response...
          if response == 0:
            logging.info(f"{hostname} is up!")
          else:
            logging.info(f"{hostname} is down!")

            hostname = "dns.msftncsi.com" 
            response = os.system(f"ping {param} 1 {hostname}")

            #and then check the response...
            if response == 0:
              logging.info(f"{hostname} is up!")
            else:
              logging.info(f"{hostname} is down!")

    time.sleep(10)
    if response != 0:
        opts = FirefoxOptions()
        opts.add_argument("--headless")

        logging.info("Creating driver (opening browser window)")
        driver = webdriver.Firefox(options=opts)

        logging.info("Loading login page")
        driver.get("http://10.0.0.1")

        logging.info("Entering login information")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)

        logging.info("Submitting login form")
        driver.find_element(By.CLASS_NAME, "btn").click()

        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState == 'complete'")
        )

        logging.info("Loading reset webpage")
        driver.get("http://10.0.0.1/restore_reboot.jst")

        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState == 'complete'")
        )

        logging.info("Clicking reset button")
        driver.find_element(By.ID, "btn1").click()

        if not DEBUG:
            logging.info("Confirming dialog box")
            driver.find_element(By.ID, "popup_ok").click() # the gateway modem takes aprox. 2 minutes to be online again

        logging.info("Waiting for the reset action to be processed")
        time.sleep(30)  # sleep for 30 seconds, this will give time for the request to be processed and to be logged out

        logging.info("Quitting driver (closing browser)")
        driver.quit()
