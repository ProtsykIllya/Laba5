import random

from config import RENT_PER_DAY
from data_ingredients import INGREDIENT_LIST
from exceptions import GameError


def give_ingredients(player, amount, reason):
    print(f"\n{reason}:")
    for _ in range(amount):
        try:
            ingredient = random.choice(INGREDIENT_LIST)
            left = player.ingredients.add(ingredient.name, 1)
            if left:
                print(f"  ✗ {ingredient.name} - немає місця, інгредієнт втрачено")
            else:
                print(f"  + {ingredient.name} ({ingredient.essence})")
        except (IndexError, GameError) as error:
            print(f"  ⚠ Не вдалося видати інгредієнт: {error}")


def pay_rent(player):
    try:
        player.gold -= RENT_PER_DAY
        print(f"\nОренда лабораторії: -{RENT_PER_DAY} з. Баланс: {player.gold} з.")
    except TypeError as error:
        raise GameError(f"Помилка оплати оренди: {error}") from error