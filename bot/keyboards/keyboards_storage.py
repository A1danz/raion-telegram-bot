from telebot.types import *

CANCEL_NEW_PRODUCT_CALL = "cancel_new_product"
ADD_THING_CALL = "add_thing_to_catalog"
MAKE_ORDER_CALL = "buy_thing"
SEARCH_CALL = "search"
EDITING_OPTIONS_THING_CALL = "edit_thing"
DELETE_THING_CALL = "delete_thing"
YES_DELETE_CALL = "yes_delete"
NO_CANCEL_DELETE_CALL = "no_cancel_delete"
NOT_SAVE_EDITS_THING_CALL = "not_save_edits_thing_call"
SAVE_EDITS_THING_CALL = "save_edits_thing_call"


cancel_new_product_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
cancel_btn = InlineKeyboardButton(
        text="Отмена ❌",
        callback_data=CANCEL_NEW_PRODUCT_CALL
    )
cancel_new_product_keyboard.add(cancel_btn)

finished_adding_thing_keyboard = InlineKeyboardMarkup()
ok_btn = InlineKeyboardButton(
    text="Добавить ✅",
    callback_data=ADD_THING_CALL
)
finished_adding_thing_keyboard.add(ok_btn)
finished_adding_thing_keyboard.add(cancel_btn)

make_order_keyboard = InlineKeyboardMarkup()
make_order_btn = InlineKeyboardButton(
    text="Сделать заказ 📝",
    callback_data=MAKE_ORDER_CALL
)
make_order_keyboard.add(make_order_btn)

search_keyboard = InlineKeyboardMarkup()
search_btn = InlineKeyboardButton(
    text="🔎 Поиск по каталогу",
    switch_inline_query_current_chat="Футболка"
)
search_keyboard.add(search_btn)

editing_options_thing_keyboard = InlineKeyboardMarkup()
edit_thing_btn = InlineKeyboardButton(
    text="✏️ Изменить информацию",
    callback_data=EDITING_OPTIONS_THING_CALL
)
delete_thing_btn = InlineKeyboardButton(
    text="⛔️ Удалить товар",
    callback_data=DELETE_THING_CALL
)
editing_options_thing_keyboard.add(edit_thing_btn)
editing_options_thing_keyboard.add(delete_thing_btn)

delete_thing_keyboard = InlineKeyboardMarkup()
yes_delete_btn = InlineKeyboardButton(
    text="✅ Удалить",
    callback_data=YES_DELETE_CALL
)
no_cancel_delete_btn = InlineKeyboardButton(
    text="❌ Не удалять ",
    callback_data=NO_CANCEL_DELETE_CALL
)
delete_thing_keyboard.add(yes_delete_btn)
delete_thing_keyboard.add(no_cancel_delete_btn)

editing_thing_keyboard = InlineKeyboardMarkup()
not_save_edits_btn = InlineKeyboardButton(
    text="❌ Не сохранять изменения",
    callback_data=NOT_SAVE_EDITS_THING_CALL
)
save_edits_btn = InlineKeyboardButton(
    text="✅ Сохранить изменения",
    callback_data=SAVE_EDITS_THING_CALL
)
editing_thing_keyboard.add(save_edits_btn)
editing_thing_keyboard.add(not_save_edits_btn)



