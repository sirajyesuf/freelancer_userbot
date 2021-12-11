from os import truncate
from telethon import TelegramClient, events, client
import logging
import config
import db
import json
from telethon.tl.types import Channel, UserStatusOnline, UserStatusOffline
from twilio_client import send_sms

# Enable logging
log_format = logging.Formatter(
    "%(asctime)s - [%(name)s] [%(levelname)s]  %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('telethon').setLevel(logging.CRITICAL)

file_logger = logging.FileHandler("freelancer_userbot.log")
file_logger.setLevel(logging.INFO)
file_logger.setFormatter(log_format)
logger.addHandler(file_logger)

console_logger = logging.StreamHandler()
console_logger.setFormatter(log_format)
console_logger.setLevel(logging.ERROR)
logger.addHandler(console_logger)

# create the client
client = TelegramClient(api_id=config.API_ID,
                        api_hash=config.API_HASH, session='freelanceruserbot')

with open('db.json', 'r') as f:
    keywords = json.load(f)['keywords']
    f.close()


async def filter_job_post(job):
    hastag = "#software"
    if(hastag in job and [k for k in keywords if k in job]):
        return True


@client.on(events.NewMessage(chats=int(config.FREELANCE_ETHIOPIA_CHANNEL_ID)))
async def freelance_ethiopia_channel(event):
    channel = await client.get_entity(int(config.FREELANCE_ETHIOPIA_CHANNEL_ID))
    url = f"https://t.me/{channel.username}/{event.message.id}"
    job = event.text.replace("\n", "").strip()
    if(await filter_job_post(job)):
        me = await client.get_me()
        account = await client.get_entity(me.id)
        for i in event.text.split("\n"):
            if("description" in i.lower()):
                job_description = i

        if(isinstance(account.status, UserStatusOffline)):
            await send_sms(me, job_description, url)
        if(isinstance(account.status, UserStatusOnline)):
            await send_sms(me, job_description, url)


client.start()
logger.info('Freelancer Bot ON 🚀 ')
print("Freelancer Bot ON 🚀 ")
client.run_until_disconnected()
