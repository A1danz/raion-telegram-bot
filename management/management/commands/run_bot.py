from django.core.management import BaseCommand
import asyncio

from bot.raion_bot import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        asyncio.run(bot.infinity_polling())
