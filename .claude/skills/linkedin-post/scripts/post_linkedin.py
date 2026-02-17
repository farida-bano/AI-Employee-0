import os
import argparse
import asyncio
from playwright.async_api import async_playwright

async def post_linkedin(content):
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')

    if not linkedin_email or not linkedin_password:
        print("Error: LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables must be set.")
        return

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto("https://www.linkedin.com/login")
            await page.fill("#username", linkedin_email)
            await page.fill("#password", linkedin_password)
            await page.click(".login__form_action_container button")
            
            await page.wait_for_selector('div.artdeco-card') # Wait for the homepage to load

            # Click the "Start a post" button
            await page.click("button[aria-label='Start a post']")

            # Fill the post content
            await page.fill(".editor-content__editable", content)

            # Click the "Post" button
            await page.click("button[data-control-name='share.post']")
            
            await browser.close()
            print("Success: LinkedIn post created.")

    except Exception as e:
        print(f"Error: Failed to create LinkedIn post. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a LinkedIn text post.")
    parser.add_argument("--content", required=True, help="The text content of the LinkedIn post.")
    args = parser.parse_args()

    asyncio.run(post_linkedin(args.content))
