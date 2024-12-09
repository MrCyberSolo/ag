from messages import HINDI_MESSAGE, ENGLISH_MESSAGE
import asyncio
from datetime import datetime
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER
from groups import GROUPS
from telethon.errors.rpcerrorlist import SlowModeWaitError, UsernameInvalidError

async def send_periodic_messages(client, group_name):
    try:
        group = await client.get_entity(group_name)  # Get group entity
    except UsernameInvalidError:
        print(f"Invalid username or group not found: {group_name}")
        return
    except Exception as e:
        print(f"Unexpected error while fetching group entity: {e}")
        return

    toggle = True  # To alternate messages

    while True:
        try:
            # Refresh group entity to check slow mode status
            group = await client.get_entity(group_name)
            slow_mode_delay = getattr(group, 'slowmode_seconds', 0)

            if slow_mode_delay > 0:
                print(f"Slow mode active in {group_name}. Waiting for {slow_mode_delay} seconds.")
                await asyncio.sleep(slow_mode_delay + 1)
                continue

            # Choose message based on toggle
            message = HINDI_MESSAGE if toggle else ENGLISH_MESSAGE
            toggle = not toggle  # Alternate for next iteration

            # Send the message
            await client.send_message(group, message)
            print(f"Message sent to {group_name} at {datetime.now()}")

            # Wait before sending the next message
            await asyncio.sleep(60)

        except SlowModeWaitError as e:
            print(f"Slow mode active in {group_name}. Retrying in {e.seconds} seconds.")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error in {group_name}: {e}")
            break

async def validate_groups(client, groups):
    """Validate group names and return valid ones."""
    valid_groups = []
    for group_name in groups:
        try:
            group = await client.get_entity(group_name)
            print(f"Valid group: {group_name} (ID: {group.id}, Title: {group.title})")
            valid_groups.append(group_name)
        except UsernameInvalidError:
            print(f"Invalid group: {group_name}")
        except Exception as e:
            print(f"Error while validating group {group_name}: {e}")
    return valid_groups

async def main():
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        await client.start(phone=PHONE_NUMBER)

        # Validate and filter groups
        valid_groups = await validate_groups(client, GROUPS)
        if not valid_groups:
            print("No valid groups to process.")
            return

        # Create tasks for each group
        tasks = [send_periodic_messages(client, group) for group in valid_groups]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
