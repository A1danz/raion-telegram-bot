from django.db import transaction
from asgiref.sync import sync_to_async

from bot.models import Thing
from bot.tg_model.tg_models import TgThingModel, TgPhotoModel
from bot.service.category_service import *
from bot.service.colors_service import *
from bot.service.photo_service import *
from bot.service.visibility_types_service import *


DEFAULT_RANGE_SIZE = 10


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


async def get_model_by_id(id: int):
    try:
        return await Thing.objects.aget(id=id)
    except Thing.DoesNotExist:
        return None


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


async def get_things_count():
    return await Thing.objects.acount()


async def get_things_by_range(start, end):
    range_result = await sync_to_async(Thing.objects.filter)(
        id__range=(start, end)
    )

    range_result = await sync_to_async(list)(range_result)
    return [await __map_to_tg_model(thing) for thing in range_result]


async def delete_thing_by_id(id):
    try:
        object = await Thing.objects.aget(id=id)
        await sync_to_async(object.delete)()
        return True
    except Thing.DoesNotExist:
        return False


async def edit_thing(edited_thing: TgThingModel):
    thing_id = edited_thing.id
    thing = await get_model_by_id(int(thing_id))
    thing_tg_model: TgThingModel = await __map_to_tg_model(thing)
    if thing is None:
        return

    thing.name = edited_thing.name
    if thing_tg_model.category != edited_thing.category:
        thing.category = await category_by_name(edited_thing.category)

    # colors
    thing.cost = int(edited_thing.cost)
    thing.description = edited_thing.description
    if thing_tg_model.colors != edited_thing.colors:
        new_colors = [await color_by_name(color) for color in edited_thing.colors]
        await sync_to_async(thing.colors.set)(new_colors)

    old_photos = await get_photos_by_thing(thing)
    if thing_tg_model.photos != edited_thing.photos:
        for photo in old_photos:
            await photo.adelete()

        await add_photos_to_thing(thing, edited_thing.photos)

    await thing.asave()


async def __map_to_tg_model(thing):
    photos = await get_photos_by_thing(thing)
    colors = await get_colors_by_thing(thing)
    category = await get_category_by_thing(thing)

    return TgThingModel(
        photos=[TgPhotoModel(photo.file_id, photo.file_path, photo.url) for photo in photos],
        colors_list=[color.name for color in colors],
        name=thing.name,
        category=category.name,
        description=thing.description,
        cost=str(thing.cost),
        thing_id=thing.id
    )
