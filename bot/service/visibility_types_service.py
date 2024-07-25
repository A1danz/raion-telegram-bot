from bot.models import VisibilityType
from bot.dict_names.visibility_types import *
from asgiref.sync import sync_to_async


async def get_visible_type():
    return await VisibilityType.objects.aget(
        name=VISIBLE_TYPE
    )


async def get_hide_type():
    return await VisibilityType.objects.aget(
        name=HIDE_TYPE
    )
