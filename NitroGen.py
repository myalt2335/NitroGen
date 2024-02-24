import requests
import string
import random
import time
from concurrent.futures import ThreadPoolExecutor
import re

version = "V2.1.5"

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_request(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?application=false&with_subscription_plan=true"
    try:
        response = requests.get(url)
        response.raise_for_status()

        log(f"Status Code: {response.status_code} - {code}")

        if response.status_code == 200:
            log(f"Valid code found: {code}")
            send_to_discord_webhook(code)
        else:
            log(f"Invalid code: {code}")

    except requests.exceptions.RequestException as e:
        log(f"Request failed for code {code}. Exception: {e}")

def send_to_discord_webhook(code):
    payload = {"content": f"New valid code: {code}"}
    try:
        requests.post(discord_webhook_url, json=payload)
    except requests.exceptions.RequestException as e:
        log(f"Failed to send webhook for code {code}. Exception: {e}")

def log(message):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

def generate_and_send():
    generated_code = generate_random_string(18)
    send_request(generated_code)

def is_valid_webhook(url):
    return re.match(r'https://discord\.com/api/webhooks/\d+/.+', url) is not None

if __name__ == "__main__":
    log(f"Script started - {version}")

    discord_webhook_url = input("Enter your Discord webhook URL: ")

    while not is_valid_webhook(discord_webhook_url):
        print("Invalid Discord webhook URL. Please enter a valid URL.")
        discord_webhook_url = input("Enter your Discord webhook URL: ")

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                executor.submit(generate_and_send)
                time.sleep(7)
    except KeyboardInterrupt:
        log("Script stopped by user")
