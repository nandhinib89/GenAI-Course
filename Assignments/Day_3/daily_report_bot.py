import pyautogui
import time
import pyperclip
import re
from datetime import datetime

pyautogui.FAILSAFE = True  # Enable fail-safe feature
pyautogui.PAUSE = 1.0  # Set a pause between actions

print("Step 1: Open the Chrome browser")
time.sleep(2)  # Wait for 2 seconds

pyautogui.hotkey('command', 'space', interval=0.1)  
time.sleep(1)  # Wait for 1 second
pyautogui.write('chrome', interval=0.15) 
time.sleep(1)  
pyautogui.press('enter')  
time.sleep(2)  

print("Step 2: Open a new tab and go to the website")
pyautogui.hotkey('command', 't', interval=0.1)  
time.sleep(1)  
pyautogui.write('https://www.accuweather.com/en/in/chennai/206671/weather-today/206671', interval=0.15)
time.sleep(1)  
pyautogui.press('enter')  
time.sleep(5)  

print("Step 3: Copy the temperature from the website")
time.sleep(2)  # Wait for 2 seconds
pyautogui.hotkey('command', 'a')
time.sleep(1)
pyautogui.hotkey('command', 'c')
time.sleep(1)
page_text = pyperclip.paste()

match = re.search(r'Chennai, Tamil Nadu\s+(\d{1,2})°C', page_text)
if match:
    temperature = match.group(1) + "°C"
    print("Current temperature:", temperature)
else:
    temperature = "Temperature not found"
    print(temperature)

print("Step 4: Get the current date and time")
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.now().strftime("%Y-%m-%d")
print("Current date and time:", current_datetime)
comment = "Its cloudy in Chennai tonight"

print("Step 5: Open Numbers application")
pyautogui.hotkey('command', 'space', interval=0.1)
time.sleep(1)
pyautogui.write('Numbers', interval=0.15)
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)
pyautogui.hotkey('command', 'n', interval=0.1)  
time.sleep(1)  
pyautogui.press('enter')
time.sleep(2)

print("Step 6: Enter data into Numbers")
# Headers
pyautogui.write("Date & Time", interval=0.05)
pyautogui.press('tab')
pyautogui.write("Temperature", interval=0.05)
pyautogui.press('tab')
pyautogui.write("Comment", interval=0.05)
pyautogui.press('enter')

# Data
pyautogui.write(current_datetime, interval=0.05)
pyautogui.press('tab')
pyperclip.copy(temperature)
pyautogui.hotkey('command', 'v') # Paste temperature from clipboard
pyautogui.press('tab')
pyautogui.write(comment, interval=0.05)
pyautogui.press('enter')
time.sleep(2)

print("Step 6: Save the report as an Excel file")
pyautogui.hotkey('command', 's')
time.sleep(2)
filename = f"daily_report_{current_date}"
pyautogui.hotkey('command', 'a')
pyautogui.write(filename, interval=0.05)
time.sleep(1)
pyautogui.press('enter')
time.sleep(2)

print("Step 7: Taking screenshot")
screenshot = pyautogui.screenshot()
screenshot.save(f"Assignments/Day_3/daily_report_{current_date}.png")
print(f"Screenshot saved as daily_report_{current_date}.png")
time.sleep(2)