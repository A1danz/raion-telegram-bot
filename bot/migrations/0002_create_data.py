from django.db import migrations
from bot.dict_names.colors import *
from bot.dict_names.visibility_types import *
from bot.dict_names.categories import *


def create_initial_data(apps, schema_editor):
    app_name = "bot"

    Color = apps.get_model(app_name, "Color")
    VisibilityType = apps.get_model(app_name, "VisibilityType")
    Category = apps.get_model(app_name, "Category")

    init_colors(Color)
    init_visibility_types(VisibilityType)
    init_categories(Category)


def init_colors(Color):
    Color.objects.bulk_create([
        Color(name=BLACK_COLOR),
        Color(name=WHITE_COLOR),
        Color(name=GREY_COLOR),
        Color(name=BROWN_COLOR),
        Color(name=RED_COLOR),
        Color(name=ORANGE_COLOR),
        Color(name=YELLOW_COLOR),
        Color(name=GREEN_COLOR),
        Color(name=BLUE_COLOR),
        Color(name=PURPLE_COLOR),
        Color(name=MULTICOLORED_COLOR),
    ])


def init_visibility_types(VisibilityType):
    VisibilityType.objects.bulk_create([
        VisibilityType(name=VISIBLE_TYPE),
        VisibilityType(name=HIDE_TYPE)
    ])


def init_categories(Category):
    Category.objects.bulk_create([
        Category(name=TSHIRT_CATEGORY),
        Category(name=HOODIE_CATEGORY),
        Category(name=CAP_CATEGORY)
    ])


class Migration(migrations.Migration):
    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]