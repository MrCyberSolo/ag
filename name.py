import asyncio
import requests
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from config import API_ID, API_HASH, PHONE_NUMBER

# API key for API Ninjas
API_KEY = "4BhHH4VTnX2fYTSb1mKWeg==CcUq57Dd2jIGmdsz"

async def fetch_random_user_name():
    """Fetch a random name from the API Ninjas random user API."""
    url = "https://api.api-ninjas.com/v1/randomuser"
    headers = {
        "X-Api-Key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        # Extract the name field
        full_name = data.get("name", "Unknown Name")
        first_name, *last_name_parts = full_name.split(" ", 1)
        last_name = last_name_parts[0] if last_name_parts else ""
        return first_name, last_name
    except Exception as e:
        print(f"Error fetching random user: {e}")
        return "Unknown", "User"

async def update_profile_name(client):
    """Update the Telegram profile name periodically."""
    while True:
        try:
            # Fetch random name
            first_name, last_name = await fetch_random_user_name()

            # Update the profile name on Telegram
            await client(UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name
            ))
            print(f"Profile name updated to: {first_name} {last_name} at {datetime.now()}")
        except Exception as e:
            print(f"Error updating profile name: {e}")

        # Wait for 1 hour before the next update
        await asyncio.sleep(10)

async def main():
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        await client.start(phone=PHONE_NUMBER)

        # Task to update profile name
        await update_profile_name(client)

if __name__ == "__main__":
    asyncio.run(main())
