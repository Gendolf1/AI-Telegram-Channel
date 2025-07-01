from telegram import Bot
import asyncio
import ollama
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
PROMPT = os.getenv("PROMPT")

async def send_post():
    try:
        model_list = ollama.list()
        if not any("llama3" in model.get("name", "") for model in model_list.get("models", [])):
            print("Model lama3 not found, loading starts...")
            ollama.pull("llama3")
            print("Model exelent download!")
        last_prompt="Начальное значение"
        response = ollama.generate(
            model="llama3",
            prompt=PROMPT.format(last_prompt=last_prompt),
        )
        last_prompt=response
        message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{response['response']}"
        
        bot = Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message)
        print(f"Message send! {datetime.now()}")
        
    except Exception as e:
        print(f"Errror: {e}")

async def main():
    while True:
        await send_post()
        await asyncio.sleep(60) 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n Bot stopped.")

