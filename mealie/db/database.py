from sqlalchemy.orm.session import Session

from db.db_base import BaseDocument
from db.sql.meal_models import MealPlanModel
from db.sql.recipe_models import Category, RecipeModel, Tag
from db.sql.settings_models import SiteSettingsModel
from db.sql.theme_models import SiteThemeModel

"""
# TODO
    - [ ] Abstract Classes to use save_new, and update from base models
"""


class _Recipes(BaseDocument):
    def __init__(self) -> None:
        self.primary_key = "slug"
        self.sql_model = RecipeModel

    def update_image(self, session: Session, slug: str, extension: str = None) -> str:
        entry: RecipeModel = self._query_one(session, match_value=slug)
        entry.image = f"{slug}.{extension}"
        session.commit()

        return f"{slug}.{extension}"


class _Categories(BaseDocument):
    def __init__(self) -> None:
        self.primary_key = "slug"
        self.sql_model = Category


class _Tags(BaseDocument):
    def __init__(self) -> None:
        self.primary_key = "slug"
        self.sql_model = Tag


class _Meals(BaseDocument):
    def __init__(self) -> None:
        self.primary_key = "uid"
        self.sql_model = MealPlanModel


class _Settings(BaseDocument):
    def __init__(self) -> None:
        self.primary_key = "name"
        self.sql_model = SiteSettingsModel

    def create(self, session: Session, main: dict, webhooks: dict) -> str:
        new_settings = self.sql_model(main.get("name"), webhooks)

        session.add(new_settings)
        return_data = new_settings.dict()
        session.commit()

        return return_data


class _Themes(BaseDocument):
    def __init__(self) -> None:
        self.primary_key = "name"
        self.sql_model = SiteThemeModel


class Database:
    def __init__(self) -> None:
        self.recipes = _Recipes()
        self.meals = _Meals()
        self.settings = _Settings()
        self.themes = _Themes()
        self.categories = _Categories()
        self.tags = _Tags()


db = Database()
