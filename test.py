from telethon import TelegramClient, events
import requests
import json
from config import API_ID, API_HASH, PHONE_NUMBER, OWNER_ID  # Add OWNER_ID to config.py

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
        response = requests.post(API_URL, json=payload, timeout=3000)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return "I'm sorry, but I couldn't process your request at the moment. Please try again later."
    except requests.exceptions.Timeout:
        return "The system is currently busy. Please try again in a few moments."
    except requests.exceptions.RequestException:
        return "There was an issue connecting to the server. Please try again later."


def load_groups():
    """
    Load group usernames from the 'groups.json' file.
    """
    try:
        with open("groups.json", "r") as file:
            groups = json.load(file)
    except FileNotFoundError:
        groups = []
    return groups

def save_groups(groups):
    """
    Save group usernames to the 'groups.json' file.
    """
    with open("groups.json", "w") as file:
        json.dump(groups, file, indent=4)

def add_group(group_username):
    """
    Add a group username to the list and save it.
    """
    groups = load_groups()
    if group_username not in groups:
        groups.append(group_username)
        save_groups(groups)
        return f"Group '{group_username}' has been added successfully!"
    else:
        return f"Group '{group_username}' is already stored."

def remove_group(group_username):
    """
    Remove a group username from the list and save it.
    """
    groups = load_groups()
    if group_username in groups:
        groups.remove(group_username)
        save_groups(groups)
        return f"Group '{group_username}' has been removed successfully!"
    else:
        return f"Group '{group_username}' is not in the list."

def list_groups():
    """
    List all monitored groups.
    """
    groups = load_groups()
    if groups:
        return "Monitored Groups:\n" + "\n".join(f"- {group}" for group in groups)
    else:
        return "No groups are currently monitored."

def get_help():
    """
    Return the list of all available commands and their descriptions.
    """
    return (
    "🔧 **Commands:**\n\n"
    "🟢 `/addgroup` - Add group\n\n"
    "🔴 `/removegroup` - Remove group\n\n"
    "📂 `/listgroups` - Monitored groups\n\n"
    "❔ `/help` - Help\n\n"
    "💡 Message me for GPT responses!"
)

async def main():
    # Create the Telegram Client for your user account
    async with TelegramClient('anon', API_ID, API_HASH) as client:

        # Log in with the phone number
        print("Connecting to Telegram...")
        await client.start(phone=PHONE_NUMBER)
        print("Connected!")

        # In-memory cache of monitored groups
        monitored_groups = set(load_groups())

        # Event handler for new messages
        @client.on(events.NewMessage)
        async def handler(event):
            nonlocal monitored_groups  # Access the shared group list
            chat = await event.get_chat()
            group_username = chat.username

            # Check if the message is a command from a private chat
            if event.is_private:
                user_message = event.message.message.strip()
                sender_id = event.sender_id  # Get the sender's Telegram user ID

                # Restrict owner-only commands
                if user_message.lower().startswith("/addgroup ") or user_message.lower().startswith("/removegroup "):
                    if sender_id != OWNER_ID:  # Replace OWNER_ID with the actual owner's ID in config.py
                        await event.reply("You are not authorized to perform this action.")
                        return

                # Add a group command
                if user_message.lower().startswith("/addgroup "):
                    group_to_add = user_message[10:].strip()
                    response = add_group(group_to_add)
                    monitored_groups.add(group_to_add)  # Update in-memory cache
                    await event.reply(response)

                # Remove a group command
                elif user_message.lower().startswith("/removegroup "):
                    group_to_remove = user_message[13:].strip()
                    response = remove_group(group_to_remove)
                    monitored_groups.discard(group_to_remove)  # Update in-memory cache
                    await event.reply(response)

                # List all groups command
                elif user_message.lower().startswith("/listgroups"):
                    response = list_groups()
                    await event.reply(response)

                # Help command
                elif user_message.lower().startswith("/help"):
                    response = get_help()
                    await event.reply(response)

                # General GPT query
                else:
                    gpt_response = get_chat_completion(user_message)
                    await event.reply(f"\n{gpt_response}")

            # Respond only to messages in monitored groups
            elif group_username in monitored_groups:
                user_message = event.message.message.strip()
                gpt_response = get_chat_completion(user_message)
                await event.reply(f"\n{gpt_response}")

        print("Userbot is running... (Private commands and monitored groups only)")
        await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
