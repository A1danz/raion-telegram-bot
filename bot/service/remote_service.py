from django.conf import settings
import requests
import asyncio
import aiohttp
import logging
from telebot.async_telebot import AsyncTeleBot

LOGGER = logging.getLogger(__name__)


async def upload_image_on_ibb(file_id, downloaded_file=None, attempt=1):
    from bot.raion_bot import bot

    ibb_url = "https://api.imgbb.com/1/upload"
    if downloaded_file is None:
        file = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file.file_path)

    timeout = aiohttp.ClientTimeout(total=8)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            data = {
                "key": settings.IBB_API_KEY,
                "image": downloaded_file
            }

            async with session.post(ibb_url, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['data']['url']
                else:
                    LOGGER.error(f"Bad response code on ibb: {response.status}")
    except Exception as ex:
        LOGGER.error(f"Exception during uploading on ibb: {ex}")

    if attempt < 4:
        LOGGER.error(f"Retry uploading on ibb: {attempt}")
        return await upload_image_on_ibb(file_id, downloaded_file, attempt + 1)
    else:
        LOGGER.error(f"Can't upload image to ibb with {attempt} attempts.")
        return None





