import requests
from bs4 import BeautifulSoup
from telegram import Bot, constants
import asyncio
import time

# Telegram bot token
bot_token = '6804553299:AAFMF_QJjUGwM1J4eRLFUIPVy5zjTZJgnL0'
# Telegram channel ID or username
telegram_channel_username = '@BananaNews12'  # Replace with your channel username

bot = Bot(token=bot_token)

async def fetch_news():
    url = "https://zehabesha.com/"
    try:
        response = requests.get(url)
        if response.ok:  # Checks if response status code is 200
            soup = BeautifulSoup(response.content, "html.parser")

            # Fetch text from specific tags known to contain news
            texts = soup.find_all(['p', 'span', 'div'])

            # Filter and clean up the text
            filtered_texts = [text.get_text(strip=True) for text in texts if 20 < len(text.get_text(strip=True)) < 300]

            return filtered_texts if filtered_texts else ["No relevant text items found."]
        else:
            return [f"Failed to fetch text: HTTP status code {response.status_code}"]
    except Exception as e:
        return [f"Error occurred: {e}"]

async def send_message_to_telegram(message):
    try:
        await bot.send_message(chat_id=telegram_channel_username, text=message, parse_mode=constants.ParseMode.HTML)
    except Exception as e:
        print(f"Failed to send message to Telegram channel. Error: {e}")

async def send_news_to_telegram():
    await send_message_to_telegram("Fetching text content...")
    text_results = await fetch_news()
    for text in text_results:
        # Send each news item to the Telegram channel
        await send_message_to_telegram(text)
        # Sleep for a short duration to avoid being blocked by the server
        await asyncio.sleep(5)

# Create an event loop
async def main():
    await send_news_to_telegram()

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
