from config import POTION_STACK
from data_ingredients import INGREDIENTS
from data_potions import POTIONS
from exceptions import (GameError, InventoryFullError,
                        NotEnoughIngredientsError)
from ui import ask_int


def plan_ingredients(player, potion):
    try:
        totals = player.ingredients.totals()
        plan = []
        for essence, need in potion.recipe_counts.items():
            candidates = sorted(
                ((name, count) for name, count in totals.items()
                 if INGREDIENTS[name].essence == essence),
                key=lambda pair: pair[1])
            for name, have in candidates:
                take = min(have, need)
                plan.append((name, take))
                need -= take
                if need == 0:
                    break
            if need > 0:
                raise NotEnoughIngredientsError(
                    f"Не вистачає сутності «{essence}»: бракує {need} шт.")
        return plan
    except NotEnoughIngredientsError:
        raise
    except (KeyError, TypeError) as error:
        raise GameError(f"Помилка планування варіння: {error}") from error


def can_brew(player, potion):
    try:
        plan_ingredients(player, potion)
        return True
    except GameError:
        return False


def brew(player, potion):
    try:
        plan = plan_ingredients(player, potion)
        if player.potions.free_space_for(potion.name) < 1:
            raise InventoryFullError("Інвентар зілля заповнений - продай або дочекайся вечора")
        for name, quantity in plan:
            player.ingredients.remove(name, quantity)
        player.potions.put(potion.name, 1)
        return plan
    except GameError:
        raise
    except Exception as error:
        raise GameError(f"Невдача при варінні: {error}") from error


def show_recipe_book(player):
    try:
        print("\n=== Книга рецептів (✓ - можна зварити зараз) ===")
        for number, potion in enumerate(POTIONS, 1):
            mark = "✓" if can_brew(player, potion) else " "
            recipe = " + ".join(potion.recipe)
            print(f"{number:>2}. [{mark}] {potion.name} — {recipe} (база {potion.price} з.)")
    except (TypeError, AttributeError) as error:
        raise GameError(f"Помилка показу рецептів: {error}") from error


def brew_menu(player):
    try:
        show_recipe_book(player)
        number = ask_int("Номер зілля (0 - скасувати): ", 0, len(POTIONS))
        if number == 0:
            return
        potion = POTIONS[number - 1]
        times = ask_int(f"Скільки зварити (1-{POTION_STACK}): ", 1, POTION_STACK)
        done = 0
        for _ in range(times):
            try:
                brew(player, potion)
                done += 1
            except GameError as error:
                print(f"⚠ {error}")
                break
        if done:
            print(f"✔ Зварено: {potion.name} x{done}")
    except GameError as error:
        print(f"⚠ {error}")