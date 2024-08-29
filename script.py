import os
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from telethon import utils
from telethon import functions

@dataclass
class UserInfo:
    participated: bool 
    username: str
    name: str

async def main():

    if load_dotenv():
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
    else:
        print('You have no .env file, one will be created to store your Telegram app data for future use.')
        with open('.env', 'w') as file:
            api_id = input('Please enter your API id\n')
            api_hash = input('Please enter your API hash\n')
            file.writelines(f'API_ID = {api_id}\n', f'API_HASH = {api_hash}\n')
    client = TelegramClient('anon', api_id, api_hash)
    target_group_name = input('Please enter the group name you would like me to scan.\n--> ')
    print('Up until when would you like me to scan?', end=' ')
    year_limit = int(input('Please enter the year.\n--> ')) 
    month_limit = int(input('Please enter the month.\n--> ')) 
    day_limit = int(input('Please enter the day.\n--> ')) 
    datetime_limit = datetime(year_limit, month_limit, day_limit, tzinfo=timezone.utc)

    await client.start()
    chats = await client.get_dialogs()
    group_chat = list(filter(lambda chat: chat.name.startswith(target_group_name), chats))[0]
    all_members = await client.get_participants(group_chat)
    members_dict_id_to_userinfo = dict()
    for member in all_members:
        members_dict_id_to_userinfo[member.id] = UserInfo(False, member.username, member.first_name)

    async for message in client.iter_messages(group_chat):
        if datetime_limit <= message.date:
            members_dict_id_to_userinfo[message.sender_id].participated = True
            if message.reactions:
                for reaction in message.reactions.recent_reactions:
                    members_dict_id_to_userinfo[reaction.peer_id.user_id].participated = True
        else:
            break
    for member_id in members_dict_id_to_userinfo: 
        if not members_dict_id_to_userinfo[member_id].participated:
            print(f'{members_dict_id_to_userinfo[member_id].username}, {members_dict_id_to_userinfo[member_id].name}')


asyncio.run(main())

