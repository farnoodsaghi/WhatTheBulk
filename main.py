from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from func import automate, SENT_BUTTON, MAIN_PAGE
import time

# Read message from file
with open('message.txt', 'r') as text_message:
    message = text_message.read()
    print(f'Message:\n{message}')

# Encode message so that it can be concatenated to the url
message = quote(message)

# Read phone numbers from file
with open('numbers.txt', 'r') as phone_numbers:
    num_set = {num.strip('\n') for num in phone_numbers}

ORIGINAL_LENGTH = len(num_set)

print(f'Found {ORIGINAL_LENGTH} number(s) in the list')
input('Press ENTER to proceed ')
print('Login to WhatsApp once your browser opens up')
time.sleep(5)

driver = webdriver.Chrome(ChromeDriverManager(
    log_level=0, print_first_line=False).install())

driver.get('https://web.whatsapp.com/')

# Wait indefinitely for user to login
while True:
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, MAIN_PAGE)))
        break
    except TimeoutException:
        pass

success_count, fail_count = 0, 0
failures = []

# Iterate over phone numbers and send message
try:
    while num_set:
        num = num_set.pop()
        url = f'https://web.whatsapp.com/send?phone={num}&text={message}'

        r = automate(driver, url, 15)

        if r == SENT_BUTTON:
            success_count += 1
            print(f'({ORIGINAL_LENGTH - len(num_set)} / {ORIGINAL_LENGTH})'
                  f' Successfully sent message to {num}')
        else:
            failures.append(num)
            fail_count += 1
            print(f'({ORIGINAL_LENGTH - len(num_set)} / {ORIGINAL_LENGTH})'
                  f' Failed to send message to {num}')
# Save remaining numbers to file if process is manually interrupted
except KeyboardInterrupt:
    with open('remainder.txt', 'w') as remaining_numbers:
        for r_num in num_set:
            print(r_num, file=remaining_numbers)
    print('Process was manually interrupted')

# Write failures to file
with open('failures.txt', 'w') as failed_numbers:
    for f_num in failures:
        print(f_num, file=failed_numbers)

# Print summary
print('\nOperation Complete')
print('Summary:', f'\t\tSuccessful = {success_count}',
      f'\t\tFailed = {fail_count}',
      f'\t\tTotal = {fail_count + success_count}', sep='\n')

time.sleep(10)
driver.close()
