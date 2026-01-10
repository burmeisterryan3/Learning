"""Day 49 Signup."""

import calendar
from datetime import date
import os
import re
import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

GYM_URL = "https://appbrewery.github.io/gym/"
BOOKINGS_URL = "https://appbrewery.github.io/gym/my-bookings"
ACCOUNT_EMAIL = "myaccount@test.com"
ACCOUNT_PASSWORD = "test1234test1234"

booking_summary = {"booked": 0, "waitlisted": 0, "already_booked": 0}


def retry(func=None, retries=7, delay=1, backoff=2, description=None):
    """Build a retry wrapper to handle network failure cases.

    Args:
        func: Function to wrap
        retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier applied to delay after each retry
        description: Optional description for logging
    """

    def decorator(f):
        def inner(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(retries):
                try:
                    result = f(*args, **kwargs)
                    if attempt > 0:
                        func_desc = description or f.__name__
                        print(f"✓ {func_desc} succeeded on attempt {attempt + 1}")
                    return result

                except (
                    NoSuchElementException,
                    TimeoutException,
                    WebDriverException,
                    StaleElementReferenceException,
                ) as e:
                    last_exception = e
                    func_desc = description or f.__name__

                    if attempt < retries - 1:
                        print(f"⚠ {func_desc} failed (attempt {attempt + 1}/{retries}): {type(e).__name__}")
                        print(f"  Retrying in {current_delay:.1f} seconds...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"❌ {func_desc} failed after {retries} attempts")
                        raise last_exception

            # Should not reach here, but just in case
            if last_exception:
                raise last_exception

        return inner

    # Handle both @retry and @retry() syntax
    if func is not None:
        return decorator(func)
    return decorator


@retry(retries=5, delay=2, description="Login")
def login(driver) -> None:
    """Select the login button."""
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.ID, "login-button")))

    login_button = driver.find_element(By.ID, "login-button")
    webdriver.ActionChains(driver).click(login_button).perform()

    # Wait for the login modal to appear
    wait.until(ec.presence_of_element_located((By.ID, "email-input")))

    email_input = driver.find_element(By.ID, "email-input")
    password_input = driver.find_element(By.ID, "password-input")

    email_input.clear()
    password_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_button = driver.find_element(By.ID, "submit-button")
    webdriver.ActionChains(driver).click(submit_button).perform()

    # Wait for login to complete
    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

    return


def get_class_and_date(id_text: str) -> tuple[str, str, str]:
    """Get month and day from the id attribute of an element."""
    # pattern = r"^(?:[^-]+-){3}\d{4}-(\d{2})-(\d{2})"
    pattern = r"^(?:[^-]+-){2}([^-]+)-\d{4}-(\d{2})-(\d{2})"  # To assist capture of the class name
    match = re.search(pattern, id_text)
    if match:
        class_name = match.group(1)
        month_num = int(match.group(2))
        day = match.group(3)
        month_abbr = calendar.month_abbr[month_num]

        return (class_name.capitalize(), day, month_abbr)

    return ("Error", "Error", "Error")


def build_date_annotation(day: str, num_day: str, month: str) -> str:
    """Build a string using the day and month for printing a message to the user."""
    if date.today().day == int(num_day):
        message = f"Today ({day}, {month} {num_day})"
    elif int(num_day) - date.today().day == 1:
        message = f"Tomorrow ({day}, {month} {num_day})"
    else:
        message = f"{day}, {month} {num_day}"

    return message


@retry(retries=5, delay=1, description="Book class")
def book_class(driver, day="tue", time="1800") -> None:
    """Find class details."""
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "[id^='day-group']")))

    element = driver.find_element(By.CSS_SELECTOR, f"[id*='{day}'][id^='day-group']")
    course_div = element.find_element(By.CSS_SELECTOR, f"[id*='{time}']")

    booked = course_div.get_attribute("data-user-booked")
    waitlisted = course_div.get_attribute("data-user-waitlisted")
    class_status = course_div.get_attribute("data-class-status")

    course_button = element.find_element(By.CSS_SELECTOR, f"button[id*='{time}']")
    id_text = course_button.get_attribute("id")
    class_name, num_day, month_abbr = get_class_and_date(id_text)

    day = day.capitalize()
    date_annotation = build_date_annotation(day, num_day, month_abbr)

    if booked == "true":
        print(f"✓ Already Booked: {class_name} Class on {date_annotation}")
        booking_summary["already_booked"] += 1
    elif waitlisted == "true":
        print(f"✓ Already on Waitlist: {class_name} Class on {date_annotation}")
        booking_summary["already_booked"] += 1
    else:
        webdriver.ActionChains(driver).click(course_button).perform()
        wait.until(
            lambda _: course_button.get_attribute("data-user-booked") == "true"
            or course_button.get_attribute("data-user-waitlisted") == "true"
        )
        if class_status == "full":
            print(f"✓ Joined Waitlist: {class_name} Class on {date_annotation}")
            booking_summary["waitlisted"] += 1
        else:
            print(f"✓ Booked: {class_name} Class on {date_annotation}")
            booking_summary["booked"] += 1

    return


@retry(retries=5, delay=1, description="Final verification")
def final_verification(driver) -> None:
    """Pretty print a summary."""
    expected_num_classses = sum(booking_summary.values())
    print(f"\n--- Total Tuesday/Thursay 6pm classes: {expected_num_classses} ---\n")

    driver.get(BOOKINGS_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))
    element = driver.find_element(By.ID, "my-bookings-page")

    print("--- VERIFICATION RESULT --- ")
    bookings_count = int(element.get_attribute("data-bookings-count"))
    waitlist_count = int(element.get_attribute("data-waitlist-count"))
    actual_booking_count = bookings_count + waitlist_count

    print(f"Expected: {expected_num_classses} bookings")
    print(f"Found: {actual_booking_count} bookings")

    if expected_num_classses == actual_booking_count:
        print("✅ SUCCESS: All bookings verified!")
    else:
        print(f"❌ MISMATCH: Missing {expected_num_classses - actual_booking_count} booking(s)")

    return


def main():
    """Main logic."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(GYM_URL)

    login(driver)

    desired_bookings = [("tue", "1800"), ("thu", "1800")]
    for booking in desired_bookings:
        book_class(driver, booking[0], booking[1])
    final_verification(driver)


def admin():
    """Allow for admin changes main should be unaware of."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(GYM_URL)


if __name__ == "__main__":
    main()
    # admin()
