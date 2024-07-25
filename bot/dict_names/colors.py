BLACK_COLOR = "Черный"
WHITE_COLOR = "Белый"
GREY_COLOR = "Серый"
BROWN_COLOR = "Коричневый"
RED_COLOR = "Красный"
ORANGE_COLOR = "Оранжевый"
YELLOW_COLOR = "Желтый"
GREEN_COLOR = "Зеленый"
BLUE_COLOR = "Синий"
PURPLE_COLOR = "Фиолетовый"
MULTICOLORED_COLOR = "Разноцветный"

COLOR_EMOJI = {
    BLACK_COLOR: "⚫️",
    WHITE_COLOR: "⚪️",
    GREY_COLOR: "🩶",
    BROWN_COLOR: "🟤",
    RED_COLOR: "🔴",
    ORANGE_COLOR: "🟠",
    YELLOW_COLOR: "🟡",
    GREEN_COLOR: "🟢",
    BLUE_COLOR: "🔵",
    PURPLE_COLOR: "🟣",
    MULTICOLORED_COLOR: "🎨"
}


def map_color_to_emoji(str_color):
    return COLOR_EMOJI.get(str_color, "")
