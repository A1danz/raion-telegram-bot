import logging

import telebot.types
from django.conf import settings
import asyncio
from asgiref.sync import sync_to_async
import traceback
from datetime import datetime

from telebot.async_telebot import AsyncTeleBot

from bot.typography.texts import *
from bot.utils.thing_options import *
from bot.state.state import *
from bot.keyboards.keyboards_storage import *
from bot.service.thing_service import *


bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode="HTML")

LOGGER = logging.getLogger(__name__)

user_states = dict()

INLINE_QUERY_LIMIT = 10


def log_info_about_message(message):
    LOGGER.info(f"{message.from_user.username}: {message.text}")


def log_info_about_call(call):
    LOGGER.info(f"{call.message.from_user.username}: ${call.data}")


# Handle 'cancel' inline btn
@bot.callback_query_handler(func=lambda call: call.data == CANCEL_NEW_PRODUCT_CALL)
async def handle_cancel_new_product(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
    message = call.message
    if call.from_user.id in user_states:
        user_states.pop(call.from_user.id)
    await bot.delete_message(message.chat.id, message.message_id)


# Handle 'add thing' inline btn
@bot.callback_query_handler(func=lambda call: call.data == ADD_THING_CALL)
async def handle_add_thing(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
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
            await bot.edit_message_text(
                THING_SAVING_TEXT,
                chat_id=call.message.chat.id,
                message_id=call.message.id
            )
            thing = await save_thing(
                thing=user_states[call.from_user.id].tg_model
            )
            await bot.edit_message_text(get_thing_article(thing.id), call.message.chat.id, call.message.id)
            user_states.pop(call.from_user.id, None)
    except Exception as e:
        LOGGER.error(traceback.format_exc())


# Handle 'make order' inline btn
@bot.callback_query_handler(func=lambda call: call.data == MAKE_ORDER_CALL)
async def handle_make_order(call: CallbackQuery):
    log_info_about_call(call)
    ordered_time = datetime.now()
    article = call.message.text.split("Артикул: ")[-1]

    thing = await get_by_article(int(article))
    await bot.send_message(
        chat_id=settings.ADMIN_ID,
        text=new_order_for_admin_text(
            username=call.from_user.username,
            name=call.from_user.first_name,
            thing_name=thing.name,
            article=article,
            time=ordered_time.strftime("%d.%m.%Y %H:%M")
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
        text=order_maked_text(settings.ADMIN_USERNAME),
        reply_markup=None
    )


# Handle 'delete thing' btn
@bot.callback_query_handler(func=lambda call: call.data == DELETE_THING_CALL)
async def handle_delete_thing_call(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
    article = call.message.text.split("Артикул: ")[-1].strip()

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=you_want_delete_thing_text(article),
        reply_markup=delete_thing_keyboard
    )


# Handle 'yes delete thing' btn
@bot.callback_query_handler(func=lambda call: call.data == YES_DELETE_CALL)
async def handle_yes_delete_thing(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
    article = call.message.text.split("Артикул: ")[-1].strip()

    delete_result = await delete_thing_by_id(int(article))
    text = thing_not_deleted_text(article)
    if delete_result:
        text = thing_successful_deleted_text(article)

    await bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=None
    )


# Handle 'no, cancel delete thing' btn
@bot.callback_query_handler(func=lambda call: call.data == NO_CANCEL_DELETE_CALL)
async def handle_no_cancel_delete_thing(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
    article = call.message.text.split("Артикул: ")[-1].strip()

    await bot.edit_message_text(
        text=edit_thing_text(article),
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=editing_options_thing_keyboard
    )


# Handle 'edit thing' btn
@bot.callback_query_handler(func=lambda call: call.data == EDITING_OPTIONS_THING_CALL)
async def handle_edit_thing_call(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
    article = call.message.text.split("Артикул: ")[-1].strip()

    tg_model = await get_by_article(int(article))
    user_states[call.from_user.id] = EditThingState(
        call.from_user.id,
        tg_model
    )
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=EDIT_THING_TEXT,
        reply_markup=editing_thing_keyboard
    )


# Handle 'not save edits thing' btn
@bot.callback_query_handler(func=lambda call: call.data == NOT_SAVE_EDITS_THING_CALL)
async def handle_not_save_edits_btn(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
    if call.from_user.id in user_states:
        user_states.pop(call.from_user.id)

    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=EDITS_NOT_SAVED_TEXT,
        reply_markup=None
    )


# Handle 'save edits' btn
@bot.callback_query_handler(func=lambda call: call.data == SAVE_EDITS_THING_CALL)
async def handle_save_edits_btn(call: CallbackQuery):
    if str(call.from_user.id) not in settings.WHITE_LIST:
        return

    log_info_about_call(call)
    if call.from_user.id in user_states:
        state = user_states[call.from_user.id]

        saved = True
        validation_steps = state.tg_model.get_required_not_filled_options()
        if len(validation_steps) != 0:
            return await bot.send_message(
                chat_id=call.message.chat.id,
                text=get_thing_invalid_options_text(validation_steps)
            )
        print(state.need_save())
        if state.need_save():
            try:
                await edit_thing(state.tg_model)
            except Exception as ex:
                saved = False
                await bot.send_message(
                    chat_id=call.message.chat.id,
                    text=ERROR_EDITS_SAVING_TEXT
                )

                LOGGER.error(ex)
                LOGGER.error(traceback.format_exc())

        if saved:
            await bot.send_message(
                chat_id=call.message.chat.id,
                text=EDITS_SAVED_TEXT
            )


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message: Message):
    log_info_about_message(message)
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
    log_info_about_message(message)
    if str(user_id) not in settings.WHITE_LIST:
        await bot.reply_to(message, INVALID_COMMAND_TEXT)
        return

    user_states[user_id] = NewThingState(user_id)

    await bot.send_message(
        message.chat.id,
        NEW_PRODUCT_TEXT,
        reply_markup=cancel_new_product_keyboard
    )


# Handle '/list' command
@bot.message_handler(commands=['list'])
async def list_command(message: Message):
    log_info_about_message(message)
    user_id = message.from_user.id
    text = INVALID_COMMAND_TEXT

    if str(user_id) in settings.WHITE_LIST:
        if len(message.text.split()) > 1:
            await handle_list_command(message)
            return

        text = things_count_text(await get_things_count())

    await bot.send_message(
        chat_id=message.chat.id,
        text=text
    )


# Handle '/admin' command
@bot.message_handler(commands=['admin'])
async def handle_admin_command(message: Message):
    log_info_about_message(message)
    if str(message.from_user.id) in settings.WHITE_LIST:
        await bot.send_message(
            chat_id=message.chat.id,
            text=ADMIN_COMMANDS_TEXT
        )


# Handle text message
@bot.message_handler(func=lambda message: True)
async def handle_text_message(message: Message):
    log_info_about_message(message)
    if message.text.startswith("/"):
        await handle_commands_with_args(message)
        return

    user_id = message.from_user.id
    if str(user_id) in settings.WHITE_LIST and user_id in user_states:
        text = message.text
        state = user_states[message.from_user.id]

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
        if isinstance(state, NewThingState):
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
        elif isinstance(state, EditThingState):
            validation_steps = state.tg_model.get_validation_steps()
            text = ""
            if len(validation_steps) != 0:
                text = get_thing_invalid_options_text(validation_steps)
            else:
                text = EDIT_TAKEN_TEXT
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=editing_thing_keyboard
            )
    else:
        await bot.reply_to(message, INVALID_TEXT)


# Handle 'photo' message
@bot.message_handler(content_types=['photo'])
async def handle_photo(message: Message):
    log_info_about_message(message)
    user_id = message.from_user.id
    if str(user_id) in settings.WHITE_LIST and user_id in user_states:
        state: NewThingState = user_states[user_id]
        photo_file_id = message.photo[-1].file_id
        file_path = (await bot.get_file(photo_file_id)).file_path
        if isinstance(state, NewThingState):
            validation_steps = state.tg_model.get_validation_steps()
            if state.is_ready_to_set_photos() and len(validation_steps) == 0:
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
        elif isinstance(state, EditThingState):
            if state.media_group is None or state.media_group != message.media_group_id:
                state.tg_model.photos = []
                state.media_group = message.media_group_id

            state.tg_model.append_photo(photo_file_id, file_path)
            await set_last_photo_handler(len(state.tg_model.photos), state, message.chat.id)


# function for follow last photo in media group
async def set_last_photo_handler(current_size, state: NewThingState | EditThingState, chat_id):
    await asyncio.sleep(1)
    if current_size != len(state.tg_model.photos):
        return

    if isinstance(state, NewThingState):
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
    elif isinstance(state, EditThingState):
        await bot.send_message(
            chat_id=chat_id,
            text=PHOTOS_EDITED,
            reply_markup=editing_thing_keyboard
        )


# handle commands with args
async def handle_commands_with_args(message: Message):
    command_arr = message.text.split()
    if len(command_arr) >= 2:
        command = command_arr[0]
        if command == "/article":
            await handle_article_command(message)
        elif command == "/list":
            await handle_list_command(message)
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
            await send_make_order_message(message.chat.id, thing)


# handle list command
async def handle_list_command(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await bot.reply_to(message, INPUT_NUMERIC_RANGE)
        return

    range_value = args[1]
    try:
        range_value = int(range_value)
    except ValueError as err:
        await bot.reply_to(message, INPUT_NUMERIC_RANGE)
        return

    start = max(0, range_value - DEFAULT_RANGE_SIZE)
    end = range_value
    things = await get_things_by_range(start, end)
    if len(things) == 0:
        await bot.send_message(
            chat_id=message.chat.id,
            text=things_by_range_not_found(start, end)
        )
    else:
        await send_edit_things_messages(message, things)


async def send_edit_things_messages(message, things):
    for thing in things:
        await send_edit_thing_message(message, thing)


async def send_edit_thing_message(message, thing: TgThingModel):
    await send_thing_message(
        chat_id=message.chat.id,
        thing=thing
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=edit_thing_text(thing.id),
        reply_markup=editing_options_thing_keyboard
    )


# send make order message
async def send_make_order_message(chat_id, thing):
    await send_thing_message(chat_id, thing)

    await bot.send_message(
        chat_id,
        text=make_order_text(thing.id),
        reply_markup=make_order_keyboard
    )


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


# handle inline mode request
@bot.inline_handler(func=lambda query: len(query.query) > 0)
async def query_text(query: InlineQuery):
    LOGGER.info(f"INLINE_REQUEST[{query.from_user.username}]: {query.query}")
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
