from telethon import TelegramClient, events
from datetime import datetime
from config import API_ID, API_HASH, PHONE_NUMBER
from groups import GROUPS  # List of group usernames
from messages import HINDI_MESSAGE, ENGLISH_MESSAGE
import asyncio

# Initialize a global toggle for language selection
toggle_language = True

async def main():
    # Initialize the Telegram client for a user account
    client = TelegramClient('anon', API_ID, API_HASH)

    @client.on(events.NewMessage())  # Listen for new messages
    async def handle_new_message(event):
        global toggle_language

        # Get chat information
        group = await event.get_chat()
        sender = await event.get_sender()

        # Check if the message is from a group in GROUPS and it's not your own message
        if group.username in GROUPS and event.is_group and sender.id != (await client.get_me()).id:
            # Prepare a message to send, alternating between Hindi and English
            response_message = HINDI_MESSAGE if toggle_language else ENGLISH_MESSAGE
            toggle_language = not toggle_language  # Alternate the language
            
            # Wait for 10 seconds before sending the message
            await asyncio.sleep(60)
            
            # Send the message to the same group
            await client.send_message(group, response_message)
            print(f"Message sent to {group.title} at {datetime.now()}")

    # Start the client and keep it running
    async with client:
        print("Listening for messages...")
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
