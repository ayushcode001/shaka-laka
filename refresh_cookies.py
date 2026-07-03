"""
Run this script every 2-3 weeks to refresh your LeetCode session cookies.
It will print the new values — update them in your .env file and GitHub secrets.

Usage:
    python refresh_cookies.py

Requires:
    pip install playwright python-dotenv
    playwright install chromium
"""

import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

LEETCODE_EMAIL    = os.getenv("LEETCODE_EMAIL")
LEETCODE_PASSWORD = os.getenv("LEETCODE_PASSWORD")


def refresh_cookies():
    if not LEETCODE_EMAIL or not LEETCODE_PASSWORD:
        print("ERROR: Add LEETCODE_EMAIL and LEETCODE_PASSWORD to your .env file first.")
        return

    print("Launching browser and logging into LeetCode...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False so you can see it
        context = browser.new_context()
        page    = context.new_page()

        page.goto("https://leetcode.com/accounts/login/", wait_until="networkidle")
        time.sleep(2)

        # Fill credentials
        page.fill('input[name="login"]', LEETCODE_EMAIL)
        page.fill('input[name="password"]', LEETCODE_PASSWORD)
        time.sleep(1)

        print("Please solve the Cloudflare Turnstile captcha in the browser window if prompted...")
        page.click('button[type="submit"]', timeout=60000)

        # Wait for redirect to home
        try:
            page.wait_for_url("https://leetcode.com/", timeout=15000)
        except Exception:
            print("Login may have failed or took too long. Check the browser window.")
            browser.close()
            return

        print("Login successful. Extracting cookies...")
        time.sleep(2)

        cookies = context.cookies()

        session_cookie = next((c for c in cookies if c["name"] == "LEETCODE_SESSION"), None)
        csrf_cookie    = next((c for c in cookies if c["name"] == "csrftoken"), None)

        browser.close()

    if not session_cookie or not csrf_cookie:
        print("Could not find cookies. Try again or copy them manually from the browser.")
        return

    print("\n" + "="*60)
    print("Copy these into your .env file and GitHub Actions secrets:")
    print("="*60)
    print(f"\nLEETCODE_SESSION={session_cookie['value']}")
    print(f"\nLEETCODE_CSRF_TOKEN={csrf_cookie['value']}")
    print("\n" + "="*60)

    # Optionally auto-write back to .env
    update = input("\nAuto-update your .env file? (y/n): ").strip().lower()
    if update == "y":
        _update_env("LEETCODE_SESSION",    session_cookie["value"])
        _update_env("LEETCODE_CSRF_TOKEN", csrf_cookie["value"])
        print(".env updated successfully.")


def _update_env(key: str, value: str):
    env_path = ".env"
    with open(env_path, "r") as f:
        lines = f.readlines()

    updated = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"{key}={value}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)


if __name__ == "__main__":
    refresh_cookies()