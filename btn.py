import asyncio
from datetime import datetime
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER

async def send_message(client, target_chat):
    # Define the message with clickable links
    message = (
        "Hello! Please choose an option below:\n\n"
        "👉 [Join Our Channel](https://t.me/mxpayone)\n"
        "👉 [Contact Us](https://t.me/mxpay0)"
    )
    
    # Send the message
    await client.send_message(
        target_chat,
        message,
        parse_mode="markdown"  # Enable markdown for clickable links
    )
    print(f"Message sent to {target_chat} at {datetime.now()}")

async def main():
    # Initialize and start the Telegram client
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        await client.start(phone=PHONE_NUMBER)

        # Replace with the target chat username or ID
        target_chat = "InfernaQueen"  # Example: 'example_group' or chat ID
        await send_message(client, target_chat)

if __name__ == "__main__":
    asyncio.run(main())
