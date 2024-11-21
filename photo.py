import asyncio
import requests
from PIL import Image
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest
import os
from config import API_ID, API_HASH, PHONE_NUMBER

async def download_and_prepare_image(url, file_path):
    """Download the image and ensure it's formatted properly."""
    try:
        # Download the image
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image downloaded successfully: {file_path}")
        else:
            raise Exception(f"Failed to download image, status code: {response.status_code}")

        # Validate and resize the image to 800x800
        with Image.open(file_path) as img:
            img = img.convert("RGB")  # Ensure it's in RGB mode
            img = img.resize((800, 800), Image.Resampling.LANCZOS)  # Resize to 800x800
            img.save(file_path, format="JPEG")
            print(f"Image prepared as 800x800 JPEG: {file_path}")
    except Exception as e:
        print(f"Error downloading or preparing image: {e}")
        raise

async def change_client_photo(client, image_path):
    """Upload the image and set it as the profile photo."""
    try:
        # Upload the file to Telegram
        uploaded_file = await client.upload_file(image_path)

        # Update the profile photo
        result = await client(UploadProfilePhotoRequest(file=uploaded_file))
        print("Profile photo updated successfully:", result)
    except Exception as e:
        print("Error updating profile photo:", e)

async def main():
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        await client.start(phone=PHONE_NUMBER)

        # Step 1: Download and prepare the image
        image_url = "https://sharedp.com/wp-content/uploads/2024/07/krishna-images-for-dp-920x1024.jpg"
        local_image_path = "profile.jpg"  # Local file path to save the image
        await download_and_prepare_image(image_url, local_image_path)

        # Step 2: Update the profile picture
        await change_client_photo(client, local_image_path)

if __name__ == "__main__":
    asyncio.run(main())
