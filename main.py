import asyncio
import logging
import re
import os
import threading
from telethon import events, TelegramClient, functions
from telethon.errors import MessageIdInvalidError, MessageNotModifiedError, StartParamInvalidError
from telethon.sessions import StringSession
import uvloop
from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World'

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
api_id = 8447214
api_hash = '9ec5782ddd935f7e2763e5e49a590c0d'
string_session = "1BVtsOL8Bu6rsW9suHSYWsIPEM4qMHKpxSSexN5k5qmUSmCdg9Sp5WY1ebPaZuVLUFDCCWfY3AVTm9whUAap29jx_nyWuqJ5Kb0317BeO0E9toWbf57pCbq-QZ3hVJvbzpdKt_6AXdVW7V-WsppkpsTN9EkDtufc22NQWsICVNJSTZ0xVi0V6Te7FinKkYdaLvYa4uQs418yHy0hmW05Gu9hlDgzltURzC-NV-K3Hn5HifVswtVk7i1SUcP5XZ8KJKC_4m68BpAH0Z6JA2a3_NDAXrZpMrBfV-AA_MYCjZzGWYdyTWaZ0EGrxOCet9tAOdBU2fuad3XDOrd0CF1uhGSLICUt2L3E="
stvring_session = os.getenv("string")
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def send_riddle():
    while True:
        try:
            await client.send_message("@lustXcatcherrobot", "/riddle")
            response = await client.get_messages("@lustXcatcherrobot", limit=1)
            response_text = response[0].text
            logger.info(f"Received response: {response_text}")
            if "Please wait" in response_text:
                wait_time_match = re.search(r'Please wait (\d+) seconds', response_text)
                if wait_time_match:
                    wait_time = int(wait_time_match.group(1))
                    if wait_time == 0:
                        logger.info("Wait time is 0, sending immediately...")
                        continue  # Skip the sleep and send immediately
                    else:
                        logger.info(f"Waiting for {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
            else:
                logger.info("Waiting for 10 seconds (default)...")
                await asyncio.sleep(8)  # Default wait time if no specific wait time is found
        except Exception as e:
            logger.error(f"Error sending riddle: {e}")

@client.on(events.NewMessage(from_users="@lustXcatcherrobot"))
async def handle_new_message(event):
    if event.buttons:
        logger.info("Received buttons, clicking on them...")
        tasks = [button.click() for row in event.buttons for button in row]
        try:
            await asyncio.gather(*tasks)
        except StartParamInvalidError:
            logger.error("StartParamInvalidError occurred while clicking buttons, skipping")

@client.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    start_time = datetime.datetime.now()
    await event.respond('Pong!')
    end_time = datetime.datetime.now()
    ms = (end_time - start_time).microseconds / 1000
    await event.respond(f'Pong ({ms} ms)')

async def send_propose():
    while True:
        try:
            await asyncio.sleep(2)
            await client.send_message("@lustsupport", "/propose")
            logger.info("Sent /propose")
            await asyncio.sleep(600)  # 10 minutes
        except Exception as e:
            logger.error(f"Error sending /propose: {e}")

async def send_tesure():
    while True:
        try:
            await asyncio.sleep(5)
            await client.send_message("@lustsupport", "/tesure")
            logger.info("Sent /tesure")
            await asyncio.sleep(1800)  # 30 minutes
        except Exception as e:
            logger.error(f"Error sending /tesure: {e}")

async def send_shunt():
    while True:
        try:
            await asyncio.sleep(7)
            await client.send_message("@lustsupport", "/shunt")
            logger.info("Sent /shunt")
            await asyncio.sleep(60)  # 1 minute
        except Exception as e:
            logger.error(f"Error sending /shunt: {e}")

async def send_sfight():
    while True:
        try:
            await asyncio.sleep(9)
            await client.send_message("@lustsupport", "/sfight")
            logger.info("Sent /sfight")
            await asyncio.sleep(600)  # 10 minutes
        except Exception as e:
            logger.error(f"Error sending /sfight: {e}")

async def start_client():
    await client.start()

    # Define the chat entity of the "@lustXcatcherrobot" chat
    lustsupport_entity = await client.get_entity('lustXcatcherrobot')

    # Define a dictionary to store the start time of each message
    message_start_times = {}

    # Define the event handler
    @client.on(events.NewMessage(chats=lustsupport_entity))
    async def handler(event):
        # Store the start time of the message
        message_start_times[event.message.id] = asyncio.get_event_loop().time()

async def check_for_buttons():
    # Define the chat entity of the "@lustXcatcherrobot" chat
    lustsupport_entity = await client.get_entity('lustXcatcherrobot')

    # Define a dictionary to store the start time of each message
    message_start_times = {}

    while True:
        try:
            # Get the latest messages from the chat
            messages = await client.get_messages(lustsupport_entity, limit=10)
            for message in messages:
                # Store the start time of the message
                message_start_times[message.id] = asyncio.get_event_loop().time()
            # Wait for 1 second before checking for new messages
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Error getting messages: {e}")

        for message_id, start_time in list(message_start_times.items()):
            # Check if 20 seconds have passed since the message was received
            if asyncio.get_event_loop().time() - start_time > 20:
                # Remove the message from the dictionary
                del message_start_times[message_id]
            else:
                try:
                    # Get the latest message from the chat
                    latest_message = await client.get_messages(lustsupport_entity, ids=message_id)
                    if latest_message is not None:
                        # Check if the message has buttons
                        if latest_message.buttons:
                            logger.info(f"Message {message_id} has buttons:")
                            for row in latest_message.buttons:
                                for button in row:
                                    logger.info(f"  - {button.text}")
                                    try:
                                        await client(functions.messages.ClickMessageButtonRequest(
                                            peer=lustsupport_entity,
                                            msg_id=message_id,
                                            button=button
                                        ))
                                        logger.info(f"Clicked button: {button.text}")
                                    except StartParamInvalidError:
                                        logger.error(f"StartParamInvalidError occurred while clicking button: {button.text}")
                            logger.info(f"Message text: {latest_message.text}")
                        else:
                            logger.info(f"Message {message_id} does not have buttons")
                    else:
                        logger.info(f"Message {message_id} not found")
                except MessageIdInvalidError:
                    # If the message ID is invalid, remove it from the dictionary
                    del message_start_times[message_id]
                    logger.info(f"Message {message_id} is no longer valid")

async def schedule_tasks():
    # Define the chat entity of the "@lustXcatcherrobot" chat
    lustsupport_entity = await client.get_entity('lustXcatcherrobot')

    while True:
        try:
            await send_stour(lustsupport_entity)
            await asyncio.sleep(18000)  # 5 hours
        except Exception as e:
            logger.error(f"Error in scheduling tasks: {e}")

async def send_stour(chat_entity):
    try:
        await client.send_message(chat_entity, "/stour")
        logger.info("Sent /stour")
        response = await client.get_messages(chat_entity, limit=1)
        response_text = response[0].text
        if "Welcome to the slave Zone!" in response_text:
            logger.info("Received 'Welcome to the slave Zone!' message")
            await send_explore_command(chat_entity)
        elif "You are already in the slave zone!" in response_text:
            logger.info("Received 'You are already in the slave zone!' message")
            await send_explore_command(chat_entity)
        else:
            logger.info("Did not receive expected response")
    except Exception as e:
        logger.error(f"Error sending /stour: {e}")

async def send_explore_command(chat_entity):
    while True:
        try:
            await client.send_message(chat_entity, "/explore")
            logger.info("Sent /explore")
            response = await client.get_messages(chat_entity, limit=1)
            response_text = response[0].text
            if "You have reached your hunt limit." in response_text:
                logger.info("Received 'You have reached your hunt limit.' message, stopping /explore")
                break
            await asyncio.sleep(20)
        except MessageNotModifiedError:
            logger.info("Message not modified, skipping")
        except Exception as e:
            logger.error(f"Error sending /explore: {e}")

def run_flask_app():
    app.run(host='0.0.0.0', port=8080)

async def main_loop():
    await client.start()

    client.loop.create_task(send_propose())
    client.loop.create_task(send_tesure())
    client.loop.create_task(send_shunt())
    client.loop.create_task(send_sfight())
    client.loop.create_task(send_riddle())
    client.loop.create_task(start_client())
    client.loop.create_task(check_for_buttons())
    client.loop.create_task(schedule_tasks())
    await client.run_until_disconnected()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_loop())
