from telebot.types import *

CANCEL_NEW_PRODUCT_CALL = "cancel_new_product"
ADD_THING_CALL = "add_thing_to_catalog"
MAKE_ORDER_CALL = "buy_thing"
SEARCH_CALL = "search"

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
