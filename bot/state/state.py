from bot.tg_model.tg_models import *
from copy import deepcopy


class NewThingState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.tg_model = TgThingModel()
        self.media_group = None

    def __str__(self):
        return f"{self.tg_model}"

    def is_ready_to_set_photos(self):
        return (self.tg_model.name_is_filled() and self.tg_model.category_is_filled()
                and self.tg_model.colors_is_filled() and self.tg_model.description_is_filled())


class EditThingState:
    def __init__(self, user_id, tg_model):
        self.user_id = user_id
        self.tg_model = tg_model
        self.__original_tg_model = deepcopy(tg_model)
        self.media_group = None

    def need_save(self):
        return self.tg_model != self.__original_tg_model
