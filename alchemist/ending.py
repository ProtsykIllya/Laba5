from config import GOAL_GOLD, MAX_DAYS
from exceptions import GameError


def check_ending(player):
    try:
        if player.gold >= GOAL_GOLD:
            return "win"
        if player.gold < 0:
            return "bankrupt"
        if player.day >= MAX_DAYS:
            return "deadline"
        return None
    except TypeError as error:
        raise GameError(f"Помилка перевірки фіналу: {error}") from error


ENDINGS = {
    "win": (
        "🏆 ПЕРЕМОГА!\n"
        "Ти зібрав {gold} золотих і викупив ліцензію в гільдії алхіміків.\n"
        "Лабораторія тепер твоя назавжди, а королівський двір замовляє\n"
        "в тебе еліксири. Про тебе складають легенди!"
    ),
    "bankrupt": (
        "💀 ПОРАЗКА: банкрутство.\n"
        "Грошей не вистачило навіть на оренду. Кредитори забрали котли,\n"
        "колби та рецепти, а тебе виставили за двері."
    ),
    "deadline": (
        "⌛ ПОРАЗКА: час вийшов.\n"
        "Тридцять днів минуло, а на рахунку лише {gold} золотих.\n"
        "Гільдія забрала лабораторію, і ти знову шукаєш роботу."
    ),
}


def show_ending(result, player):
    try:
        print("\n" + "=" * 50)
        print(ENDINGS[result].format(gold=player.gold))
        print("=" * 50)
    except KeyError as error:
        raise GameError(f"Невідомий фінал: {error}") from error