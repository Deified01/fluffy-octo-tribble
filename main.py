import asyncio
import logging
import os
from telethon import events, TelegramClient
from telethon.sessions import StringSession

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_id = 8447214
api_hash = '9ec5782ddd935f7e2763e5e49a590c0d'
string_session = os.getenv("string")
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# Flag to control the on/off state
is_on = False

async def main():
    logger.info('''
 ___                   _______            _________________
|   |                /   ___   \         |______    _______|
|   |               /   /   \   \               |   |
|   |              /   /__ __\   \              |   |
|   |    ___      /   ________\   \             |   |
|   |___|   |    /   /         \   \      ______|   |______
\___________/   /___/           \___\    |_________________|
''')

async def send_riddle():
    while True:
        try:
            await client.send_message("@lustXcatcherrobot", "/riddle")
            # Rest of the riddle handling code
        except Exception as e:
            logger.error(f"Error sending riddle: {e}")

@client.on(events.NewMessage(from_users="@lustXcatcherrobot"))
async def handle_new_message(event):
    if event.buttons:
        logger.info("Received buttons, clicking on them...")
        tasks = [button.click() for row in event.buttons for button in row]
        await asyncio.gather(*tasks)

@client.on(events.NewMessage(pattern='/on'))
async def turn_on(event):
    if event.sender.username == '@y2god':
        global is_on
        is_on = True
        await event.respond("Switch is now on")
    else:
        await event.respond("You are not authorized to control the switch.")

@client.on(events.NewMessage(pattern='/off'))
async def turn_off(event):
    if event.sender.username == '@y2god':
        global is_on
        is_on = False
        await event.respond("Switch is now off")
    else:
        await event.respond("You are not authorized to control the switch.")

async def send_actions():
    async def send_propose():
        try:
            await client.send_message("@lustsupport", "/propose")
            logger.info("Sent /propose")
            await asyncio.sleep(600)  # 10 minutes
        except Exception as e:
            logger.error(f"Error sending /propose: {e}")

    async def send_tesure():
        try:
            await client.send_message("@lustsupport", "/tesure")
            logger.info("Sent /tesure")
            await asyncio.sleep(1800)  # 30 minutes
        except Exception as e:
            logger.error(f"Error sending /tesure: {e}")

    async def send_shunt():
        try:
            await client.send_message("@lustsupport", "/shunt")
            logger.info("Sent /shunt")
            await asyncio.sleep(60)  # 1 minute
        except Exception as e:
            logger.error(f"Error sending /shunt: {e}")

    async def send_sfight():
        try:
            await client.send_message("@lustsupport", "/sfight")
            logger.info("Sent /sfight")
            await asyncio.sleep(600)  # 10 minutes
        except Exception as e:
            logger.error(f"Error sending /sfight: {e}")

    while True:
        if is_on:
            await send_propose()
            await send_tesure()
            await send_shunt()
            await send_sfight()
        else:
            logger.info("Switch is off, not sending any actions")
            await asyncio.sleep(60)  # Wait for 1 minute before checking the switch again

if __name__ == "__main__":
    client.start()

    client.loop.create_task(send_actions())
    client.loop.create_task(send_riddle())
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
