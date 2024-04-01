import requests
from bs4 import BeautifulSoup as BS
from smtplib import SMTP
import csv
import time
import sys
import getpass
import json
import schedule 

# Constants for email configuration
CONFIG_FILE = "config.json"
URLS_FILE = "urls_with_prices.csv"

config = {}

def wait(message, delay=0.1):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def extract_price(URL):
    page = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        },
    )
    soup = BS(page.content, "html.parser")

    try:
        price = float(soup.find(class_="a-price-whole").text.replace(",", "").replace("₹", "").strip())
        product_name = soup.find(id="productTitle").text
    except AttributeError:
        print(f"Error extracting price for {URL}. Check the HTML structure.")
        return None, None

    return price, product_name

def notify(url, product_name, affordable_price):
    print(config)
    server = SMTP(config["SMTP_SERVER"], config["PORT"])
    server.starttls()
    server.login(config["email"], config["password"])

    subject = f"Price Drop Alert: {product_name}"
    body = f"Price has fallen below {affordable_price}. Go BUY it Now --- {url}"
    msg = f"Subject: {subject}\n\n{body}"

    msg = msg.encode('ascii', 'ignore').decode('ascii')

    server.sendmail(config["email"], config["email"], msg)

def remove_url_and_price_from_csv(url, filename=URLS_FILE):
    rows = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == url:
                continue
            rows.append(row)

    with open(filename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in rows:
            csvwriter.writerow(row)

def store_login_credentials(email, password):
    with open(CONFIG_FILE, "w") as config_file:
        json.dump({
            "email": email,
            "password": password,
            "SMTP_SERVER": "smtp.gmail.com",
            "PORT": 587
        }, config_file)

def retrieve_login_credentials():
    global config
    try:
        with open(CONFIG_FILE, "r") as config_file:
            config = json.load(config_file)
            return config["email"], config["password"]
    except FileNotFoundError:
        with open(CONFIG_FILE, "w"):
            pass
        return None, None

def check_price_drop(urls_with_prices):
    for url, affordable_price in urls_with_prices.items():
        print(url)
        print(affordable_price)
        current_price, product_name = extract_price(url)
        if current_price is not None and current_price <= affordable_price:
            notify(url, product_name, affordable_price)
            remove_url_and_price_from_csv(url)

def get_login_info():
    email, password = retrieve_login_credentials()
    if email != None or password != None:
        wait("Verifying your login credentials... \n")
        time.sleep(3)
        print("Verified successfully!!")

    if email is None or password is None:
        print("Welcome to the Price Tracker!")
        print("Let's ensure we have your login information to notify you of price drops.")
        print("")

        email = input("Enter your email: ")
        password = getpass.getpass("Enter your Email Generated password (will be hidden): ")

        wait("Storing your login credentials... \n")
        time.sleep(3)
        print("Done!!")
        store_login_credentials(email, password)

    return email, password

def get_urls_with_prices_from_user():
    urls_with_prices = {}
    while True:
        print("-" * 100)
        url = input("Enter Product URL (or type 'done' to finish): ")
        if url.lower() == "done":
            break

        try:
            price = float(input("Enter affordable price for this URL: "))
            urls_with_prices[url] = price
        except ValueError:
            print("Please enter a valid price.")

        print("-" * 100)

    return urls_with_prices

def store_urls_with_prices_to_csv(urls_with_prices, filename=URLS_FILE):
    with open(filename, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        for url, price in urls_with_prices.items():
            csvwriter.writerow([url, price])

def retrieve_urls_with_prices_from_csv(filename=URLS_FILE):
    urls_with_prices = {}
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            urls_with_prices[row[0]] = float(row[1])

    return urls_with_prices

def job():
    stored_urls_with_prices = retrieve_urls_with_prices_from_csv(URLS_FILE)
    check_price_drop(stored_urls_with_prices)

if __name__ == "__main__":
    email, password = get_login_info()

    config["email"] = email
    config["password"] = password

    store_login_credentials(email, password)

    urls_with_prices = get_urls_with_prices_from_user()
    store_urls_with_prices_to_csv(urls_with_prices)

    schedule.every(1).minutes.do(job)  # Schedule the job to run every 30 minutes
  

    while True:
        schedule.run_pending()
time.sleep(1)