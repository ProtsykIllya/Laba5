from alchemy import brew_menu, show_recipe_book
from config import (DAILY_INGREDIENTS, GOAL_GOLD, MAX_DAYS,
                    RENT_PER_DAY, START_INGREDIENTS)
from daily import give_ingredients, pay_rent
from ending import check_ending, show_ending
from exceptions import GameError
from market import market_phase
from player import Player
from ui import ask_int, discard_menu, show_inventory


def show_status(player):
    print(f"\n📅 День {player.day}/{MAX_DAYS} | 💰 {player.gold} з. "
          f"(ціль: {GOAL_GOLD}) | оренда: {RENT_PER_DAY} з./день")


def play_day(player):
    give_ingredients(player, DAILY_INGREDIENTS, "🌿 Ранкова доставка інгредієнтів")
    while True:
        show_status(player)
        print("1 - Інвентар\n2 - Книга рецептів\n3 - Варити зілля\n"
              "4 - Викинути інгредієнт\n5 - Завершити день (ринок + оренда)")
        try:
            choice = ask_int("> ", 1, 5)
            if choice == 1:
                show_inventory(player)
            elif choice == 2:
                show_recipe_book(player)
            elif choice == 3:
                brew_menu(player)
            elif choice == 4:
                discard_menu(player)
            else:
                break
        except GameError as error:
            print(f"⚠ {error}")
    market_phase(player)
    pay_rent(player)


def run_game():
    print("=" * 50)
    print("  АЛХІМІК: ліцензія за 30 днів")
    print("=" * 50)
    print(f"Гільдія вимагає {GOAL_GOLD} золотих за викуп лабораторії.")
    print(f"У тебе {MAX_DAYS} днів. Щодня оренда {RENT_PER_DAY} золотих.\n")

    player = Player()
    give_ingredients(player, START_INGREDIENTS, "🎒 Стартовий набір інгредієнтів")

    while True:
        play_day(player)
        result = check_ending(player)
        if result is not None:
            show_ending(result, player)
            return
        player.day += 1