import random

from general import *

'''Car Stats File'''


class CarStats:
    def __init__(self, image, drift_angle, coin_req, frag_req, lvl_req, health, health_regen, mana, mana_regen, rarity,
                 ability):
        self.image = image
        self.drift_angle = drift_angle
        self.coin_req = coin_req
        self.frag_req = frag_req
        self.lvl_req = lvl_req
        self.health = health
        self.health_regen = health_regen
        self.mana = mana
        self.mana_regen = mana_regen
        self.rarity = rarity
        self.ability = ability


class CarType:
    rarity_colours = {"COMMON": "#000000",
                      "UNCOMMON": "#32CD32",
                      "RARE": "#0000ff",
                      "EPIC": "#8b008b",
                      "LEGENDARY": "#FFD700",
                      "MYTHIC": "#FF69B4"}

    lvl_rarity_bonuses = {"COMMON": 1,
                          "UNCOMMON": 1.1,
                          "RARE": 1.2,
                          "EPIC": 1.35,
                          "LEGENDARY": 1.65,
                          "MYTHIC": 2.0}

    lvl_costs = {"COMMON": 20,
                 "UNCOMMON": 30,
                 "RARE": 50,
                 "EPIC": 75,
                 "LEGENDARY": 100,
                 "MYTHIC": 150}

    upgrade_rarity_costs = {"COMMON": 300,
                            "UNCOMMON": 450,
                            "RARE": 700,
                            "EPIC": 1200,
                            "LEGENDARY": 2500,
                            "MYTHIC": 6000}

    reforges = ["AGILE", "TITANIC", "HEROIC", "SKILLED", "LUCKY"]
    reforge_stats = {
        "AGILE": {"DRIFT": 0.5, "HEALTH": 0, "HEALTH REGEN": 0, "MANA": 0, "MANA REGEN": 0, "SCORE WISDOM": 0,
                  "COIN WISDOM": 0},
        "TITANIC": {"DRIFT": 0, "HEALTH": 20, "HEALTH REGEN": 6, "MANA": 0, "MANA REGEN": 0, "SCORE WISDOM": 0,
                    "COIN WISDOM": 0},
        "HEROIC": {"DRIFT": 0, "HEALTH": 0, "HEALTH REGEN": 0, "MANA": 20, "MANA REGEN": 6, "SCORE WISDOM": 0,
                   "COIN WISDOM": 0},
        "SKILLED": {"DRIFT": 0, "HEALTH": 0, "HEALTH REGEN": 0, "MANA": 0, "MANA REGEN": 0, "SCORE WISDOM": 20,
                    "COIN WISDOM": 0},
        "LUCKY": {"DRIFT": 0, "HEALTH": 0, "HEALTH REGEN": 0, "MANA": 0, "MANA REGEN": 0, "SCORE WISDOM": 0,
                  "COIN WISDOM": 20}
    }

    reforge_rarity_bonuses = {"COMMON": 1,
                              "UNCOMMON": 1.2,
                              "RARE": 1.5,
                              "EPIC": 1.9,
                              "LEGENDARY": 2.5,
                              "MYTHIC": 3.1}

    reforge_costs = {"COMMON": 40,
                     "UNCOMMON": 70,
                     "RARE": 110,
                     "EPIC": 180,
                     "LEGENDARY": 290,
                     "MYTHIC": 400}

    cars = {"Green Car": CarStats(image="files/green_car.png", drift_angle=1.108, coin_req=0, frag_req=0, lvl_req=0,
                                  health=0, health_regen=0, mana=0, mana_regen=0, rarity="COMMON", ability=None),
            "Yellow Car": CarStats(image="files/yellow_car.png", drift_angle=1.14, coin_req=25, frag_req=0, lvl_req=2,
                                   health=5, health_regen=2, mana=4, mana_regen=2, rarity="COMMON", ability=None),
            "Blue Car": CarStats(image="files/blue_car.png", drift_angle=1.19, coin_req=60, frag_req=0, lvl_req=4,
                                 health=20, health_regen=5, mana=9, mana_regen=5, rarity="UNCOMMON", ability=None),
            "Black Car": CarStats(image="files/black_car.png", drift_angle=1.28, coin_req=120, frag_req=0, lvl_req=7,
                                  health=40, health_regen=8, mana=14, mana_regen=8, rarity="UNCOMMON", ability=None),
            "Taxi": CarStats(image="files/taxi.png", drift_angle=1.35, coin_req=185, frag_req=0, lvl_req=11,
                             health=70, health_regen=14, mana=21, mana_regen=14, rarity="UNCOMMON", ability=None),
            "Police Car": CarStats(image="files/police_car.png", drift_angle=1.45, coin_req=350, frag_req=0, lvl_req=14,
                                   health=110, health_regen=20, mana=36, mana_regen=20, rarity="RARE", ability=None),
            "Ambulance": CarStats(image="files/ambulance.png", drift_angle=1.55, coin_req=550, frag_req=0, lvl_req=19,
                                  health=160, health_regen=26, mana=50, mana_regen=26, rarity="RARE", ability=None),
            "Fire Truck": CarStats(image="files/fire_truck.png", drift_angle=1.7, coin_req=750, frag_req=0, lvl_req=23,
                                   health=220, health_regen=32, mana=65, mana_regen=32, rarity="RARE", ability=None),
            "Bus": CarStats(image="files/bus.png", drift_angle=1.9, coin_req=1000, frag_req=0, lvl_req=28,
                            health=300, health_regen=40, mana=84, mana_regen=40, rarity="EPIC", ability=None),
            "Race Car": CarStats(image="files/racecar.png", drift_angle=2.1, coin_req=1300, frag_req=0, lvl_req=33,
                                 health=380, health_regen=55, mana=105, mana_regen=55, rarity="EPIC", ability=None),
            "Spaceship": CarStats(image="files/spaceship.png", drift_angle=1.3, coin_req=1650, frag_req=0, lvl_req=38,
                                  health=400, health_regen=60, mana=150, mana_regen=60, rarity="EPIC", ability=None),
            "Drifter": CarStats(image="files/the_drifter.png", drift_angle=2.1, coin_req=2400, frag_req=2,
                                lvl_req=43,
                                health=580, health_regen=80, mana=150, mana_regen=80, rarity="LEGENDARY",
                                ability="drifter"),
            "Timewarp": CarStats(image="files/timewarp.png", drift_angle=1.6, coin_req=4000, frag_req=5, lvl_req=48,
                                 health=500, health_regen=70, mana=190, mana_regen=70, rarity="LEGENDARY",
                                 ability="timewarp"),
            "Fortunate": CarStats(image="files/fortunate.png", drift_angle=2.2, coin_req=8000, frag_req=9, lvl_req=53,
                                  health=580, health_regen=80, mana=150, mana_regen=80, rarity="LEGENDARY",
                                  ability="fortunate"),
            "Midas' Car": CarStats(image="files/midas_car.png", drift_angle=2.2, coin_req=14000, frag_req=15,
                                   lvl_req=60,
                                   health=580, health_regen=80, mana=150, mana_regen=80, rarity="LEGENDARY",
                                   ability="midas car")}

    def __init__(self, car_type, lvl=0, lvl_cost=0, upgraded_rarity=False, locked=True, reforge=None):
        self.type = car_type
        self.selected_car = CarType.cars[car_type]
        self.image = pygame.image.load(self.selected_car.image).convert_alpha()

        self.rarity = self.selected_car.rarity
        self.rarity_colour = CarType.rarity_colours[self.rarity]
        self.upgraded_rarity = upgraded_rarity
        if self.upgraded_rarity:
            next_id = list(CarType.rarity_colours.keys()).index(self.rarity) + 1
            self.rarity = list(CarType.rarity_colours.keys())[next_id]
            self.rarity_colour = list(CarType.rarity_colours.values())[next_id]

        self.lvl = lvl
        self.lvl_bonus = (1 + self.lvl / 20) * CarType.lvl_rarity_bonuses[self.rarity] if self.lvl > 0 else 1

        self.reforge = reforge
        self.reforge_drift_bonus = (0 if self.reforge is None else CarType.reforge_stats[self.reforge]["DRIFT"] *
                                                                   CarType.reforge_rarity_bonuses[
                                                                       self.rarity]) * self.lvl_bonus
        self.reforge_health_bonus = (0 if self.reforge is None else CarType.reforge_stats[self.reforge]["HEALTH"] *
                                                                    CarType.reforge_rarity_bonuses[
                                                                        self.rarity]) * self.lvl_bonus
        self.reforge_health_regen_bonus = (0 if self.reforge is None else CarType.reforge_stats[self.reforge][
                                                                              "HEALTH REGEN"] *
                                                                          CarType.reforge_rarity_bonuses[
                                                                              self.rarity]) * self.lvl_bonus
        self.reforge_mana_bonus = (0 if self.reforge is None else CarType.reforge_stats[self.reforge]["MANA"] *
                                                                  CarType.reforge_rarity_bonuses[
                                                                      self.rarity]) * self.lvl_bonus
        self.reforge_mana_regen_bonus = (0 if self.reforge is None else CarType.reforge_stats[self.reforge][
                                                                            "MANA REGEN"] *
                                                                        CarType.reforge_rarity_bonuses[
                                                                            self.rarity]) * self.lvl_bonus
        self.reforge_score_wisdom_bonus = (0 if self.reforge is None else CarType.reforge_stats[self.reforge][
                                                                              "SCORE WISDOM"] *
                                                                          CarType.reforge_rarity_bonuses[
                                                                              self.rarity]) * self.lvl_bonus
        self.reforge_coin_wisdom_bonus = (0 if self.reforge is None else CarType.reforge_stats[self.reforge][
                                                                             "COIN WISDOM"] *
                                                                         CarType.reforge_rarity_bonuses[
                                                                             self.rarity]) * self.lvl_bonus

        self.car_drift_angle = self.selected_car.drift_angle * self.lvl_bonus + self.reforge_drift_bonus
        self.health = self.selected_car.health * self.lvl_bonus + self.reforge_health_bonus
        self.health_regen = self.selected_car.health_regen * self.lvl_bonus + self.reforge_health_regen_bonus
        self.mana = self.selected_car.mana * self.lvl_bonus + self.reforge_mana_bonus
        self.mana_regen = self.selected_car.mana_regen * self.lvl_bonus + self.reforge_mana_regen_bonus
        self.score_wisdom = 0 + self.reforge_score_wisdom_bonus
        self.coin_wisdom = 0 + self.reforge_coin_wisdom_bonus

        self.coin_req = self.selected_car.coin_req
        self.frag_req = self.selected_car.frag_req
        self.lvl_req = self.selected_car.lvl_req
        self.ability = self.selected_car.ability

        self.base_lvl_cost = CarType.lvl_costs[self.rarity]
        self.lvl_cost = lvl_cost
        self.upgrade_rarity_cost = CarType.upgrade_rarity_costs[self.rarity]
        self.reforge_cost = CarType.reforge_costs[self.rarity]
        self.locked = locked

    def update_bonus_stats(self):
        self.__init__(self.type, self.lvl, self.lvl_cost, self.upgraded_rarity, self.locked, self.reforge)

    def upgrade_lvl(self, coins):
        if coins >= self.lvl_cost:
            if self.lvl < 5:
                self.lvl += 1
                coins -= self.lvl_cost
                self.lvl_cost = self.base_lvl_cost * self.lvl
                self.update_bonus_stats()
        return coins

    def upgrade_rarity(self, coins):
        if coins >= self.upgrade_rarity_cost:
            if not self.upgraded_rarity:
                next_id = list(CarType.rarity_colours.keys()).index(self.rarity) + 1
                self.rarity = list(CarType.rarity_colours.keys())[next_id]
                coins -= self.upgrade_rarity_cost
                self.rarity_colour = list(CarType.rarity_colours.values())[next_id]
                self.upgraded_rarity = True
                self.update_bonus_stats()
        return coins

    def change_reforge(self, coins):
        if coins >= self.reforge_cost:
            self.reforge = random.choice(self.reforges)
            self.__init__(self.type, self.lvl, self.lvl_cost, self.upgraded_rarity, self.locked, self.reforge)
            coins -= self.reforge_cost
        return coins

    def load(self, lvl, lvl_cost, upgraded_rarity, locked, reforge):
        self.lvl = lvl
        self.lvl_bonus = (1 + self.lvl / 20) * CarType.lvl_rarity_bonuses[self.rarity]
        self.lvl_cost = lvl_cost
        self.upgraded_rarity = upgraded_rarity
        self.locked = locked
        self.reforge = reforge
        if self.upgraded_rarity:
            next_id = list(CarType.rarity_colours.keys()).index(self.rarity) + 1
            self.rarity = list(CarType.rarity_colours.keys())[next_id]
            self.rarity_colour = list(CarType.rarity_colours.values())[next_id]
        self.__init__(self.type, self.lvl, self.lvl_cost, self.upgraded_rarity, self.locked, self.reforge)

    def save(self):
        return {"lvl": self.lvl, "lvl cost": self.lvl_cost, "upgraded rarity": self.upgraded_rarity, "locked": self.locked, "reforge": self.reforge}


class Cars:
    def __init__(self):
        self.cars = [CarType('Green Car'), CarType('Yellow Car'), CarType('Blue Car'), CarType('Black Car'),
                     CarType('Taxi'), CarType('Police Car'), CarType('Ambulance'), CarType('Fire Truck'),
                     CarType('Bus'), CarType('Race Car'), CarType('Spaceship'), CarType('Drifter'),
                     CarType('Timewarp'), CarType("Fortunate"), CarType("Midas' Car")]

    def reset(self):
        self.__init__()

    def load(self, load_dict):
        for c, load_item in enumerate(list(load_dict.values())):
            lvl, lvl_cost, upgraded_rarity, locked, reforge = list(load_item.values())
            self.cars[c].load(lvl, lvl_cost, upgraded_rarity, locked, reforge)

    def save(self):
        return {car.type: car.save() for car in self.cars}
