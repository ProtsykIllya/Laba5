from game import run_game
from ui import ask_int


def main():
    while True:
        try:
            run_game()
        except (KeyboardInterrupt, EOFError):
            print("\nГру перервано. До зустрічі, алхіміку!")
            break
        except Exception as error:
            print(f"Критична помилка: {error}")
            break
        try:
            if ask_int("\nЗіграти ще раз? 1 - так, 0 - ні: ", 0, 1) == 0:
                break
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()

