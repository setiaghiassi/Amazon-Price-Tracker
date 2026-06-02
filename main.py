import os
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()

# Environment variables
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASS = os.getenv("MY_PASS")
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

# Headers to simulate a real browser request
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
}

# Sending request to Amazon
response = requests.get(url=URL, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

# Finding elements safely
price_element = soup.find(class_="a-price-whole")
fraction_element = soup.find(class_="a-price-fraction")
title_element = soup.find(id="productTitle")

# Anti-bot check
if price_element and fraction_element and title_element:
    # 🛠️ FIX: Clean the whole number parts by removing newlines, spaces, and extra dots
    num = price_element.text.replace(".", "").strip()
    fraction = fraction_element.text.strip()
    price = f"{num}.{fraction}"

    price_float = float(price)

    # Cleaning product name spacing
    product_name = title_element.text.strip()

    print(f"Success! Product found: {product_name}")
    print(f"Current Price: ${price_float}")

    target_price = 100

    # Creating the email message
    message = MIMEText(
        f"Subject: Amazon price alert!\n\n"
        f"{product_name} is now ${price_float}!\n"
        f"Buy it here: {URL}",
        "plain",
        "utf-8"
    )

    # Check price and send email
    if price_float <= target_price:
        with smtplib.SMTP(SMTP_ADDRESS, 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASS)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="ghiassisatia@gmail.com",
                msg=message.as_string()
            )
        print("Alert email sent successfully!")
    else:
        print("Price is still above target. No email sent.")

else:
    print("Anti-bot alert: Amazon blocked the request or changed the page layout. Could not find the elements.")