from exceptions import GameError, InventoryFullError, NotEnoughItemsError

class Inventory:
    def __init__(self, slots, stack_size, title):
        try:
            if slots <= 0 or stack_size <= 0:
                raise ValueError("розмір має бути додатнім")
            self.title = title
            self.stack_size = stack_size
            self.slots = [None] * slots  # слот = [назва, кількість] або None
        except (TypeError, ValueError) as error:
            raise GameError(f"Некоректні параметри інвентаря: {error}") from error

    # ---------- запити ----------
    def used_slots(self):
        return sum(1 for slot in self.slots if slot is not None)

    def is_empty(self):
        return self.used_slots() == 0

    def count(self, name):
        try:
            return sum(s[1] for s in self.slots if s is not None and s[0] == name)
        except (TypeError, IndexError) as error:
            raise GameError(f"Помилка підрахунку: {error}") from error

    def totals(self):
        try:
            result = {}
            for slot in self.slots:
                if slot is not None:
                    result[slot[0]] = result.get(slot[0], 0) + slot[1]
            return result
        except (TypeError, IndexError) as error:
            raise GameError(f"Помилка підрахунку: {error}") from error

    def free_space_for(self, name):
        space = 0
        for slot in self.slots:
            if slot is None:
                space += self.stack_size
            elif slot[0] == name:
                space += self.stack_size - slot[1]
        return space

    def add(self, name, amount=1):
        try:
            if not isinstance(amount, int) or amount <= 0:
                raise ValueError("кількість має бути додатнім цілим числом")
            left = amount
            for slot in self.slots:
                if left == 0:
                    break
                if slot is not None and slot[0] == name and slot[1] < self.stack_size:
                    put = min(self.stack_size - slot[1], left)
                    slot[1] += put
                    left -= put
            for index, slot in enumerate(self.slots):
                if left == 0:
                    break
                if slot is None:
                    put = min(self.stack_size, left)
                    self.slots[index] = [name, put]
                    left -= put
            return left
        except ValueError as error:
            raise GameError(f"Не вдалося додати «{name}»: {error}") from error

    def put(self, name, amount=1):
        try:
            if self.free_space_for(name) < amount:
                raise InventoryFullError(f"Інвентар «{self.title}» заповнений")
            self.add(name, amount)
        except InventoryFullError:
            raise
        except GameError:
            raise
        except Exception as error:
            raise GameError(f"Помилка додавання: {error}") from error

    def remove(self, name, amount=1):
        try:
            have = self.count(name)
            if amount <= 0:
                raise ValueError("кількість має бути додатньою")
            if have < amount:
                raise NotEnoughItemsError(
                    f"Недостатньо «{name}»: є {have}, потрібно {amount}")
            left = amount
            stacks = sorted(
                (s for s in self.slots if s is not None and s[0] == name),
                key=lambda s: s[1])
            for stack in stacks:
                take = min(stack[1], left)
                stack[1] -= take
                left -= take
                if left == 0:
                    break
            self._cleanup()
        except NotEnoughItemsError:
            raise
        except ValueError as error:
            raise GameError(f"Не вдалося забрати «{name}»: {error}") from error

    def remove_from_slot(self, index, amount):
        try:
            slot = self.slots[index]
        except IndexError as error:
            raise GameError("Такого слота немає") from error
        if slot is None:
            raise GameError("Цей слот порожній")
        if amount <= 0 or amount > slot[1]:
            raise NotEnoughItemsError(f"У слоті лише {slot[1]} шт.")
        name = slot[0]
        slot[1] -= amount
        self._cleanup()
        return name

    def _cleanup(self):
        self.slots = [None if (s is not None and s[1] <= 0) else s for s in self.slots]