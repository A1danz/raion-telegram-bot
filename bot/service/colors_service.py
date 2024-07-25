from bot.models import Color
from asgiref.sync import sync_to_async


async def color_by_name(name):
    return await Color.objects.aget(name=name)


async def get_colors_by_thing(thing):
    result = await sync_to_async(Color.objects.filter)(
        thing=thing
    )

    return await sync_to_async(list)(result)
