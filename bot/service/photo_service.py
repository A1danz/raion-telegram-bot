from bot.models import Photo
from bot.service.remote_service import *
from asgiref.sync import sync_to_async


async def add_photos_to_thing(thing, photos):
    for photo in photos:
        await add_photo_to_thing(thing, photo)


async def add_photo_to_thing(thing, photo):
    await Photo.objects.acreate(
        thing=thing,
        file_id=photo.file_id,
        file_path=photo.file_path,
        url=await upload_image_on_ibb(photo.file_id)
    )


async def get_photos_by_thing(thing):
    result = await sync_to_async(Photo.objects.filter, thread_sensitive=True)(thing=thing)
    return await sync_to_async(list)(result)
