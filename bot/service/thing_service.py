from django.db import transaction
from asgiref.sync import sync_to_async

from bot.models import Thing
from bot.tg_model.tg_models import TgThingModel, TgPhotoModel
from bot.service.category_service import *
from bot.service.colors_service import *
from bot.service.photo_service import *
from bot.service.visibility_types_service import *


async def save_thing(thing: TgThingModel):
    thing_object = await Thing.objects.acreate(
        name=thing.name,
        category=await category_by_name(thing.category),
        cost=int(thing.cost),
        description=thing.description,
        visibility_type=await get_visible_type()
    )

    for color in thing.colors:
        await thing_object.colors.aadd(await color_by_name(color))

    await add_photos_to_thing(thing_object, thing.photos)

    return thing_object


async def get_by_article(article: int):
    try:
        thing = await Thing.objects.aget(id=article)
    except Thing.DoesNotExist:
        return None

    return await __map_to_tg_model(thing)


async def search_with_offset(query, offset, limit):
    searched_result = await sync_to_async(Thing.objects.search)(
        query=query,
        visibility_type=await get_visible_type(),
        offset=offset,
        limit=limit
    )
    searched_result = await sync_to_async(list)(searched_result)
    return [await __map_to_tg_model(thing) for thing in searched_result]


async def __map_to_tg_model(thing):
    photos = await get_photos_by_thing(thing)
    colors = await get_colors_by_thing(thing)

    return TgThingModel(
        photos=[TgPhotoModel(photo.file_id, photo.file_path, photo.url) for photo in photos],
        colors_list=[color.name for color in colors],
        name=thing.name,
        category=await get_category_by_thing(thing),
        description=thing.description,
        cost=str(thing.cost),
        thing_id=thing.id
    )
