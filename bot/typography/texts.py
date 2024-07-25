INVALID_COMMAND_TEXT = "Комманда не распознана."
NEW_PRODUCT_TEXT = """
Вы выбрали функцию добавления товара. В следующем сообщении отправьте информацию о товаре в следующем формате:
Название: «ne ochen’» tee
Категория: Футболка
Цвета: белый,черный
Цена: 2250
Описание: не очень

Если вы передумали - нажмите на кнопку ниже.
<code>
Название:
Категория: 
Цвета:
Цена:
Описание: 
</code>  
"""
READY_TO_SET_PHOTOS_TEXT = "Отлично! Теперь пора загрузить фотографиии. В следующем сообщении прикрепите от 1 до 10 фотографий."
TOO_EARLY_SET_PHOTOS_TEXT = "🚫 Слишком рано загружать фото для товара. Сначала заполните информацию о нем."
FINISHED_ADDING_THING_TEXT = "Информация о товаре загружена.\nВыше вы можете увидеть, как он будет выглядеть.\nПодтвердите добавление в каталог:"
INVALID_TEXT = "Я вас не понял. Для ознакомления с функционалом напишите /help."
INPUT_ARTICLE = "Пожалуйста, введите артикул."
ORDER_MAKED = "✅ Вы успешно сделали заказ! В ближайшее время с вами свяжется менеджер."


def get_start_text(username):
    return """
👋 Привет, <b>{}</b>!
👕 Это чат-бот Raion.
🛍 Здесь вы можете посмотреть каталог наших товаров и приобрести нужную вещь.
📈 Команды:
@raion_clothes_bot "футболка" - поиск товаров по запросу
/article 52 - информация о товаре по артиклю
/help - если вы что-то забыли, всегда можете написать эту команду

⬇️ Для поиска вы можете использовать меню ⬇️
""".format(username)


def get_product_not_filled_text(not_filled_options):
    return """
Вы не заполнили все поля для нового товара:
<i>
{}
</i>
Пожалуйста, заполните их.
""".format("\n".join(not_filled_options))


def get_thing_invalid_options_text(steps_to_fix):
    return f"Вы неправильно заполнили некоторые поля. Исправьте ошибки, согласно следующим пунктам:\n\n<b>{'\n'.join(steps_to_fix)}</b>"


def get_success_new_thing_text(thing_text):
    return "Вы успешно загрузили информацию о товаре, он будет выглядеть следующим образом:\n\n<blockquote>{}</blockquote>".format(thing_text)


def get_thing_article(article):
    return f"Товар успешно добавлен! <b>Артикул: {article}</b>"


def article_must_be_digit(article):
    return f"<b>{article}</b> - должен быть числовым значением."


def article_not_found(article):
    return f"<b>{article}</b> - по этому артикулу ничего не найдено."


def new_order_for_admin_text(username, name, thing_name, article):
    return f"🆕 Новый заказ! 🆕\n<b>Пользователь</b> - @{username}.\n<b>Имя</b> - {name}\n<b>Товар:</b> {thing_name}\n<b>Артикул товара</b> - {article}."


def make_order_text(article):
    return f'Хотите сделать заказ по данному товару?\n\n<span class="tg-spoiler">Артикул: {article}</span>'


