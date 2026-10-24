from config import (START_GOLD, INGREDIENT_SLOTS, INGREDIENT_STACK,
                    POTION_SLOTS, POTION_STACK)
from inventory import Inventory

class Player:
    def __init__(self):
        self.gold = START_GOLD
        self.day = 1
        self.ingredients = Inventory(INGREDIENT_SLOTS, INGREDIENT_STACK, "Інгредієнти")
        self.potions = Inventory(POTION_SLOTS, POTION_STACK, "Зілля")