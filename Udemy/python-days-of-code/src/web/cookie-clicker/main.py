"""Day 48 Challenge."""

import asyncio
import time

from playwright.async_api import async_playwright


async def print_status(page) -> None:
    """Print the current score and status."""
    status = await page.locator("#cookies").inner_text()
    total = status.splitlines()[0]
    rate = status.splitlines()[1]
    print(f"Total: {total}")
    print(f"Rate {rate} cookies per second")


async def make_purchase(page) -> None:
    """Make the most expensive purchase of a product available."""
    products = page.locator(".product.unlocked.enabled")
    count = await products.count()
    if count > 0:
        await products.last.click()
        await print_status(page)


async def main():
    """Main logic."""
    timeout = time.time() + 60 * 5  # 5 minutes from now

    async with async_playwright() as p:
        args = ["--disable-blink-features=AutomationControlled"]  # Help avoid CloudFlare checks
        browser = await p.chromium.launch(headless=False, args=args)
        page = await browser.new_page()
        await page.goto("http://orteil.dashnet.org/cookieclicker/")
        await page.locator("#langSelect-EN").wait_for()
        await page.locator("#langSelect-EN").click()

        locator = page.locator("#bigCookie")

        while time.time() < timeout:
            score_check = time.time() + 5
            while time.time() < score_check:
                await locator.click(force=True)
            await make_purchase(page)

        await print_status(page)


if __name__ == "__main__":
    asyncio.run(main())
