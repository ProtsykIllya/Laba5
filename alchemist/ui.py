from data_ingredients import INGREDIENTS
from exceptions import GameError, InvalidInputError


def ask_int(prompt, low, high):
    while True:
        try:
            value = int(input(prompt).strip())
            if not low <= value <= high:
                raise InvalidInputError(f"Введи число від {low} до {high}")
            return value
        except ValueError:
            print("⚠ Це не число, спробуй ще раз.")
        except InvalidInputError as error:
            print(f"⚠ {error}")


def show_ingredients(player):
    try:
        inv = player.ingredients
        print(f"\n=== {inv.title}: {inv.used_slots()}/{len(inv.slots)} слотів ===")
        for number, slot in enumerate(inv.slots, 1):
            if slot is None:
                print(f"[{number:02}] —")
            else:
                name, count = slot
                essence = INGREDIENTS[name].essence
                print(f"[{number:02}] {name} ({essence}) x{count}/{inv.stack_size}")
    except (KeyError, TypeError) as error:
        raise GameError(f"Помилка показу інгредієнтів: {error}") from error


def show_potions(player):
    try:
        inv = player.potions
        print(f"\n=== {inv.title}: {inv.used_slots()}/{len(inv.slots)} слотів ===")
        for number, slot in enumerate(inv.slots, 1):
            if slot is None:
                print(f"[{number:02}] —")
            else:
                print(f"[{number:02}] {slot[0]} x{slot[1]}/{inv.stack_size}")
    except TypeError as error:
        raise GameError(f"Помилка показу зілля: {error}") from error


def show_inventory(player):
    show_ingredients(player)
    show_potions(player)


def discard_menu(player):
    try:
        if player.ingredients.is_empty():
            print("Інвентар інгредієнтів порожній.")
            return
        show_ingredients(player)
        slot_count = len(player.ingredients.slots)
        number = ask_int("Номер слота (0 - скасувати): ", 0, slot_count)
        if number == 0:
            return
        slot = player.ingredients.slots[number - 1]
        if slot is None:
            raise GameError("Цей слот порожній")
        amount = ask_int(f"Скільки викинути (1-{slot[1]}): ", 1, slot[1])
        name = player.ingredients.remove_from_slot(number - 1, amount)
        print(f"Викинуто: {name} x{amount}")
    except GameError as error:
        print(f"⚠ {error}")