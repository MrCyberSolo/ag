from messages import HINDI_MESSAGE, ENGLISH_MESSAGE
import asyncio
from datetime import datetime
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER
from groups import GROUPS
from telethon.errors.rpcerrorlist import SlowModeWaitError

async def send_periodic_messages(client, group_name):
    group = await client.get_entity(group_name)  # Get group entity
    toggle = True  # To alternate messages

    while True:
        # Refresh group entity to check slow mode status
        group = await client.get_entity(group_name)
        slow_mode_delay = getattr(group, 'slowmode_seconds', 0)

        if slow_mode_delay > 0:
            print(f"Slow mode active in {group_name}. Waiting for {slow_mode_delay} seconds.")
            await asyncio.sleep(slow_mode_delay + 1)  # Wait until slow mode ends
            continue  # Recheck slow mode after the wait
        
        # Send a message immediately after slow mode ends
        try:
            # Choose message based on toggle
            message = HINDI_MESSAGE if toggle else ENGLISH_MESSAGE
            toggle = not toggle  # Alternate for next iteration

            # Send the message
            await client.send_message(group, message)
            print(f"Message sent to {group_name} at {datetime.now()}")

            # Wait before sending the next message
            await asyncio.sleep(60)

        except SlowModeWaitError as e:
            print(f"Slow mode unexpectedly active in {group_name}. Retrying after {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)  # Wait for the duration specified in the error
        except Exception as e:
            print(f"Error in {group_name}: {e}")
            break

async def main():
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        await client.start(phone=PHONE_NUMBER)
        
        # Create tasks for each group
        tasks = [send_periodic_messages(client, group) for group in GROUPS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
