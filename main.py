from messages import HINDI_MESSAGE, ENGLISH_MESSAGE
import asyncio
from datetime import datetime
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER
from groups import GROUPS

async def send_periodic_messages(client, group_name):
    group = await client.get_entity(group_name)  # Get group entity
    toggle = True  # To alternate messages
    while True:
        # Choose message based on toggle
        message = HINDI_MESSAGE if toggle else ENGLISH_MESSAGE
        toggle = not toggle  # Alternate for next iteration

        # Send message
        await client.send_message(group, message)
        print(f"Message sent to {group_name} at {datetime.now()}")
        await asyncio.sleep(60)  # Wait for a minute

async def main():
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        await client.start(phone=PHONE_NUMBER)
        tasks = [send_periodic_messages(client, group) for group in GROUPS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
