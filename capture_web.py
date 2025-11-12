"""Capture web page screenshots using Playwright."""

import asyncio
from playwright.async_api import async_playwright


async def capture_screenshot(url: str, output_path: str) -> None:
    """Capture a screenshot of the given URL."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(2000)  # Wait 2 seconds for rendering
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()
        print(f"Screenshot saved to {output_path}")


async def main():
    """Capture screenshots of the web application."""
    urls = [
        ("http://127.0.0.1:8000", "screenshot_home.png"),
        ("http://127.0.0.1:8000/api/docs", "screenshot_api_docs.png"),
    ]

    for url, filename in urls:
        print(f"Capturing {url}...")
        await capture_screenshot(url, filename)


if __name__ == "__main__":
    asyncio.run(main())
