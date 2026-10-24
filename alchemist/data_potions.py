from collections import Counter
from dataclasses import dataclass

from config import POTION_POOL
from data_ingredients import (FIRE, ICE, EARTH, AIR, LIGHT, DARK,
                              LIFE, DEATH, MIND, SPIRIT)
from exceptions import DataError


@dataclass(frozen=True)
class Potion:
    name: str
    price: int
    recipe: tuple

    @property
    def recipe_counts(self):
        return dict(Counter(self.recipe))


_RAW = [
    # --- прості рецепти (2 інгредієнти) ---
    ("Мале зілля лікування", 30, (LIFE, LIFE)),
    ("Зілля вогняного захисту", 35, (FIRE, EARTH)),
    ("Зілля крижаної шкіри", 35, (ICE, EARTH)),
    ("Зілля легкої ходи", 30, (AIR, AIR)),
    ("Зілля нічного бачення", 40, (DARK, LIGHT)),
    ("Еліксир ясного розуму", 40, (MIND, MIND)),
    ("Зілля спокою", 38, (SPIRIT, ICE)),
    ("Настоянка бадьорості", 34, (LIFE, AIR)),
    ("Зілля сили", 42, (FIRE, LIFE)),
    ("Зілля витривалості", 32, (EARTH, EARTH)),
    ("Отрута павука", 45, (DEATH, DEATH)),
    ("Зілля невидимості", 48, (DARK, AIR)),
    ("Зілля сяйва", 36, (LIGHT, LIGHT)),
    ("Зілля холодного розрахунку", 44, (ICE, MIND)),
    ("Зілля пекучого гніву", 38, (FIRE, FIRE)),
    ("Зілля тіней", 36, (DARK, DARK)),
    ("Зілля пам'яті", 50, (MIND, SPIRIT)),
    ("Зілля зцілення духу", 52, (LIFE, SPIRIT)),
    ("Зілля розмови з мертвими", 55, (DEATH, SPIRIT)),
    ("Зілля відлякування нечисті", 46, (LIGHT, DEATH)),
    ("Зілля зростання", 40, (LIFE, EARTH)),
    ("Зілля штормового кроку", 44, (AIR, FIRE)),
    ("Крижаний щит", 38, (ICE, ICE)),
    ("Зілля левітації", 52, (AIR, SPIRIT)),
    ("Зілля прозріння", 54, (LIGHT, MIND)),
    ("Зілля мертвого сну", 50, (DEATH, DARK)),
    ("Зілля теплого вогнища", 42, (FIRE, LIGHT)),
    ("Зілля кам'яної шкіри", 46, (EARTH, DEATH)),
    ("Зілля зимового сну", 48, (ICE, LIFE)),
    ("Зілля чарівного голосу", 45, (SPIRIT, SPIRIT)),
    # --- складні рецепти (3 інгредієнти) ---
    ("Велике зілля лікування", 90, (LIFE, LIFE, LIGHT)),
    ("Еліксир безсмертя", 160, (LIFE, SPIRIT, LIGHT)),
    ("Зілля драконячого подиху", 110, (FIRE, FIRE, DEATH)),
    ("Зілля вічної мерзлоти", 105, (ICE, ICE, DEATH)),
    ("Еліксир мудрості", 100, (MIND, MIND, LIGHT)),
    ("Зілля бурі", 85, (AIR, AIR, FIRE)),
    ("Зілля землетрусу", 88, (EARTH, EARTH, FIRE)),
    ("Зілля тіньового клинка", 120, (DARK, DEATH, MIND)),
    ("Зілля повної невидимості", 115, (DARK, AIR, SPIRIT)),
    ("Еліксир берсерка", 125, (FIRE, LIFE, DEATH)),
    ("Зілля пророчого сну", 130, (MIND, SPIRIT, DARK)),
    ("Зілля сонячного дотику", 118, (LIGHT, FIRE, LIFE)),
    ("Зілля вічної весни", 95, (LIFE, EARTH, AIR)),
    ("Зілля примарного кроку", 122, (AIR, SPIRIT, DEATH)),
    ("Зілля кришталевого розуму", 112, (ICE, MIND, LIGHT)),
    ("Еліксир тиші", 108, (DARK, ICE, SPIRIT)),
    ("Зілля вірності каменю", 98, (EARTH, SPIRIT, LIFE)),
    ("Зілля вогняного прозріння", 135, (FIRE, MIND, SPIRIT)),
    ("Зілля безодні", 102, (DARK, DARK, DEATH)),
    ("Крапля філософського каменю", 180, (LIFE, MIND, SPIRIT)),
]


def build_potions():
    try:
        potions = [Potion(name, price, recipe) for name, price, recipe in _RAW]
        if len(potions) != POTION_POOL:
            raise DataError(f"Очікувалось {POTION_POOL} зілль, а є {len(potions)}")
        if len({p.name for p in potions}) != len(potions):
            raise DataError("Є зілля з однаковими назвами")
        if len({tuple(sorted(p.recipe)) for p in potions}) != len(potions):
            raise DataError("Є зілля з однаковими рецептами")
        return potions
    except DataError:
        raise
    except Exception as error:
        raise DataError(f"Не вдалося створити пул зілля: {error}") from error


POTIONS = build_potions()
POTION_BY_NAME = {p.name: p for p in POTIONS}