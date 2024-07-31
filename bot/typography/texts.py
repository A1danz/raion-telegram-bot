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
ORDER_MAKED = "✅ Вы успешно сделали заказ! В ближайшее время с вами свяжется менеджер: @raionseller"
THING_SAVING_TEXT = "🔁 Происходит сохранение товара в базе данных..."
INPUT_NUMERIC_RANGE = "Введите число, которое соответсвует числовому диапазону.\n<b>Например:</b> /list 20 - будут выведены объекты с номерами 10-20"
EDIT_THING_TEXT = ("👌 Теперь вы можете изменить информацию о товаре. Как это сделать?\n"
                   "1️⃣ Если вы хотите изменить какие-либо характеристики, то просто отправьте в чат название и значние. "
                   "Например: \n<code>Цвета: черный\nКатегория: кепка</code>\n"
                   "2️⃣ Если вы хотите изменить фотографии, то просто отправьте их.\n"
                   "3️⃣ После того, как вы внесете все изменения нажмите на кнопку 'Сохранить изменения'")
EDITS_NOT_SAVED_TEXT = "👌 Все изменения успешно сброшены!"
ERROR_EDITS_SAVING_TEXT = "🚫 Не удалось сохранить изменения"
EDITS_SAVED_TEXT = "✅ Все изменения успешно сохранены!"
EDIT_TAKEN_TEXT = "👌 Изменение учтено!"
PHOTOS_EDITED = "🖼 Новые фотографии усешно прикреплены!"
ADMIN_COMMANDS_TEXT = ("<b>/new</b> - создать новый товар\n<b>/list</b> - получить количество товров\n"
                       "<b>/list 10</b> - получить первые 10 товаров из каталога\n\t❕<b>/list 50</b> - будут показаны товары из интервала 40 ➡️ 50")

def get_start_text(username):
    return """
👋 Привет, <b>{}</b>!
👕 Это чат-бот Raion.
🛍 Здесь вы можете посмотреть каталог наших товаров и приобрести нужную вещь.
📈 Команды:
@raion_clothes_bot футболка - поиск товаров по запросу
/article 52 - информация о товаре по артикулу
/help - если вы что-то забыли, всегда можете написать эту команду

⬇️ Для поиска вы можете использовать меню ⬇️
""".format(username)


def order_maked_text(manager_username):
    return f"✅ Вы успешно сделали заказ! В ближайшее время с вами свяжется менеджер: @{manager_username}"



def get_product_not_filled_text(not_filled_options):
    return """
Вы не заполнили все поля для нового товара:
<i>
{}
</i>
Пожалуйста, заполните их.
""".format("\n".join(not_filled_options))


def get_thing_invalid_options_text(steps_to_fix):
    return "Вы неправильно заполнили некоторые поля. Исправьте ошибки, согласно следующим пунктам:\n\n<b>{}</b>".format('\n'.join(steps_to_fix))


def get_success_new_thing_text(thing_text):
    return "Вы успешно загрузили информацию о товаре, он будет выглядеть следующим образом:\n\n<blockquote>{}</blockquote>".format(thing_text)


def get_thing_article(article):
    return f"Товар успешно добавлен! <b>Артикул: {article}</b>"


def article_must_be_digit(article):
    return f"<b>{article}</b> - должен быть числовым значением."


def article_not_found(article):
    return f"<b>{article}</b> - по этому артикулу ничего не найдено."


def new_order_for_admin_text(username, name, thing_name, article, time):
    return (f"🆕 Новый заказ! 🆕\n<b>Пользователь</b> - @{username}.\n<b>Имя</b> - {name}\n<b>Товар:</b> {thing_name}"
            f"\n<b>Артикул товара</b> - {article}.\n\n<b>Время заказа</b>: {time}")


def __add_tg_spoiler_article(text, article):
    return text + '\n\n<span class="tg-spoiler">Артикул: {}</span>'.format(article)


def make_order_text(article):
    return __add_tg_spoiler_article('Хотите сделать заказ по данному товару?', article)


def things_count_text(count):
    return f'Количество объектов в базе данных на данный момент: <b>{count}</b>.'


def things_by_range_not_found(start, end):
    return f"🚫 По данному числовому диапазону ничего не найдено:\n<b>{start} ➡️ {end}</b>"


def edit_thing_text(article):
    return __add_tg_spoiler_article('Что вы хотите сделать с этим товаром?', article)


def you_want_delete_thing_text(article):
    return __add_tg_spoiler_article("Вы уверены, что хотите удалить данный товар?", article)


def thing_successful_deleted_text(article):
    return f"Товар с артикулом <b>{article}</b> успешно удалена!"


def thing_not_deleted_text(article):
    return f"Товар с артикулом <b>{article}</b> не найден!"