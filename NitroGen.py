import requests
import string
import random
import time
from concurrent.futures import ThreadPoolExecutor
import re

version = "V2.1.6"


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_request(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?application=false&with_subscription_plan=true"
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            print(f"Valid code found: {code}")
            send_to_discord_webhook(code)
        else:
            print(f"Invalid code: {code}")

    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.HTTPError):
            if e.response.status_code == 429:
                print(f"Rate limited. Waiting...")
                time.sleep(10)  # You can adjust this if you want so it runs as fast as it can without ratelimiting
                send_request(code)
            else:
                print(f"Request failed for code {code}. Code may be invalid.")
        else:
            print(f"Request failed for code {code}. Code may be invalid.")

def send_to_discord_webhook(code):
    payload = {"content": f"New valid code: {code}"}
    try:
        requests.post(discord_webhook_url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook for code {code}. Exception: {e}")

def generate_and_send():
    generated_code = generate_random_string(18)
    send_request(generated_code)

def is_valid_webhook(url):
    return re.match(r'https://discord\.com/api/webhooks/\d+/.+', url) is not None

if __name__ == "__main__":
    discord_webhook_url = input("Enter your Discord webhook URL: ")

    while not is_valid_webhook(discord_webhook_url):
        print("Invalid Discord webhook URL. Please enter a valid URL.")
        discord_webhook_url = input("Enter your Discord webhook URL: ")

    print(f"Script started - {version}")

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                executor.submit(generate_and_send)
                time.sleep(7) # You gotta edit this one aswell lmao I don't know why I split it up in to two sleeps to serve the same purpose, too late to go back though.
    except KeyboardInterrupt:
        print("Script stopped by user")
