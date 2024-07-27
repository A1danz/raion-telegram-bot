from bot.dict_names.colors import *
from bot.utils.thing_options import *
from bot.utils.string_converter import *
from bot.models import Thing
from bot.dict_names.colors import *
from bot.dict_names.categories import *


class TgThingModel:
    def __init__(self, photos=None, colors_list=None, name=None, category=None, description=None, cost=None, thing_id=None):
        self.id = thing_id
        self.photos = photos
        self.colors = colors_list
        self.name = name
        self.category = category
        self.description = description
        self.cost = cost

    def __str__(self):
        return (f"Название: {self.name}\nКатегория: {self.category}\nЦвета: {self.colors}\nОписание: {self.description}"
                f"\nФото: {self.photos}\nСтоимость: {self.cost}")

    def photos_is_filled(self):
        return self.photos is not None

    def colors_is_filled(self):
        return self.colors is not None

    def name_is_filled(self):
        return self.name is not None

    def category_is_filled(self):
        return self.category is not None

    def description_is_filled(self):
        return self.description is not None

    def cost_is_filled(self):
        return self.cost is not None

    def get_required_not_filled_options(self):
        result = []
        if not self.colors_is_filled():
            result.append(COLORS)
        if not self.name_is_filled():
            result.append(NAME)
        if not self.category_is_filled():
            result.append(CATEGORY)
        if not self.description_is_filled():
            result.append(DESCRIPTION)

        return result

    def get_validation_steps(self):
        steps = [
            self.__get_colors_validation_steps(),
            self.__get_category_validation_steps(),
            self.__get_cost_validation_steps()
        ]

        steps = list(filter(lambda step: step is not None, steps))
        return steps

    def __get_colors_validation_steps(self):
        if self.colors is None:
            return None

        invalid_colors = []
        for color in self.colors:
            if color not in COLOR_EMOJI:
                invalid_colors.append(color)
        if len(invalid_colors) != 0:
            return "Цвета не найдены: " + ", ".join(invalid_colors)

        return None

    def __get_category_validation_steps(self):
        if self.category is None:
            return None

        result = None
        if self.category not in CATEGORIES_LIST:
            result = f"Категория не найдена: {self.category}"

        return result

    def __get_cost_validation_steps(self):
        if self.cost is None:
            return None

        result = None
        try:
            int(self.cost)
        except ValueError:
            result = f"Цена не подходит под целый числовой тип: {self.cost}"

        return result

    def is_ready_to_save(self):
        return self.name_is_filled() and self.colors_is_filled() and self.category_is_filled()

    def append_photo(self, photo_file_id, photo_path):
        if self.photos is None:
            self.photos = []

        self.photos.append(
            TgPhotoModel(
                photo_file_id,
                photo_path
            )
        )

    def get_thing_card_text(self):
        return (
            f"<b>{self.name}</b>\n"
            f"{self.category}\n"
            f"Цвета: {''.join(map(map_color_to_emoji, self.colors))}\n"
            f"Цена: <b>{'не указана' if self.cost is None else convert_cost(self.cost) + ' ₽'}</b>\n\n"
            f"{self.description}"
        )

    def get_name_with_price(self):
        return f"{self.name} | {convert_cost(self.cost)} ₽"

    def __setattr__(self, __name, __value):
        if __name == "colors" and __value is not None and isinstance(__value, list):
            __value = list(map(self.standardize_text, __value))
        if __name == "category" and __value is not None and isinstance(__value, str):
            __value = self.standardize_text(__value)

        super().__setattr__(__name, __value)

    def standardize_text(self, text: str):
        text = text.lower().strip().replace("ё", "е")
        text = text[0].upper() + text[1:]
        return text


class TgPhotoModel:
    def __init__(self, file_id, file_path, url=None):
        self.file_id = file_id
        self.file_path = file_path
        self.url = url
