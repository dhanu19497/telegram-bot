import os
import re
import gdown
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("7845323504:AAGiF7f_8msiLhYgtq3LNeIPzcZjjgDyr3s")

# Initialize bot and dispatcher
bot = Bot(token="7845323504:AAGiF7f_8msiLhYgtq3LNeIPzcZjjgDyr3s")
dp = Dispatcher()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Directory to store downloaded files
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Function to extract Google Drive file ID
def extract_drive_id(url):
    match = re.search(r"(?:drive\.google\.com\/file\/d\/|id=)([\w-]+)", url)
    return match.group(1) if match else None

# Telegram bot handler for /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hello! Send me a Google Drive link, and I'll download the file for you.")

# Telegram bot handler for downloading files
@dp.message()
async def download_drive_file(message: Message):
    url = message.text.strip()
    file_id = extract_drive_id(url)

    if not file_id:
        await message.answer("Invalid Google Drive link. Please send a valid **public** Google Drive link.")
        return

    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.file")
        gdown.download(f"https://drive.google.com/uc?id={file_id}", file_path, quiet=False)

        # Send file to Telegram
        with open(file_path, "rb") as file:
            await message.answer_document(file)

        # Cleanup: Delete file after sending
        os.remove(file_path)

    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("Failed to download the file. Make sure the link is public.")

# Main function to run bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
