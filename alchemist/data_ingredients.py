from dataclasses import dataclass

from config import MIN_INGREDIENT_POOL
from exceptions import DataError

FIRE, ICE, EARTH, AIR, LIGHT = "вогонь", "лід", "земля", "повітря", "світло"
DARK, LIFE, DEATH, MIND, SPIRIT = "темрява", "життя", "смерть", "розум", "дух"

ESSENCES = {
    FIRE: "вогняний", ICE: "крижаний", EARTH: "земляний", AIR: "вітряний",
    LIGHT: "сяйний", DARK: "тіньовий", LIFE: "живий", DEATH: "мертвий",
    MIND: "мудрий", SPIRIT: "духовний",
}

BASES = [
    "Гриб", "Корінь", "Лист", "Цвіт", "Мох", "Пагін", "Колос", "Плід",
    "Сік", "Пил", "Попіл", "Лишайник", "Пелюсток", "Шип", "Камінь",
    "Кристал", "Ріг", "Кіготь", "Зуб", "Хвіст",
]


@dataclass(frozen=True)
class Ingredient:
    name: str
    essence: str


def build_pool():
    try:
        pool = {}
        for essence, adjective in ESSENCES.items():
            for base in BASES:
                name = f"{base} {adjective}"
                if name in pool:
                    raise DataError(f"Дубль інгредієнта: {name}")
                pool[name] = Ingredient(name, essence)
        if len(pool) < MIN_INGREDIENT_POOL:
            raise DataError(f"Пул замалий: {len(pool)} < {MIN_INGREDIENT_POOL}")
        return pool
    except DataError:
        raise
    except Exception as error:
        raise DataError(f"Не вдалося створити пул інгредієнтів: {error}") from error


INGREDIENTS = build_pool()
INGREDIENT_LIST = list(INGREDIENTS.values())