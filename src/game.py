class Game:
    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def score(self):
        total = 0
        roll_index = 0

        for _ in range(10):
            first, second = self.rolls[roll_index], self.rolls[roll_index + 1]

            if first + second == 10:
                bonus = self.rolls[roll_index + 2]
                total += 10 + bonus
            else:
                total += first + second

            roll_index += 2

        return total
