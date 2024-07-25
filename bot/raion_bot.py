import logging

import telebot.types
from django.conf import settings
import asyncio
from asgiref.sync import sync_to_async
import traceback

from telebot.async_telebot import AsyncTeleBot

from bot.typography.texts import *
from bot.utils.thing_options import *
from bot.state.state import NewThingState
from bot.keyboards.keyboards_storage import *
from bot.service.thing_service import *


bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode="HTML")

LOGGER = logging.getLogger(__name__)

user_states = dict()

INLINE_QUERY_LIMIT = 10


# Handle 'cancel' inline btn
@bot.callback_query_handler(func=lambda call: call.data == CANCEL_NEW_PRODUCT_CALL)
async def handle_cancel_new_product(call: CallbackQuery):
    message = call.message
    if call.from_user.id in user_states:
        user_states.pop(call.from_user.id)
    await bot.delete_message(message.chat.id, message.message_id)


# Handle 'add thing' inline btn
@bot.callback_query_handler(func=lambda call: call.data == ADD_THING_CALL)
async def handle_add_thing(call: CallbackQuery):
    try:
        await bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
        tg_model = user_states[call.from_user.id].tg_model

        not_filled_options = tg_model.get_required_not_filled_options()
        if len(not_filled_options) > 0:
            await bot.edit_message_text(
                text=get_product_not_filled_text(not_filled_options),
                chat_id=call.message.chat.id,
                message_id=call.message.id
            )
        else:
            thing = await save_thing(
                thing=user_states[call.from_user.id].tg_model
            )
            await bot.edit_message_text(get_thing_article(thing.id), call.message.chat.id, call.message.id)
            user_states.pop(call.from_user.id, None)
    except Exception as e:
        LOGGER.error(traceback.format_exc())


# Handle 'make order' inline btn
@bot.callback_query_handler(func=lambda call: call.data == MAKE_ORDER_CALL)
async def handel_make_order(call: CallbackQuery):
    article = call.message.text.split("Артикул: ")[-1]

    thing = await get_by_article(int(article))
    await bot.send_message(
        chat_id=settings.ADMIN_ID,
        text=new_order_for_admin_text(
            username=call.from_user.username,
            name=call.from_user.first_name,
            thing_name=thing.name,
            article=article
        )
    )

    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.id,
        reply_markup=None
    )

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=ORDER_MAKED,
        reply_markup=None
    )

    await bot.reply_to(call.message, ORDER_MAKED)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message: Message):
    LOGGER.info(f"message.from_user.id use {message.text}")
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=settings.HEADER_FILE_ID,
        caption=get_start_text(message.from_user.first_name),
        reply_markup=search_keyboard
    )
    # await bot.reply_to(message, get_start_text(message.from_user.first_name))


# Handle '/new' command
@bot.message_handler(commands=['new'])
async def new_product(message: Message):
    user_id = message.from_user.id
    LOGGER.info(f"{message.from_user.username}[{user_id}] try to use /new command")
    if str(user_id) not in settings.WHITE_LIST:
        await bot.reply_to(message, INVALID_COMMAND_TEXT)
        return

    user_states[user_id] = NewThingState(user_id)

    await bot.send_message(
        message.chat.id,
        NEW_PRODUCT_TEXT,
        reply_markup=cancel_new_product_keyboard
    )


# Handle text message
@bot.message_handler(func=lambda message: True)
async def handle_text_message(message: Message):
    if message.text.startswith("/"):
        await handle_commands_with_args(message)
        return

    user_id = message.from_user.id
    if str(user_id) in settings.WHITE_LIST and user_id in user_states:
        text = message.text
        state: NewThingState = user_states[message.from_user.id]

        lines = text.split("\n")
        thing_options = dict()
        for line in lines:
            splitted = line.split(":")
            if len(splitted) > 1:
                key = splitted[0].strip().lower()
                value = " ".join(splitted[1:]).strip()
                thing_options[key] = value

        state.tg_model.name = thing_options.get(NAME.lower(),  state.tg_model.name)
        state.tg_model.category = thing_options.get(CATEGORY.lower(),  state.tg_model.category)
        state.tg_model.colors = thing_options[COLORS.lower()].split(",") if COLORS.lower() in thing_options else state.tg_model.colors
        state.tg_model.description = thing_options.get(DESCRIPTION.lower(),  state.tg_model.description)
        state.tg_model.cost = thing_options.get(COST.lower(),  state.tg_model.cost)

        not_filled_options = state.tg_model.get_required_not_filled_options()
        if not state.is_ready_to_set_photos():
            await bot.send_message(
                message.chat.id,
                get_product_not_filled_text(not_filled_options),
                reply_markup=cancel_new_product_keyboard
            )
        else:
            validation_steps = state.tg_model.get_validation_steps()
            if len(validation_steps) != 0:
                await bot.send_message(
                    message.chat.id,
                    get_thing_invalid_options_text(validation_steps),
                    reply_markup=cancel_new_product_keyboard
                )
            else:
                await bot.send_message(
                    message.chat.id,
                    READY_TO_SET_PHOTOS_TEXT,
                    reply_markup=cancel_new_product_keyboard
                )
    else:
        await bot.reply_to(message, INVALID_TEXT)


# Handle 'photo' message
@bot.message_handler(content_types=['photo'])
async def handle_photo(message: Message):
    user_id = message.from_user.id
    if str(user_id) in settings.WHITE_LIST and user_id in user_states:
        state: NewThingState = user_states[user_id]
        validation_steps = state.tg_model.get_validation_steps()
        if state.is_ready_to_set_photos() and len(validation_steps) == 0:
            photo_file_id = message.photo[-1].file_id
            file_path = (await bot.get_file(photo_file_id)).file_path
            state.tg_model.append_photo(photo_file_id, file_path)
            await set_last_photo_handler(len(state.tg_model.photos), state, message.chat.id)
        else:
            if state.media_group is None or state.media_group != message.media_group_id:
                state.media_group = message.media_group_id
                await bot.send_message(
                    message.chat.id,
                    TOO_EARLY_SET_PHOTOS_TEXT
                )
                if not state.is_ready_to_set_photos():
                    not_filled_options = state.tg_model.get_required_not_filled_options()
                    await bot.send_message(
                        message.chat.id,
                        get_product_not_filled_text(not_filled_options)
                    )
                else:
                    await bot.send_message(
                        message.chat.id,
                        get_thing_invalid_options_text(validation_steps)
                    )


# function for follow last photo in media group
async def set_last_photo_handler(current_size, state: NewThingState, chat_id):
    await asyncio.sleep(1)
    if current_size != len(state.tg_model.photos):
        return

    card_txt = state.tg_model.get_thing_card_text()
    await bot.send_media_group(
        chat_id,
        [InputMediaPhoto(photo.file_id, card_txt if index == 0 else None) for index, photo in enumerate(state.tg_model.photos)],
    )
    await bot.send_message(
        chat_id,
        FINISHED_ADDING_THING_TEXT,
        reply_markup=finished_adding_thing_keyboard
    )


# handle commands with args
async def handle_commands_with_args(message: Message):
    command_arr = message.text.split()
    if len(command_arr) >= 2:
        command = command_arr[0]
        if command == "/article":
            await handle_article_command(message)
            return

    await bot.reply_to(message, INVALID_TEXT)


# handle article command
async def handle_article_command(message: Message):
    article_arr = message.text.split()
    if len(article_arr) < 2:
        await bot.reply_to(message, INPUT_ARTICLE)
    else:
        article = article_arr[1]
        if not article.isdigit() or int(article) < 0:
            await bot.reply_to(message, article_must_be_digit(article))
            return

        article_value = int(article)
        thing = await get_by_article(article_value)
        if thing is None:
            await bot.reply_to(message, article_not_found(article))
        else:
            await send_thing_message(message.chat.id, thing)


# send message with thing
async def send_thing_message(chat_id, thing):
    thing_text = thing.get_thing_card_text()
    if thing.photos is None or len(thing.photos) == 0:
        await bot.send_message(chat_id, thing_text)
    else:
        await bot.send_media_group(
            chat_id,
            [
                InputMediaPhoto(photo.file_id, thing_text if ind == 0 else None)
                for ind, photo in enumerate(thing.photos)
            ],
        )

    await bot.send_message(
        chat_id,
        text=make_order_text(thing.id),
        reply_markup=make_order_keyboard
    )


# handle inline mode request
@bot.inline_handler(func=lambda query: len(query.query) > 0)
async def query_text(query: InlineQuery):
    offset = int(query.offset) if query.offset else 0
    things = await search_with_offset(
        query=query.query,
        offset=offset,
        limit=INLINE_QUERY_LIMIT
    )

    next_offset = None
    if len(things) == INLINE_QUERY_LIMIT:
        next_offset = offset + INLINE_QUERY_LIMIT

    result_arr = []
    LOGGER.info(things)
    for thing in things:
        thing_photo_url = settings.LOGO_URL if thing.photos is None or len(thing.photos) == 0 or thing.photos[0].url is None \
            else thing.photos[0].url
        result_arr.append(InlineQueryResultArticle(
            id=thing.id,
            title=thing.get_name_with_price(),
            description=thing.description,
            input_message_content=InputTextMessageContent(f"/article {thing.id}"),
            thumbnail_url=thing_photo_url
        ))

    await bot.answer_inline_query(query.id, result_arr)
