import sys
import aiohttp
import asyncio
from loguru import logger
from src.config import TG_ID, TGBOT_TOKEN

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TGBOT_TOKEN}/sendMessage"

async def send_log_to_telegram(message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(TELEGRAM_API_URL, data={'chat_id': TG_ID, 'text': message}) as response:
                if response.status != 200:
                    logger.error(f"Failed to send log to Telegram: {await response.text()}")
        except Exception as e:
            logger.error(f"Failed to send log to Telegram: {e}")

# Создайте обертку для асинхронного вызова
def send_log(message):
    loop = asyncio.get_event_loop()
    loop.create_task(send_log_to_telegram(message))

def logging_setup():
    format_info = "<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | <level>{message}</level>"
    logger.remove()

    logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")
    logger.add("hh-test.log", rotation="50 MB", compression="zip", format=format_info, level="TRACE")
    
    logger.add(
        send_log,  # Здесь вы передаете функцию send_log
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        filter=lambda record: record['level'].name == 'INFO'
    )
            
logging_setup()