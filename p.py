from telethon import TelegramClient, events
import requests
from config import API_ID, API_HASH, PHONE_NUMBER

# GPT API credentials
API_URL = "https://devsdocode-openai.hf.space/chat/completions"
MODEL_NAME = "gpt-4o-mini-2024-07-18"

def get_chat_completion(message, model=MODEL_NAME, temperature=0.7, top_p=1):
    """
    Fetch a chat completion from the GPT API.
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
        "temperature": temperature,
        "top_p": top_p
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return "No response from GPT API."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

async def main():
    # Create the Telegram Client for your user account
    async with TelegramClient('anon', API_ID, API_HASH) as client:

        # Log in with the phone number
        print("Connecting to Telegram...")
        await client.start(phone=PHONE_NUMBER)
        print("Connected!")

        # Event handler for new messages in private chats only
        @client.on(events.NewMessage)
        async def handler(event):
            # Check if the message is from a private chat
            if event.is_private:
                user_message = event.message.message
                sender = await event.get_sender()
                sender_name = sender.first_name if sender else "User"

                # Call GPT API and fetch response
                gpt_response = get_chat_completion(user_message)

                # Send the GPT response back
                await event.reply(f"\n{gpt_response}")

        print("Userbot is running... (Private chats only)")
        await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
