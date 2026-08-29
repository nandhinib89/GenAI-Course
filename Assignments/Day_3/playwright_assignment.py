from playwright.sync_api import sync_playwright
from datetime import datetime

print("Starting the Playwright automation script...")
print(f"Script started at: {datetime.now()}")

#Cricbuzz Match Report Bot
#chromium --> cricbuzz site --> Extract one match report --> Screenshot --> final text file
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print("Navigating to Cricbuzz website...")
    page.goto("https://www.cricbuzz.com/")
    page.screenshot(path="cricbuzz_homepage.png")
    print("Screenshot of Cricbuzz homepage saved as cricbuzz_homepage.png")
    
    print("Clicking on the 'Live Scores' link...")
    page.click("text=Live Scores")
    page.screenshot(path="live_scores.png")
    print("Screenshot of Live Scores page saved as live_scores.png")
    
    print(f"Script completed at: {datetime.now()}")
    browser.close()