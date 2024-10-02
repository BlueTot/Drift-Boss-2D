"""Boosters"""


class Booster:
    costs = {'Double Score': 30,
             'Car Insurance': 30,
             'Coin Rush': 30}

    def __init__(self, booster_type, lvl):

        self.booster_type = booster_type
        self.lvl = lvl
        self.cost = Booster.costs[booster_type] + self.lvl * 10
        self.colour = '#0096FF' if lvl == 0 else '#C5B4E3'

    def increment_level(self, coins):
        if self.lvl < 7 and coins >= self.cost:
            self.lvl += 1
            if self.lvl > 0:
                self.colour = '#C5B4E3'
            coins -= self.cost
            self.cost += 10
        return coins


class DoubleScore(Booster):
    def __init__(self, lvl=0):
        super().__init__('Double Score', lvl)
        self.mana = 0
        self.rem_time = 0

    def increment_level(self, coins):
        return super().increment_level(coins)

    # perk 1: score multiplier (min lv. 1)
    def get_score_multiplier(self):
        return self.lvl * 0.4

    # perk 2: consume all mana and gain a score boost for 30 seconds
    def set_ability_score_multiplier(self, mana):
        self.mana = mana
        self.rem_time = 15 + 5 * (self.lvl - 4)

    def deduct_ability_time(self):
        if self.rem_time > 0:
            self.rem_time -= 1

    def is_active(self):
        if self.rem_time > 0:
            return True
        else:
            return False

    def get_ability_score_multiplier(self):
        if self.lvl >= 4 and self.mana > 0:
            return 0.8 * (self.lvl - 3) * (1 + (self.mana - 100) / 40)
        else:
            return 0


class CarInsurance(Booster):
    def __init__(self, lvl=0):
        super().__init__('Car Insurance', lvl)
        if lvl >= 4:
            self.lives = lvl - 4
        else:
            self.lives = 0
        self.rem_time = 0

    def increment_level(self, coins):
        coins = super().increment_level(coins)
        if self.lvl in [1, 2, 3, 6]:
            self.lives += 1
        return coins

    # perk 1: instantly heal for x% of your max health (min lv. 1)
    def get_instant_heal_amount(self):
        if self.lvl >= 1:
            return self.lvl * 3
        return 0

    # perk 2: extra lives
    def get_num_lives(self):
        if self.lives >= 4:
            return self.lives - 4
        return 0

    def deduct_life(self):
        self.lives -= 1

    # perk 3: consume all flight to gain invincibility for 5s, also reduce score and coins by 50% and gain 2x flight regen
    def set_invincibility_time(self):
        self.rem_time = 5

    def deduct_ability_time(self):
        if self.rem_time > 0:
            self.rem_time -= 1

    def is_active(self):
        if self.rem_time > 0:
            return True
        else:
            return False


class CoinRush(Booster):
    def __init__(self, lvl=0):
        super().__init__('Coin Rush', lvl)
        self.mana = 0
        self.rem_time = 0

    def increment_level(self, coins):
        return super().increment_level(coins)

    # perk 1: higher coin spawn rate (min lv. 1)
    def get_coin_spawn_rate(self):
        rate = 4 - self.lvl
        if rate < 1:
            return 1
        else:
            return rate

    def get_sec_coin_spawn_rate(self):
        if self.lvl >= 4:
            rate = 8 - self.lvl
            if rate < 1:
                return 1
            else:
                return rate
        else:
            return None

    # perk 2: consume all mana and gain a coin boost for 30 seconds
    def set_ability_coin_multiplier(self, mana):
        self.mana = mana
        self.rem_time = 15 + 5 * (self.lvl - 4)

    def deduct_ability_time(self):
        if self.rem_time > 0:
            self.rem_time -= 1

    def is_active(self):
        if self.rem_time > 0:
            return True
        else:
            return False

    def get_ability_coin_multiplier(self):
        if self.lvl >= 4 and self.mana > 0:
            return 0.8 * (self.lvl - 3) * (1 + (self.mana - 100) / 2) / 10
        else:
            return 0
