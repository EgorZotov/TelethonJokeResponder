from modules.jokes import get_porutchik_joke 
from telethon import TelegramClient, events, sync
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB('db.json')
User = Query()
target_users = os.getenv("TARGET_USERS").split(",")

load_dotenv()
client = TelegramClient('session_name', os.getenv("TELEGRAM_APP_ID"), os.getenv("TELEGRAM_HASH"))
client.start()

@client.on(events.NewMessage)
async def handler(event):
    from_id = str(event.message.from_id) 
    if from_id in target_users:
        print("Message from target")
        founded_users = db.search(User.id == from_id)
        print(founded_users)
        if founded_users:
            print("User found", founded_users)
            print("Date of last message", datetime.fromtimestamp(founded_users[0]["last_message_date"]))
            last_message_date = datetime.fromtimestamp(founded_users[0]["last_message_date"])
            now = datetime.today()
            minutes_diff = int((now - last_message_date).total_seconds()/60)
            print("MINUTES DIFF", minutes_diff)
            if minutes_diff > int(os.getenv("COOLDOWN_MINUTES")):
                print("SENDING JOKE....")
                db.update({"last_message_date": now.timestamp()}, User.id == from_id)
                poruchik_joke = get_porutchik_joke()
                await event.respond("Ежедневная рубрика, анекдот про поручика\n\n" + poruchik_joke)
        else:
            print("Need to insert user", type(datetime.today().timestamp()), datetime.today().timestamp())
            db.insert({"id": from_id, "last_message_date": datetime.today().timestamp()})

    
client.run_until_disconnected()


