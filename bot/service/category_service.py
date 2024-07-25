from bot.models import Category
from asgiref.sync import sync_to_async


async def category_by_name(name):
    return await Category.objects.aget(name=name)


async def get_category_by_thing(thing):
    return await Category.objects.aget(thing=thing)
