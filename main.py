import asyncio
import logging
import os
import threading
from telethon import events, TelegramClient
from telethon.sessions import StringSession
import uvloop
from flask import Flask, request, jsonify

app = Flask(__name__)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
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

@app.route('/on', methods=['POST'])
def turn_on():
    global is_on
    is_on = True
    logger.info("Switch is now on")
    return jsonify({'status': 'on'})

@app.route('/off', methods=['POST'])
def turn_off():
    global is_on
    is_on = False
    logger.info("Switch is now off")
    return jsonify({'status': 'off'})

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

def run_flask_app():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    client.start()

    client.loop.create_task(send_actions())
    client.loop.create_task(send_riddle())
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
