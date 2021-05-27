import argparse
import logging
import uuid
import os
import time
import coloredlogs

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Parsing provided args
parser = argparse.ArgumentParser()
parser.add_argument("--method", type=str, required=True)
parser.add_argument("--user", type=str, required=False)
parser.add_argument("--pw", type=str, required=False)
parser.add_argument("--set-mining-timeout", type=int, dest="miningtimeout", required=False, default=300)
parser.add_argument("--set-mining-cooldown", type=int, dest="miningcooldown", required=False, default=300)
parser.add_argument("--debug", dest="debug", action="store_true")
parser.add_argument("--no-force-miner", dest="force_miner", action="store_false", default=True)
parser.add_argument("--mac", dest="mac", action="store_true", default=False)
args = parser.parse_args()

# Initializing logger
process_uid = uuid.uuid4()
logger = logging.getLogger(f"{process_uid}")
# Setting logging level
logger.setLevel("DEBUG" if args.debug else "INFO")

# If logs directory doesn't exist
if not os.path.exists("logs"):
    # Create logs directory
    os.mkdir("logs")
# Setting log file
log_file_handler = logging.FileHandler(f"logs/debug_{process_uid}.log")
# Setting log format
log_file_handler.setFormatter(logging.Formatter("{asctime} | {levelname} | {message}", style="{"))
# Setting log handler
logger.addHandler(log_file_handler)

# Creating stream handler
stream_handler = logging.StreamHandler()
# Enabling ms logging in log file
coloredlogs.install(milliseconds=True)

# Setting log format
stream_handler.formatter = coloredlogs.ColoredFormatter("{asctime} | {levelname} | {message}", style="{")
# Clearing logging handlers
logging.root.handlers.clear()
# Setting the handler created
logging.root.addHandler(stream_handler)
logger.debug("Logging setup successfully!")
logger.info(f"Process ID is {process_uid}.")

# Path to Chromedriver
driver_path = "./chromedriver"
# Providing files path depending on OS (if --mac flag is provided)
if args.mac:
    # Path to Brave executable
    brave_path = "./Brave Browser.app/Contents/MacOS/Brave Browser"
else:
    # Path to Brave executable
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# Setting browser's desired capabilities
d = DesiredCapabilities.CHROME
# Enabling logging for browser
d['goog:loggingPrefs'] = {'browser': 'ALL'}

# Setting browser options
option = webdriver.ChromeOptions()
# Setting browser's log level
option.add_argument('log-level=3')
# Setting windows size upon launch
option.add_argument('window-size=929, 1012')
# Providing browser executable location
option.binary_location = brave_path
# Setting browser language to English
option.add_argument("--lang=en")
# Disabling infobars
option.add_argument("--disable-infobars")

# Initializing browser
driver = webdriver.Chrome(executable_path=driver_path, options=option, desired_capabilities=d)
# Creating variable and setting it to current window handle
main_page = driver.current_window_handle

# Available login methods
methods = ["manual", "wax", "reddit"]
# Getting specified login method
login_method = args.method

# If invalid login method provided
if login_method not in methods:
    logger.fatal("You entered incorrect login method.")
    # Stop running the script
    exit(0)

# If the method chosen is not manual
if login_method != "manual":
    # Use --user and --pw args
    username = args.user
    password = args.pw

# Setting cooldown in case the script is unable to get it from website logs
cooldown = args.miningcooldown

# Opening wax website
driver.get("https://wallet.wax.io/")

# Pre-setting size variable to 0, 0
size = 0, 0


def preload():  # logs into wax.io
    logger.debug("Preloading...")
    # If reddit is chosen as login method
    if login_method == "reddit":
        while True:
            logger.info("Logging in via Reddit.")
            logger.debug("Clicking Reddit login.")
            # Trying to click on reddit login button
            try:
                driver.find_element_by_id("reddit-social-btn").click()
            except:
                # If the website is reddit
                if driver.current_url.startswith("https://www.reddit.com/"):
                    logger.debug("Website is reddit, breaking.")
                    # Break the loop
                    break
                else:
                    time.sleep(0.5)
            else:
                break
        while True:
            logger.debug("Logging in")
            # Trying to enter reddit credentials
            try:
                # Filling the username field
                driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input').send_keys(
                    username)
                # Filling the password field
                driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[2]/input').send_keys(
                    password)
                # Clicking login button
                driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()
            except:
                time.sleep(0.1)
            else:
                break
            time.sleep(2)
        while True:
            logger.debug("Allowing Reddit API.")
            # Trying to click 'allow' button to enable WAX to access reddit account API
            try:
                driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/form/div/input[1]').click()
            except:
                time.sleep(0.5)
            else:
                break
            time.sleep(3)

    # If login method selected is wax
    # TODO Fix wax login
    elif login_method == "wax":
        logger.info("Logging in via Wax.")
        while True:
            # Trying to enter wax account credentials
            try:
                logger.debug("Entering login credentials.")
                # Filling the username field
                driver.find_element_by_name("userName").send_keys(username)
                # Filling the password field
                driver.find_element_by_name("password").send_keys(password)

                # Captcha checking loop
                while True:
                    logger.debug("Waiting to solve captcha.")
                    # Setting captcha status block to variable
                    captcha = driver.find_element_by_class_name('status').text
                    # If captcha is solved
                    if captcha == "Solved":
                        logger.debug("Captcha solved.")
                        # Break the loop
                        break
                    time.sleep(1)

                logger.debug("Clicking login button.")
                # Clicking the login button
                driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[5]/button[1]").click()
            except:
                time.sleep(0.5)
            else:
                break
        time.sleep(3)

    # If login method selected is manual
    else:
        logger.info("Manual login selected. You have 60 seconds to log in.")
        # Waiting 60 senconds for user to log in
        time.sleep(60)

    # Checking if wax page is loaded
    while True:
        if driver.current_url != "https://wallet.wax.io/dashboard":
            logger.debug("Waiting for dashboard to load.")
            time.sleep(0.6)
        else:
            break
    logger.debug("Switching to Alien Worlds.")
    # Opening alienworlds page
    driver.get("https://play.alienworlds.io/")
    global size
    logger.debug(f"Size = {size}.")

    # Setting window size variable to 500, 500
    size = 500, 500
    logger.debug(f"Resizing window to {size}.")
    # Resizing window
    driver.set_window_size(size[0], size[1])


def login():  # Login into alienworlds
    t = 0
    time.sleep(5)
    logger.info("Logging in to Alien Worlds.")
    # When the time spent is less than 15 seconds, otherwise continue running
    while t < 15:
        logger.debug("Waiting for login page to load.")
        # Check logs for message
        for e in driver.get_log('browser'):
            if "Input Manager initialize...\\n" in e["message"]:
                logger.debug("Login page loaded.")
                t = 30
                break
        time.sleep(0.5)
        # If no message was found, increment t variable, run the loop again
        t += 0.5
    global size
    time.sleep(5)

    _debugLog = driver.get_log('browser')
    # Resize window
    driver.set_window_size(size[0], size[1])
    # Setting button coordinates to (250, 230)
    x, y = 250, 230
    logger.debug(f"Clicking at ({x}, {y}).")
    # Clicking login button
    ActionChains(driver).move_by_offset(x, y).click().perform()
    time.sleep(0.2)
    logger.debug(f"Backing.")
    # Moving cursor back to 0, 0
    ActionChains(driver).move_by_offset(-x, -y).perform()
    time.sleep(5)

    logger.info("Successfully logged in to Alien Worlds.")


def miner(force=False):  # Activates miner menu button
    logger.info("Going to mining menu.")
    found = False
    # While message in log is not found
    while not found:
        logger.debug(f"Waiting for miner")
        # If force mode is enabled
        if force is True:
            logger.debug(f"Force mode is enabled. Continuing.")
            # Break the loop
            break
        # Check browser log
        for e in driver.get_log('browser'):
            # If the message is found
            if "successfully downloaded and stored in the indexedDB cache" in e["message"]:
                found = True
                logger.debug("Successfully loaded the page. Continuing to mining menu.")
                break
        # Wait 1 second between loop cycles
        time.sleep(1)
    time.sleep(15)
    # Resize window
    driver.set_window_size(size[0], size[1])
    # Setting mining menu coordinates
    x, y = 405, 110
    logger.debug(f"Clicking at ({x}, {y}).")
    # Clicking the button
    ActionChains(driver).move_by_offset(x, y).click().perform()
    time.sleep(0.2)
    logger.debug(f"Backing.")
    # Moving the cursor back to (0, 0)
    ActionChains(driver).move_by_offset(-x, -y).perform()
    time.sleep(3)
    logger.info("Successfully entered mining menu.")


def mine():  # Starts mining
    logger.info("Starting mining.")
    started = False
    # Resizing window
    driver.set_window_size(size[0], size[1])
    # Setting mine button coordinates
    x, y = 250, 275
    t = 0
    # While mining cycle hasn't started and time spent trying to start is less than 30 seconds
    while not started and t < 30:
        logger.debug("Waiting for mining to start.")
        logger.debug(f"Clicking at ({x}, {y}).")
        # Clicking mine button
        ActionChains(driver).move_by_offset(x, y).click().perform()
        time.sleep(0.2)
        logger.debug(f"Backing.")
        # Moving the cursor back to (0, 0)
        ActionChains(driver).move_by_offset(-x, -y).perform()
        # Checking the browser log
        for e in driver.get_log('browser'):
            # If the mining started
            if "start doWork" in e["message"]:
                started = True
                break
        # If the button was 'Claim'
        if driver.current_url.startswith("https://all-access.wax.io/"):
            started = True
            # Break the loop
            break
        time.sleep(0.6)
        t += 0.8

    # If time spent is >= 30
    if t >= 30:
        logger.warning(f"Starting mining timed out. Reloading.")
        # Reloading the website
        driver.refresh()
        logger.debug("Page reloaded.")
        time.sleep(10)
        # Returning False (the cycle hasn't started)
        return False

    # If the cycle has started
    if started:
        logger.info("Started mining.")
        return True


def wait_for_mining_to_finish():
    t = 0
    logger.debug("Waiting for mining to finish.")
    # While time spent mining is less than provided (300 seconds by default)
    while t < float(args.miningtimeout):
        # Check the log for message
        for e in driver.get_log('browser'):
            if "end doWork" in e["message"]:
                logger.info("Finished mining.")
                # Clicking Claim button
                # Claim button coordinates
                x, y = 210, 200
                logger.debug(f"Clicking at ({x}, {y}).")
                # Clicking claim button
                ActionChains(driver).move_by_offset(x, y).click().perform()
                time.sleep(0.2)
                logger.debug("Backing.")
                # Moving cursor back to (0, 0)
                ActionChains(driver).move_by_offset(-x, -y).perform()
                time.sleep(5)
                # Return True (Mined successfully)
                return True
        time.sleep(0.6)
        t += 0.6
    # If the mining took longer
    logger.warning(f"Mining took longer than {args.miningtimeout} seconds. Reloading.")
    # Reload the website
    driver.refresh()
    logger.debug("Page reloaded.")
    time.sleep(2)
    # Return False (Mining took too long, the page was reloaded)
    return False


def start_new_cycle():  # Starts another cycle
    logger.info("Starting a new cycle.")
    logger.debug(f"Reloading the page.")
    # Reload the page
    driver.refresh()
    logger.debug("Page reloaded.")
    time.sleep(5)


def end():  # Finds sleep time and waits
    logger.info("Ending the cycle.")
    logger.debug(f"Resizing the window to ({size[0]}, {size[1]}).")
    # Resizing window
    driver.set_window_size(size[0], size[1])
    global cooldown
    if cooldown is not None:
        # If cooldown value is > 5
        if cooldown > 5:
            logger.info(f"Sleeping for {cooldown} seconds until the cooldown.")
            # Wait until next mining cycle
            time.sleep(cooldown)
            logger.info("Mining cooled down. Starting a new cycle.")
    time.sleep(5)


def main():
    logger.info("Initializing.")
    # Log in to the account
    preload()
    # Mining loop
    while True:
        driver.switch_to.window(driver.window_handles[0])
        mining_completed = False
        # Loop in case mining fails
        while not mining_completed:
            mining_started = False
            # Loop in case mining won't start
            while not mining_started:
                # Login to alien worlds
                login()
                # Enter the mining menu
                miner(args.force_miner)
                # Start mining, check if it has started
                mining_started = mine()
            # Wait for mining to finish, check if it didn't time out
            mining_completed = wait_for_mining_to_finish()
        # End the cycle
        end()
        # Start another cycle
        start_new_cycle()


if __name__ == "__main__":
    main()
