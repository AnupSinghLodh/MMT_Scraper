from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

def fetch_mmt_coupons_only():
    print("🚀 Opening MakeMyTrip Offers page...")

    # Chrome setup
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Load homepage to allow cookies and scripts
        driver.get("https://www.makemytrip.com/")
        print("🌍 Opened homepage...")
        time.sleep(5)

        # Step 2: Navigate to offers via JavaScript
        driver.execute_script("window.location.href='https://www.makemytrip.com/offers/';")
        print("➡️ Redirected to offers page...")
        time.sleep(8)

        wait = WebDriverWait(driver, 20)

        # Step 3: Close login popup if it appears
        try:
            driver.find_element(By.CSS_SELECTOR, "span.commonModal__close").click()
            print("✅ Login popup dismissed.")
        except:
            print("ℹ️ No login popup found, continuing...")

        print("🔍 Waiting for offer cards to load...")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ofrDealCard")))

        cards = driver.find_elements(By.CSS_SELECTOR, ".ofrDealCard")
        print(f"🧩 Found {len(cards)} offer cards on page.")

        offers = []

        for card in cards:
            try:
                coupon = card.find_element(By.CSS_SELECTOR, ".sprOfrCard__code.copyText.smoothenFont").text.strip()
                if not coupon:
                    continue  # Only keep offers that have a coupon code

                title = card.find_element(By.CSS_SELECTOR, ".ofrDealCard__hdng.smoothenFont").text.strip()
                expiry = card.find_element(By.CSS_SELECTOR, ".time.smoothenFont").text.strip()
                cta = card.find_element(By.CSS_SELECTOR, ".primaryBtn.ofrDealCard__cta.smoothenFont").text.strip()

                try:
                    desc = card.find_element(By.CSS_SELECTOR, ".ofrDealCard__body-lft p").text.strip()
                except:
                    desc = "No description available."

                try:
                    category = card.find_element(By.CSS_SELECTOR, ".makeFlex.column.appendBottom10 span").text.strip()
                except:
                    category = "General Offer"

                offers.append({
                    "Category": category,
                    "Title": title,
                    "Description": desc,
                    "Coupon Code": coupon,
                    "Expiry Date": expiry,
                    "CTA": cta,
                    "Fetched At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except:
                continue

        print(f"✅ Found {len(offers)} offers with coupon codes.\n")

        # ✅ Print all offers
        for i, o in enumerate(offers, 1):
            print(f"🎯 Offer {i}")
            print(f"  Category    : {o['Category']}")
            print(f"  Title       : {o['Title']}")
            print(f"  Description : {o['Description']}")
            print(f"  Coupon Code : {o['Coupon Code']}")
            print(f"  Expiry Date : {o['Expiry Date']}")
            print(f"  CTA         : {o['CTA']}\n")

        # ✅ Save all offers to CSV
        if offers:
            df = pd.DataFrame(offers)
            filename = f"mmt_offers_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 Saved {len(offers)} offers to CSV file: {filename}")
        else:
            print("⚠️ No offers found with coupon codes.")

        return offers

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    fetch_mmt_coupons_only()
