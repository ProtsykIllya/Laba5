import random

from config import PRICE_MIN_MULT, PRICE_MAX_MULT
from data_potions import POTIONS, POTION_BY_NAME
from exceptions import GameError
from ui import ask_int


def generate_prices():
    try:
        return {
            p.name: max(1, round(p.price * random.uniform(PRICE_MIN_MULT, PRICE_MAX_MULT)))
            for p in POTIONS
        }
    except (TypeError, ValueError) as error:
        raise GameError(f"Помилка генерації цін: {error}") from error


def show_market(player, prices):
    try:
        print("\n=== Твоє зілля та ціни сьогодні ===")
        for number, slot in enumerate(player.potions.slots, 1):
            if slot is None:
                continue
            name, count = slot
            today = prices[name]
            base = POTION_BY_NAME[name].price
            arrow = "▲" if today > base else ("▼" if today < base else "=")
            print(f"[{number:02}] {name} x{count} — {today} з./шт. {arrow} (база {base})")
        print(f"Золото: {player.gold}")
    except (KeyError, TypeError) as error:
        raise GameError(f"Помилка показу ринку: {error}") from error


def sell_all(player, prices):
    try:
        earned = 0
        for name, count in player.potions.totals().items():
            player.potions.remove(name, count)
            earned += prices[name] * count
        player.gold += earned
        return earned
    except KeyError as error:
        raise GameError(f"Немає ціни для зілля: {error}") from error


def sell_from_slot(player, prices, index, amount):
    try:
        name = player.potions.remove_from_slot(index, amount)
        earned = prices[name] * amount
        player.gold += earned
        return name, earned
    except KeyError as error:
        raise GameError(f"Немає ціни для зілля: {error}") from error


def market_phase(player):
    try:
        prices = generate_prices()
    except GameError as error:
        print(f"⚠ {error}")
        return
    print(f"\n--- Вечірній ринок, день {player.day} ---")
    while True:
        try:
            if player.potions.is_empty():
                print("Зілля для продажу більше немає.")
                return
            show_market(player, prices)
            print("1 - продати все\n2 - продати зі слота\n0 - завершити торгівлю")
            choice = ask_int("> ", 0, 2)
            if choice == 0:
                return
            if choice == 1:
                print(f"Продано все! Виручка: +{sell_all(player, prices)} з.")
            else:
                number = ask_int("Номер слота: ", 1, len(player.potions.slots))
                slot = player.potions.slots[number - 1]
                if slot is None:
                    raise GameError("Цей слот порожній")
                amount = ask_int(f"Скільки продати (1-{slot[1]}): ", 1, slot[1])
                name, earned = sell_from_slot(player, prices, number - 1, amount)
                print(f"Продано {name} x{amount}: +{earned} з.")
        except GameError as error:
            print(f"⚠ {error}")