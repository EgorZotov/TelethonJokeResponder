from modules.jokes import get_porutchik_joke 
from telethon import TelegramClient, events, sync
from dotenv import load_dotenv
import os

load_dotenv()
client = TelegramClient('session_name', os.getenv("TELEGRAM_APP_ID"), os.getenv("TELEGRAM_HASH"))
client.start()

@client.on(events.NewMessage)
async def handler(event):
    target_id = int(os.getenv("TARGET_ID"))
    if(event.message.from_id == target_id):
        print("Message from target")
        poruchik_joke = get_porutchik_joke()
        await event.respond("Ежедневная рубрика, анекдот про поручика\n\n" + poruchik_joke)
    
client.run_until_disconnected()


