import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from telethon import utils
from telethon import functions

# Getting the api id and api hash from the .env file
# The .env file should be in the same directory as the script
# Get the api id and api hash from https://my.telegram.org
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


# The name of the group chat you want to get the members from and the date limit
target_group_name = ''
day_limit = 21
month_limit = 8
year_limit = 2024 


async def main():

    client = TelegramClient('anon', api_id, api_hash)
    datetime_limit = datetime(year_limit, month_limit, day_limit, tzinfo=timezone.utc)

    await client.start()
    chats = await client.get_dialogs()
    group_chat = list(filter(lambda chat: chat.name == target_group_name, chats))[0]
    all_members = await client.get_participants(group_chat)
    members_dict_id_to_username_name = dict()
    for member in all_members:
        members_dict_id_to_username_name[member.id] = [member.username, member.first_name]

    async for message in client.iter_messages(group_chat):
        if datetime_limit <= message.date:
            if message.sender_id in members_dict_id_to_username_name:
                del members_dict_id_to_username_name[message.sender_id]
            if message.reactions:
                for reaction in message.reactions.recent_reactions:
                    if reaction.peer_id in members_dict_id_to_username_name:
                        del members_dict_id_to_username_name[reaction.peer_id]
        break
    for member_id in members_dict_id_to_username_name: 
        print(members_dict_id_to_username_name[member_id]) 


asyncio.run(main())

