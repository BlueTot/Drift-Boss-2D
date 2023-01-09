import pygame
import random
import math
import time
import csv
import os
from tkinter import *
from tkinter import messagebox

'''STR TO BOOL CONVERSION'''


def str_to_bool(string):
    return string == "True"


'''COLOURS'''


class Colours:
    colours = {"LIGHT GREEN": "#90EE90",  # light green
               "LIGHT BLUE": "#ADD8E6",  # light blue
               "LIGHT RED": "#ffcccb",  # light red
               "BROWN": "#A52A2A",  # brown
               "BLUE-PURPLE": "#5D3FD3",  # blue-purple
               "ORANGE": "#FFA500",  # orange
               "YELLOW": "#F0E68C",  # yellow
               "LIGHT PURPLE": "#C5B4E3",  # light purple
               "BLACK": "#000000",  # black
               }


'''All Car Stats'''


class CarStats:
    def __init__(self, image, drift_angle, coin_req, frag_req, lvl_req, flight_duration, flight_regen_rate, rarity,
                 ability):
        self.image = image
        self.drift_angle = drift_angle
        self.coin_req = coin_req
        self.frag_req = frag_req
        self.lvl_req = lvl_req
        self.flight_duration = flight_duration
        self.flight_regen_rate = flight_regen_rate
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
                          "EPIC": 1.45,
                          "LEGENDARY": 1.75,
                          "MYTHIC": 2.2}

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

    cars = {"Green Car": CarStats(image="files/green_car.png", drift_angle=1.108, coin_req=0, frag_req=0, lvl_req=0,
                                  flight_duration=0, flight_regen_rate=None, rarity="COMMON", ability=None),
            "Yellow Car": CarStats(image="files/yellow_car.png", drift_angle=1.14, coin_req=25, frag_req=0, lvl_req=2,
                                   flight_duration=0, flight_regen_rate=None, rarity="COMMON", ability=None),
            "Blue Car": CarStats(image="files/blue_car.png", drift_angle=1.19, coin_req=60, frag_req=0, lvl_req=4,
                                 flight_duration=0, flight_regen_rate=None, rarity="UNCOMMON", ability=None),
            "Black Car": CarStats(image="files/black_car.png", drift_angle=1.28, coin_req=120, frag_req=0, lvl_req=7,
                                  flight_duration=0, flight_regen_rate=None, rarity="UNCOMMON", ability=None),
            "Taxi": CarStats(image="files/taxi.png", drift_angle=1.35, coin_req=185, frag_req=0, lvl_req=11,
                             flight_duration=1, flight_regen_rate=0.04, rarity="UNCOMMON", ability=None),
            "Police Car": CarStats(image="files/police_car.png", drift_angle=1.45, coin_req=350, frag_req=0, lvl_req=14,
                                   flight_duration=2, flight_regen_rate=0.12, rarity="RARE", ability=None),
            "Ambulance": CarStats(image="files/ambulance.png", drift_angle=1.55, coin_req=550, frag_req=0, lvl_req=19,
                                  flight_duration=4, flight_regen_rate=0.35, rarity="RARE", ability=None),
            "Fire Truck": CarStats(image="files/fire_truck.png", drift_angle=1.7, coin_req=750, frag_req=0, lvl_req=23,
                                   flight_duration=6, flight_regen_rate=0.45, rarity="RARE", ability=None),
            "Bus": CarStats(image="files/bus.png", drift_angle=1.9, coin_req=1000, frag_req=0, lvl_req=28,
                            flight_duration=10, flight_regen_rate=0.65, rarity="EPIC", ability=None),
            "Race Car": CarStats(image="files/racecar.png", drift_angle=2.1, coin_req=1300, frag_req=0, lvl_req=33,
                                 flight_duration=13, flight_regen_rate=0.9, rarity="EPIC", ability=None),
            "Spaceship": CarStats(image="files/spaceship.png", drift_angle=1.3, coin_req=1650, frag_req=0, lvl_req=38,
                                  flight_duration=22, flight_regen_rate=1.5, rarity="EPIC", ability=None),
            "The Drifter": CarStats(image="files/the_drifter.png", drift_angle=2.1, coin_req=2400, frag_req=2,
                                    lvl_req=41,
                                    flight_duration=16, flight_regen_rate=1.25, rarity="LEGENDARY",
                                    ability="the drifter"),
            "Timewarp": CarStats(image="files/timewarp.png", drift_angle=1.6, coin_req=4000, frag_req=5, lvl_req=45,
                                 flight_duration=27, flight_regen_rate=1.9, rarity="LEGENDARY", ability="timewarp"),
            "Fortunate": CarStats(image="files/fortunate.png", drift_angle=2.2, coin_req=8000,
                                  frag_req=9, lvl_req=48,
                                  flight_duration=24, flight_regen_rate=1.6, rarity="LEGENDARY",
                                  ability="fortunate"),
            "Midas' Car": CarStats(image="files/midas_car.png", drift_angle=2.2, coin_req=14000, frag_req=15,
                                   lvl_req=50,
                                   flight_duration=24, flight_regen_rate=1.8, rarity="LEGENDARY", ability="midas car")}

    def __init__(self, car_type):
        self.type = car_type
        self.selected_car = CarType.cars[car_type]
        self.image = pygame.image.load(self.selected_car.image).convert_alpha()

        self.car_drift_angle = self.selected_car.drift_angle
        self.flight_duration = self.selected_car.flight_duration
        self.flight_regen_rate = self.selected_car.flight_regen_rate

        self.coin_req = self.selected_car.coin_req
        self.frag_req = self.selected_car.frag_req
        self.lvl_req = self.selected_car.lvl_req
        self.rarity = self.selected_car.rarity
        self.rarity_colour = CarType.rarity_colours[self.rarity]
        self.ability = self.selected_car.ability

        self.lvl = 0
        self.lvl_bonus = 0
        self.base_lvl_cost = CarType.lvl_costs[self.rarity]
        self.lvl_cost = self.base_lvl_cost
        self.upgrade_rarity_cost = CarType.upgrade_rarity_costs[self.rarity]
        self.upgraded_rarity = False
        self.locked = True

    def update_bonus_stats(self):
        self.lvl_bonus = (1 + self.lvl / 20) * CarType.lvl_rarity_bonuses[self.rarity]
        self.car_drift_angle = self.selected_car.drift_angle * self.lvl_bonus
        self.flight_duration = self.selected_car.flight_duration * self.lvl_bonus
        if self.selected_car.flight_regen_rate is not None:
            self.flight_regen_rate = self.selected_car.flight_regen_rate * self.lvl_bonus

    def upgrade_lvl(self, coins):
        if coins >= self.lvl_cost:
            if self.lvl < 10:
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
                self.update_bonus_stats()
                self.upgraded_rarity = True
        return coins

    def load(self, lvl, lvl_cost, upgraded_rarity, locked):
        self.lvl = int(float(lvl))
        self.lvl_bonus = (1 + self.lvl / 20) * CarType.lvl_rarity_bonuses[self.rarity]
        self.lvl_cost = int(float(lvl_cost))
        self.upgraded_rarity = str_to_bool(upgraded_rarity)
        self.locked = str_to_bool(locked)
        if self.upgraded_rarity:
            next_id = list(CarType.rarity_colours.keys()).index(self.rarity) + 1
            self.rarity = list(CarType.rarity_colours.keys())[next_id]
            self.rarity_colour = list(CarType.rarity_colours.values())[next_id]
        self.car_drift_angle = self.selected_car.drift_angle * self.lvl_bonus
        self.flight_duration = self.selected_car.flight_duration * self.lvl_bonus
        if self.selected_car.flight_regen_rate is not None:
            self.flight_regen_rate = self.selected_car.flight_regen_rate * self.lvl_bonus

    def save(self):
        return self.lvl, self.lvl_cost, self.upgraded_rarity, self.locked


class Cars:
    def __init__(self):
        self.cars = [CarType('Green Car'), CarType('Yellow Car'), CarType('Blue Car'), CarType('Black Car'),
                     CarType('Taxi'), CarType('Police Car'), CarType('Ambulance'), CarType('Fire Truck'),
                     CarType('Bus'), CarType('Race Car'), CarType('Spaceship'), CarType('The Drifter'),
                     CarType('Timewarp'), CarType("Fortunate"), CarType("Midas' Car")]

    def reset(self):
        self.__init__()

    def load(self, load_list):
        for c, load_item in enumerate(load_list):
            lvl, lvl_cost, upgraded_rarity, locked = load_item
            self.cars[c].load(lvl, lvl_cost, upgraded_rarity, locked)

    def save(self):
        return [car.save() for car in self.cars]


'''Boosters'''


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
        self.flight_duration = 0
        self.rem_time = 0

    def increment_level(self, coins):
        return super().increment_level(coins)

    # perk 1: score multiplier (min lv. 1)
    def get_score_multiplier(self):
        return self.lvl * 0.4

    # perk 2: consume all flight duration and gain a score boost for 30 seconds
    def set_ability_score_multiplier(self, flight_duration):
        self.flight_duration = flight_duration
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
        if self.lvl >= 4 and self.flight_duration > 0:
            return 0.8 * (self.lvl - 3) * (1 + self.flight_duration / 20)
        else:
            return 0


class CarInsurance(Booster):
    def __init__(self, lvl=0):
        super().__init__('Car Insurance', lvl)
        if lvl in [1, 2, 3]:
            self.lives = lvl
        elif lvl == 6:
            self.lives = 4
        else:
            self.lives = 0
        self.rem_time = 0

    def increment_level(self, coins):
        coins = super().increment_level(coins)
        if self.lvl in [1, 2, 3, 6]:
            self.lives += 1
        return coins

    # perk 1: extra lives (min lv. 1)
    def get_num_lives(self):
        return self.lives

    def deduct_life(self):
        self.lives -= 1

    # perk 2: regenerate flight duration when flying
    def get_flight_regen_amount(self):
        if self.lvl >= 4:
            return (self.lvl - 3) / 6
        return None

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
        self.flight_duration = 0
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

    # perk 2: consume all flight duration and gain a coin boost for 30 seconds
    def set_ability_coin_multiplier(self, flight_duration):
        self.flight_duration = flight_duration
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
        if self.lvl >= 4 and self.flight_duration > 0:
            return 0.8 * (self.lvl - 3) * (1 + self.flight_duration) / 10
        else:
            return 0


'''Player and Selected Car Stats'''


class CarSprite(pygame.sprite.Sprite):
    def __init__(self, car, lvl_bonus):

        pygame.sprite.Sprite.__init__(self)
        self.car = car
        self.image = car.image

        self.car_drift_angle = self.car.car_drift_angle * (1 + lvl_bonus)
        self.max_flight_duration = self.car.flight_duration * (1 + lvl_bonus)
        self.flight_duration = self.car.flight_duration * (1 + lvl_bonus)
        if self.car.flight_regen_rate is not None:
            self.flight_regen_rate = self.car.flight_regen_rate * (1 + lvl_bonus)
        else:
            self.flight_regen_rate = self.car.flight_regen_rate

        self.isFlying = False
        self.rect = self.image.get_rect()
        self.rect.center = (75, -90)
        self.prev_pos_list = [self.rect.center]
        self.prev_heading_list = [-90]
        self.heading = -90
        self.speed = 4
        self.base_speed = 4
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(75, -90)
        self.rot_img = []
        self.min_angle = 1
        for i in range(360):
            rotated_image = pygame.transform.rotozoom(self.image, 360 - 90 - (i * self.min_angle), 1)
            self.rot_img.append(rotated_image)

    def move_up(self):  # move upwards
        if self.heading > -90:
            self.heading -= self.car_drift_angle
        elif self.heading < -90:
            self.heading = -90
        else:
            self.rect = self.image.get_rect()
            self.rect.center = (self.position[0], self.position[1])

    def move_right(self):  # move right
        if self.heading < 0:
            self.heading += self.car_drift_angle
        elif self.heading > 0:
            self.heading = 0
        else:
            self.rect = self.image.get_rect()
            self.rect.center = (self.position[0], self.position[1])

    def fly(self, frames):  # flying (outside path)
        if frames % 60 == 0:
            if self.flight_duration > 0:
                self.flight_duration -= 1

    def regenerate_flight_duration(self, frames, boosters):  # regenerate flight duration when on path
        if self.flight_regen_rate is not None:
            if frames % round(60 / self.flight_regen_rate) == 0:
                if self.flight_duration < self.max_flight_duration:
                    if boosters[1].is_active():
                        self.flight_duration += 2
                    else:
                        self.flight_duration += 1

    def update(self, left, top):  # update car position and direction
        self.velocity.from_polar((self.speed, self.heading))
        self.position += self.velocity
        image_index = int(self.heading)
        self.image = self.rot_img[image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (round(self.position[0]), round(self.position[1]))
        self.prev_pos_list.append((self.position[0], self.position[1]))
        self.prev_heading_list.append(self.heading)

    def collide_path(self, path):  # test if car collides with path
        collide_with_reg_path, collide_with_side_path = False, False
        for tile in path.path_tiles:
            tile_rect = pygame.Rect((tile.x, tile.y, tile.length, tile.width))
            if tile_rect.collidepoint(self.rect.centerx, self.rect.centery) and not tile.invisible:
                collide_with_reg_path = True
        for tile in path.side_path_tiles:
            tile_rect = pygame.Rect((tile.x, tile.y, tile.length, tile.width))
            if tile_rect.collidepoint(self.rect.centerx, self.rect.centery) and not tile.invisible:
                collide_with_side_path = True
        if collide_with_side_path or collide_with_reg_path:
            return True
        else:
            return False


class Player(CarSprite):
    lvl_bonuses = {[n for n in range(52)][n]: [round(0.12 * n ** 1.6, 4) for n in range(52)][n] for n in range(52)}

    def __init__(self, car):
        self.car_type = car
        self.score, self.pb = 0, 0
        self.coins, self.car_fragments = 0, 0
        self.lvl, self.exp = 0, 0
        self.lvl_bonus = 0.0
        self.timewarp_ability1_time = 0
        self.timewarp_ability2_time = 0

        super().__init__(self.car_type, self.lvl_bonus)

    def get_coin_multiplier(self, boosters):
        mult = 1 * (1 + self.lvl_bonus)
        sec_rate = boosters[2].get_sec_coin_spawn_rate()
        if sec_rate is not None:
            r_list = [1 for _ in range(sec_rate - 1)]
            while len(r_list) < 4:
                r_list.append(2)
            if random.choice(r_list) == 2:
                mult += 1
        if boosters[2].is_active():
            mult += boosters[2].get_ability_coin_multiplier()
        if boosters[1].is_active():
            mult /= 2
        if self.timewarp_ability2_time > 0:
            mult *= 1.5
        if self.car_type.type == "Midas' Car":
            mult *= 0
        return mult

    def collect_coins(self, coins, boosters):  # collect coins on the path
        for coin in coins:
            if coin.rect.colliderect(self.rect):
                self.coins += self.get_coin_multiplier(boosters)
                if self.car_type.type == "Midas' Car":
                    self.score += 25
                coins.remove(coin)
                break
        return coins

    def collect_mega_scores(self, mega_scores):
        for mega_score in mega_scores:
            mega_score_rect = pygame.Rect((mega_score.x - mega_score.radius, mega_score.y - mega_score.radius,
                                           mega_score.radius * 2, mega_score.radius * 2))
            if mega_score_rect.colliderect(self.rect):
                if self.car_type.type != "Fortunate":
                    self.score += 300
                else:
                    self.coins += 300
                mega_scores.remove(mega_score)
                break
        return mega_scores

    def collect_mega_coins(self, mega_coins):
        for mega_coin in mega_coins:
            mega_coin_rect = pygame.Rect((mega_coin.x - mega_coin.radius, mega_coin.y - mega_coin.radius,
                                          mega_coin.radius * 2, mega_coin.radius * 2))
            if mega_coin_rect.colliderect(self.rect):
                if self.car_type.type != "Midas' Car":
                    self.coins += 200
                else:
                    self.score += 200 * 25
                mega_coins.remove(mega_coin)
                break
        return mega_coins

    def collect_car_frags(self, car_frags):
        for car_frag in car_frags:
            if car_frag.rect.colliderect(self.rect):
                self.car_fragments += 1
                car_frags.remove(car_frag)
                break
        return car_frags

    def collide_with_spikes(self, f, spikes):
        if f % 30 == 0:
            for spike in spikes:
                spike_rect = pygame.Rect((spike.x, spike.y, 40, 40))
                if spike_rect.colliderect(self.rect):
                    self.flight_duration -= self.max_flight_duration / 2
                    if self.flight_duration < 0:
                        self.flight_duration = 0

    def is_colliding_with_enemy_car(self, enemy_cars):
        for enemy_car in enemy_cars:
            if enemy_car.rect.colliderect(self.rect):
                return True
        else:
            return False

    def get_score_multiplier(self, boosters):
        mult = 1 * (1 + self.lvl_bonus) + boosters[0].get_score_multiplier()
        if boosters[0].is_active():
            mult += boosters[0].get_ability_score_multiplier()
        if boosters[1].is_active():
            mult /= 2
        if self.timewarp_ability2_time > 0:
            mult *= 1.5
        return mult

    def increment_score(self, f, boosters):  # increment player score
        if f % 8 == 0:
            if self.car_type.type != "Fortunate":
                self.score += self.get_score_multiplier(boosters)
            if self.car_type.type == "Fortunate":
                self.coins += self.get_score_multiplier(boosters)

    def use_ds2_ability(self, boosters):
        boosters[0].set_ability_score_multiplier(self.flight_duration)
        self.flight_duration = 0

    def use_ci2_ability(self, f, flight_regen_amount):
        if f % 60 == 0:
            if self.flight_duration < self.max_flight_duration:
                self.flight_duration += flight_regen_amount

    def use_cr2_ability(self, boosters):
        boosters[2].set_ability_coin_multiplier(self.flight_duration)
        self.flight_duration = 0

    def use_ci3_ability(self, boosters):
        boosters[1].set_invincibility_time()
        self.flight_duration = self.max_flight_duration / 2

    def use_timewarp_lc_ability(self):
        self.speed *= 0.5
        self.timewarp_ability1_time = 5
        self.flight_duration -= self.max_flight_duration * 0.25

    def teleport(self):
        angle = abs(self.heading)
        self.position[0] += 4 * 150 * math.cos(math.radians(angle))
        self.position[1] -= 4 * 150 * math.sin(math.radians(angle))

    def use_timewarp_rc_ability(self):
        self.timewarp_ability2_time = 5
        self.flight_duration -= self.max_flight_duration * 0.25
        self.teleport()

    def update_ability_times(self, f, boosters):
        if f % 60 == 0:
            if boosters[0].is_active():
                boosters[0].deduct_ability_time()
            if boosters[2].is_active():
                boosters[2].deduct_ability_time()
            if boosters[1].is_active():
                boosters[1].deduct_ability_time()
            if self.timewarp_ability1_time > 0:
                self.timewarp_ability1_time -= 1
            if self.timewarp_ability1_time == 0:
                self.speed = self.base_speed
            if self.timewarp_ability2_time > 0:
                self.timewarp_ability2_time -= 1

    def update_exp(self, exp_reqs):
        self.exp += self.score
        prev_lvl = self.lvl
        for key, value in exp_reqs.items():
            if self.exp < value:
                self.lvl = key - 1
                break
        if self.exp > exp_reqs[51]:
            self.lvl = 51
        if prev_lvl != self.lvl:
            self.lvl_bonus = Player.lvl_bonuses[self.lvl] / 100
            super().__init__(self.car_type, self.lvl_bonus)

    def reset(self):
        if self.score > self.pb:
            self.pb = self.score
        self.score = 0
        self.set_car_type(self.car_type)

    def reset_game(self):
        self.__init__(self.car)

    def set_car_type(self, car_type):
        self.car_type = car_type
        super().__init__(car_type, self.lvl_bonus)

    def render(self, display, left, top):  # render car image
        display.blit(self.image, (self.rect.x - left, self.rect.y - top))

    def render_text(self, surface, boosters):  # render text on gameplay screen
        font = pygame.font.Font('files/Quick Starter.ttf', 45)
        score = font.render(f"{round(self.score)}", True, (0, 0, 0))
        score_rect = score.get_rect()
        score_rect.center = (250, 25)
        surface.blit(score, score_rect)
        surface.blit(pygame.image.load("files/coin.png").convert_alpha(), (0, 0))  # top left coin img
        create_text(surface, str(round(self.coins)), 25, (0, 0, 0), (45, 17))  # number of coins
        surface.blit(pygame.image.load("files/car_fragment.png").convert_alpha(), (0, 45))
        create_text(surface, str(self.car_fragments), 25, (0, 0, 0), (50, 57))  # number of car fragments
        create_text(surface, f'LIVES: {boosters[1].get_num_lives()}', 20, (0, 0, 0),
                    (370, 460))  # render remaining lives
        if self.max_flight_duration > 0 and boosters[0].lvl >= 4 and boosters[0].rem_time > 0:
            create_text(surface, f'A1: {boosters[0].rem_time}', 20, (255, 0, 0), (405, 390))
        if self.max_flight_duration > 0 and boosters[2].lvl >= 4 and boosters[2].rem_time > 0:
            create_text(surface, f'A2: {boosters[2].rem_time}', 20, (0, 0, 255), (405, 410))
        if self.max_flight_duration > 0 and boosters[1].lvl == 7 and boosters[1].rem_time > 0:
            create_text(surface, f'A3: {boosters[1].rem_time}', 20, (0, 255, 0), (405, 430))
        if self.timewarp_ability1_time > 0:
            create_text(surface, f'TW1: {self.timewarp_ability1_time}', 20, (255, 255, 0), (400, 350))
        if self.timewarp_ability2_time > 0:
            create_text(surface, f'TW2: {self.timewarp_ability2_time}', 20, (0, 255, 255), (400, 370))

    def load(self, load_list):
        pb, coins, car_fragments, lvl, exp = load_list[0]
        self.pb = float(pb)
        self.coins = float(coins)
        self.car_fragments = int(float(car_fragments))
        self.lvl = int(float(lvl))
        self.exp = float(exp)
        self.lvl_bonus = Player.lvl_bonuses[self.lvl] / 100
        super().__init__(self.car_type, self.lvl_bonus)

    def save(self):
        return [[self.pb, self.coins, self.car_fragments, self.lvl, self.exp]]


'''Enemy Car Stats and AI'''


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("files/police_car.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 4.1
        self.heading = -90
        self.velocity = pygame.math.Vector2(0, 0)
        self.rot_img = []
        self.min_angle = 1
        for i in range(360):
            rotated_image = pygame.transform.rotozoom(self.image, 360 - 90 - (i * self.min_angle), 1)
            self.rot_img.append(rotated_image)

    def move_towards_player(self, player):
        dirvect = pygame.math.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        horvect = pygame.math.Vector2(1, 0)
        dirvect.normalize()
        dirvect.scale_to_length(self.speed)
        self.heading = -1 * round(dirvect.angle_to(horvect))
        x, y = self.rect.centerx, self.rect.centery
        image_index = int(self.heading)
        self.image = self.rot_img[image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.move_ip(dirvect)

    def move(self, player):
        self.move_towards_player(player)
        self.update(player)

    def render(self, display, left, top):
        display.blit(self.image, (self.rect.x - left, self.rect.y - top))


'''Path Generation'''


class Coin:  # coin class
    def __init__(self, x, y):
        self.image = pygame.image.load("files/coin.png").convert_alpha()
        self.rect = pygame.Rect((x, y, 30, 30))


class MegaScore:  # mega score class (for double score 7)
    def __init__(self, x, y):
        self.colour = (255, 0, 0)
        self.x = x
        self.y = y
        self.radius = 20


class MegaCoin:  # mega coin class (for coin rush 7)
    def __init__(self, x, y):
        self.colour = (0, 0, 255)
        self.x = x
        self.y = y
        self.radius = 20


class CarFragment:  # car fragment class
    def __init__(self, x, y):
        self.image = pygame.image.load("files/car_fragment.png").convert_alpha()
        self.rect = pygame.Rect((x, y, 50, 50))


class Spike:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PathTile:  # individual path tile class
    def __init__(self, x, y, length, width, colour, path_type, direction, invisible=False):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.colour = colour
        self.type = path_type
        self.invisible = invisible
        self.direction = direction


class Structures:

    @staticmethod
    def double_thin_path(direction):
        if direction == "UP":
            return {(0, -1): 'regular', (0, -2): 'regular', (1, -2): 'regular',
                    (0, -3): 'thin', (0, -4): 'thin', (0, -5): 'thin', (0, -6): 'thin',
                    (0, -7): 'thin', (0, -8): 'thin', (0, -9): 'thin', (0, -10): 'thin',
                    (1, -3): 'thin', (1, -4): 'thin', (1, -5): 'thin', (1, -6): 'thin',
                    (1, -7): 'thin', (1, -8): 'thin', (1, -9): 'thin', (1, -10): 'thin',
                    (0, -11): 'regular', (1, -11): 'regular', (1, -12): 'regular'}
        else:
            return {(1, 0): 'regular', (2, 0): 'regular', (2, -1): 'regular',
                    (3, 0): 'thin', (4, 0): 'thin', (5, 0): 'thin', (6, 0): 'thin',
                    (7, 0): 'thin', (8, 0): 'thin', (9, 0): 'thin', (10, 0): 'thin',
                    (3, -1): 'thin', (4, -1): 'thin', (5, -1): 'thin', (6, -1): 'thin',
                    (7, -1): 'thin', (8, -1): 'thin', (9, -1): 'thin', (10, -1): 'thin',
                    (11, 0): 'regular', (11, -1): 'regular', (12, -1): 'regular'}

    @staticmethod
    def grid_path(direction):
        grid = {}
        if direction == "UP":
            for x in range(8):
                for y in range(8):
                    if y % 2 == 0:
                        grid[(x, -1 * y)] = 'regular'
                    else:
                        if (x + (y // 2) % 2) % 2 == 0:
                            grid[(x, -1 * y)] = 'regular'
            grid[(7, -7)] = 'regular'
        else:
            for x in range(8):
                for y in range(8):
                    if x % 2 == 0:
                        grid[(y, -1 * x)] = 'regular'
                    else:
                        if (y + (x // 2) % 2) % 2 == 0:
                            grid[(y, -1 * x)] = 'regular'
            grid[(7, -7)] = 'regular'
        return grid

    @staticmethod
    def s3_s4_transition(direction):
        grid = {}
        if direction == "UP":
            for x in range(10):
                for y in range(10):
                    if (x + y) % 2 == 0:
                        grid[(x, -1 * y - 1)] = 'thin'
            grid[(9, -10)] = 'regular'
        else:
            for x in range(10):
                for y in range(10):
                    if (x + y) % 2 == 0:
                        grid[(y + 1, -1 * x)] = 'thin'
            grid[(9, -10)] = 'regular'
        return grid


class Path:  # pathway class
    def __init__(self):  # constructor
        self.path_tiles = [PathTile(0, -500, 150, 750, "#90EE90", 'regular', "UP")]
        self.side_path_tiles = []
        self.coins, self.mega_scores, self.mega_coins = [], [], []
        self.spikes, self.car_frags = [], []
        self.enemy_cars = []
        self.stage = 0
        self.COLOURS = {0: Colours.colours["LIGHT GREEN"],  # light green
                        1: Colours.colours["LIGHT BLUE"],  # light blue
                        2: Colours.colours["LIGHT RED"],  # light red
                        3: Colours.colours["BROWN"],  # brown
                        4: Colours.colours["BLUE-PURPLE"],  # blue-purple
                        5: Colours.colours["ORANGE"],  # orange
                        6: Colours.colours["YELLOW"],  # yellow
                        7: Colours.colours["LIGHT PURPLE"],  # light purple
                        8: Colours.colours["BLACK"],  # black (for finishing part)
                        }
        self.path_num = 0
        self.current_path = 0
        self.has_gen_transition_yet = False
        self.has_finished = False

    @staticmethod
    def draw_arrow(screen, colour, start, end):
        pygame.draw.line(screen, colour, start, end, 2)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        pygame.draw.polygon(screen, (50, 50, 50), (
            (end[0] + 20 * math.sin(math.radians(rotation)), end[1] + 20 * math.cos(math.radians(rotation))),
            (
                end[0] + 20 * math.sin(math.radians(rotation - 120)),
                end[1] + 20 * math.cos(math.radians(rotation - 120))),
            (end[0] + 20 * math.sin(math.radians(rotation + 120)),
             end[1] + 20 * math.cos(math.radians(rotation + 120)))))

    @staticmethod
    def add_path(location, start, direction, colour, path_type, is_invisible=False, manual_coords=None):  # add path
        if manual_coords is None:
            if path_type == 'regular':  # regular
                length, width = 150, 150
                if start.type == 'thin':  # regular to thin
                    if direction == 'UP':  # Up
                        location.append(
                            PathTile(start.x - 35, start.y - length, width, length, colour, path_type, "UP",
                                     is_invisible))
                    else:  # Right
                        location.append(
                            PathTile(start.x + start.length, start.y - 35, length, width, colour, path_type, "RIGHT",
                                     is_invisible))
                else:  # regular to regular
                    if direction == 'UP':  # Up
                        location.append(
                            PathTile(start.x, start.y - length, width, length, colour, path_type, "UP", is_invisible))
                    else:  # Right
                        location.append(
                            PathTile(start.x + start.length, start.y, length, width, colour, path_type, "RIGHT",
                                     is_invisible))
            else:  # thin
                length, width = 150, 80
                if direction == 'UP':  # Up
                    location.append(
                        PathTile(start.x + 35, start.y - length, width, length, colour, path_type, "UP", is_invisible))
                else:  # Right
                    location.append(
                        PathTile(start.x + start.length, start.y + 35, length, width, colour, path_type, "RIGHT",
                                 is_invisible))
        else:
            x, y = manual_coords
            if path_type == 'regular':
                length, width = 150, 150
                location.append(
                    PathTile(start.x + x, start.y + y, width, length, colour, path_type, None, is_invisible))
            else:
                length, width = 150, 80
                if direction == 'UP':  # Up
                    location.append(
                        PathTile(start.x + x, start.y + y, width, length, colour, path_type, "UP", is_invisible))
                else:  # Right
                    location.append(
                        PathTile(start.x + x, start.y + y, length, width, colour, path_type, "RIGHT", is_invisible))

    def generate_mega_score(self):  # generate mega score on path
        last = self.path_tiles[-1]
        if last.type == "regular":
            x, y = last.x + 75, last.y + 75
        else:
            if last.direction == "UP":
                x, y = last.x + last.length // 2, last.y + 75
            else:
                x, y = last.x + 75, last.y + last.width // 2
        self.mega_scores.append(MegaScore(x, y))

    def generate_mega_coin(self):  # generate mega coin on path
        last = self.path_tiles[-1]
        if last.type == "regular":
            x, y = last.x + 75, last.y + 75
        else:
            if last.direction == "UP":
                x, y = last.x + last.length // 2, last.y + 75
            else:
                x, y = last.x + 75, last.y + last.width // 2
        self.mega_coins.append(MegaCoin(x, y))

    def generate_car_fragment(self):
        last = self.path_tiles[-1]
        self.car_frags.append(CarFragment(last.x + (last.length - 50) // 2, last.y + (last.width - 50) // 2))

    def generate_spike(self):
        last = self.path_tiles[-1]
        self.spikes.append(Spike(last.x + (last.length - 50) // 2, last.y + (last.width - 50) // 2))

    def generate_coins(self, boosters, direction=None, is_invisible=False):  # generate coins on path
        rate = boosters[2].get_coin_spawn_rate()
        if is_invisible:
            rate -= 2
            if rate < 0:
                rate = 0
        r_list = [1 for _ in range(rate - 1)]
        while len(r_list) < 4:
            r_list.append(2)
        has_entity = False
        if boosters[0].lvl == 7 and not has_entity:  # generate mega score
            if random.randint(1, 40) == 1:
                self.generate_mega_score()
                has_entity = True
        if boosters[2].lvl == 7 and not has_entity:  # generate mega coin
            if random.randint(1, 40) == 1:
                self.generate_mega_coin()
                has_entity = True
        if self.stage >= 6 and random.randint(1, 20) == 1:
            self.generate_spike()
            has_entity = True
        if self.stage >= 6 and random.randint(1, 20) == 1:
            self.generate_car_fragment()
            has_entity = True
        if not has_entity:  # If space is still available
            if direction == 'UP':  # Direction = Up
                if random.choice(r_list) == 2:
                    last = self.path_tiles[-1]
                    if is_invisible:  # Invisible: generate 6 coins
                        for inc in [0, 50, 100]:
                            self.coins.append(Coin(last.x + (last.length - 100) / 2, last.y + inc))
                            self.coins.append(Coin(last.x + 50 + (last.length - 100) / 2, last.y + inc))
                    else:  # Visible: generate 3 coins
                        for inc in [0, 50, 100]:
                            self.coins.append(Coin(last.x + (last.length - 50) / 2, last.y + inc))
            elif direction == 'RIGHT':  # Direction = Right
                if random.choice(r_list) == 2:
                    last = self.path_tiles[-1]
                    if is_invisible:  # Invisible: generate 6 coins
                        for inc in [0, 50, 100]:
                            self.coins.append(Coin(last.x + inc, last.y + (last.width - 100) / 2))
                            self.coins.append(Coin(last.x + inc, last.y + 50 + (last.width - 100) / 2))
                    else:  # Visible: generate 3 coins
                        for inc in [0, 50, 100]:
                            self.coins.append(Coin(last.x + inc, last.y + (last.width - 50) / 2))
            elif direction is None:  # No direction
                if random.choice(r_list) == 2:
                    last = self.path_tiles[-1]
                    self.coins.append(Coin(last.x + (last.length - 50) / 2, last.y + (last.width - 50) / 2))  # Generate 1 coin

    def generate_straight_path(self, location, colour, boosters, is_invisible=False):
        direction = random.choice(['UP', 'RIGHT'])
        path_len = random.randint(1, 5)
        for count in range(path_len):
            last = self.path_tiles[-1] if location == self.path_tiles else self.side_path_tiles[-1]
            self.add_path(location=location, start=last, direction=direction, colour=colour, path_type='regular',
                          is_invisible=is_invisible)
            if location == self.path_tiles:
                self.path_num += 1
            if location == self.path_tiles:
                if is_invisible:
                    if path_len > 2 and count not in [0, path_len - 1]:
                        self.generate_coins(boosters, direction, True)
                    else:
                        self.generate_coins(boosters, None, True)
                else:
                    if path_len > 2 and count not in [0, path_len - 1]:
                        self.generate_coins(boosters, direction)
                    else:
                        self.generate_coins(boosters)

    def generate_diagonal_path(self, location, colour, boosters, is_invisible=False):
        for count in range(3):
            last = self.path_tiles[-1] if location == self.path_tiles else self.side_path_tiles[-1]
            if count % 2 == 0:
                direction = 'UP'
            else:
                direction = 'RIGHT'
            self.add_path(location=location, start=last, direction=direction, colour=colour, path_type='regular',
                          is_invisible=is_invisible)
            if location == self.path_tiles:
                self.path_num += 1
            if location == self.path_tiles:
                if is_invisible:
                    self.generate_coins(boosters, None, True)
                else:
                    self.generate_coins(boosters)

    def generate_thin_straight_path(self, colour, boosters):
        path_length = random.randint(3, 7)
        direction = random.choice(['UP', 'RIGHT'])
        last = self.path_tiles[-1]
        self.add_path(location=self.path_tiles, start=last, direction=direction, colour=colour, path_type='regular')
        self.generate_coins(boosters)
        last = self.path_tiles[-1]
        for count in range(path_length - 2):
            self.add_path(location=self.path_tiles, start=last, direction=direction, colour=colour, path_type='thin')
            if count not in [0, path_length - 1]:
                self.generate_coins(boosters, direction)
            else:
                self.generate_coins(boosters)
            self.path_num += 1
        last = self.path_tiles[-1]
        self.add_path(location=self.path_tiles, start=last, direction=direction, colour=colour, path_type='regular')
        self.generate_coins(boosters)

    def generate_thin_diagonal_path(self, colour, boosters):
        for count in range(1, 10):
            last = self.path_tiles[-1]
            if count in [1, 2, 3, 6, 7]:
                direction = 'UP'
            else:
                direction = 'RIGHT'
            if count % 2 == 1:
                self.add_path(location=self.path_tiles, start=last, direction=direction, colour=colour,
                              path_type='regular')
                self.generate_coins(boosters)
            else:
                self.add_path(location=self.path_tiles, start=last, direction=direction, colour=colour,
                              path_type='thin')
                self.generate_coins(boosters, direction)
            self.path_num += 1

    def generate_double_thin_path(self, colour, boosters):
        direction = random.choice(["UP", "RIGHT"])
        start_tile = self.path_tiles[-1]
        if direction == "UP":
            for coord, path_type in Structures.double_thin_path("UP").items():
                xyc = [coord[0] * 150, coord[1] * 150]
                xyc[0] += 35 if path_type == "thin" else 0
                self.add_path(location=self.path_tiles, start=start_tile, direction="UP", colour=colour,
                              path_type=path_type, manual_coords=xyc)
                if path_type == "regular":
                    self.generate_coins(boosters, direction)
                else:
                    self.generate_coins(boosters)
                self.path_num += 1
        else:
            for coord, path_type in Structures.double_thin_path("RIGHT").items():
                xyc = [coord[0] * 150, coord[1] * 150]
                xyc[1] += 35 if path_type == "thin" else 0
                self.add_path(location=self.path_tiles, start=start_tile, direction="RIGHT", colour=colour,
                              path_type=path_type,
                              manual_coords=xyc)
                if path_type == "regular":
                    self.generate_coins(boosters, direction)
                else:
                    self.generate_coins(boosters)
                self.path_num += 1

    def generate_reg_grid_path(self, colour, boosters):
        direction = random.choice(["UP", "RIGHT"])
        start_tile = self.path_tiles[-1]
        if direction == "UP":
            for coord, path_type in Structures.grid_path("UP").items():
                xyc = [coord[0] * 150, coord[1] * 150]
                self.add_path(location=self.path_tiles, start=start_tile, direction="UP", colour=colour,
                              path_type=path_type, manual_coords=xyc)
                self.generate_coins(boosters)
        else:
            for coord, path_type in Structures.grid_path("RIGHT").items():
                xyc = [coord[0] * 150, coord[1] * 150]
                self.add_path(location=self.path_tiles, start=start_tile, direction="RIGHT", colour=colour,
                              path_type=path_type,
                              manual_coords=xyc)
                self.generate_coins(boosters)
        self.path_num += 10

    def generate_transition(self, colour, boosters):
        direction = random.choice(["UP", "RIGHT"])
        start_tile = self.path_tiles[-1]
        if direction == "UP":
            for coord, path_type in Structures.s3_s4_transition("UP").items():
                xyc = [coord[0] * 150, coord[1] * 150]
                self.add_path(location=self.path_tiles, start=start_tile, direction=random.choice(["UP", "RIGHT"]),
                              colour=colour, path_type=path_type, manual_coords=xyc)
                self.generate_coins(boosters)
        else:
            for coord, path_type in Structures.s3_s4_transition("RIGHT").items():
                xyc = [coord[0] * 150, coord[1] * 150]
                self.add_path(location=self.path_tiles, start=start_tile, direction=random.choice(["UP", "RIGHT"]),
                              colour=colour, path_type=path_type,
                              manual_coords=xyc)
                self.generate_coins(boosters)

    def generate_side_path(self, colour, boosters):
        x_coord = random.randint(-10, 10)
        self.add_path(location=self.side_path_tiles, start=self.path_tiles[-1],
                      direction=random.choice(["UP", "RIGHT"]), colour=colour,
                      path_type="regular", manual_coords=(self.path_tiles[-1].x + x_coord * 150, self.path_tiles[-1].y))
        self.enemy_cars.append(EnemyCar(self.path_tiles[-1].x + x_coord * 150 + 55, self.path_tiles[-1].y - 35))
        for count in range(20):
            if random.choice([1, 2]) == 1:
                self.generate_straight_path(self.side_path_tiles, colour, boosters)
            else:
                self.generate_diagonal_path(self.side_path_tiles, colour, boosters)

    def generate_ending_path(self, colour):
        self.add_path(location=self.path_tiles, start=self.path_tiles[-1], direction="UP", colour=colour,
                      path_type="regular")
        self.has_finished = True

    def generate_path(self, frames, car, boosters):  # generate next path
        if frames % 40 == 0:
            self.stage = self.path_num // 40
            colour = self.COLOURS[self.stage % 9]
            if self.stage >= 8:
                choice = [6]
            elif self.stage >= 7:
                choice = [0] * 6 + [1] * 6 + [2] * 17 + [3] * 5 + [4]
            elif self.stage == 6:
                if not self.has_gen_transition_yet:
                    choice = [5]
                    self.has_gen_transition_yet = True
                else:
                    choice = [0] * 6 + [1] * 5 + [2] * 14 + [3] * 3 + [4]
            elif self.stage == 5:  # Orange Stage (6)
                choice = [0] * 6 + [1] * 5 + [2] * 14 + [3] * 3 + [4]
            elif self.stage == 4:  # Purple Stage (5)
                choice = [0] * 6 + [1] * 5 + [2] * 14 + [3] * 3 + [4]
            elif self.stage == 3:  # Brown Stage (4)
                choice = [0] * 10 + [1] * 5 + [3] + [4]
            elif self.stage == 2:  # Light Red Stage (3)
                choice = [0] * 11 + [1] * 5 + [4]
            elif self.stage == 1:  # Blue Stage (2)
                choice = [0] * 12 + [4]
            else:  # Green Stage (1)
                choice = [0] * 2
            modes = ['straight', 'thin', 'floating', 'double thin', 'grid', 'transition', 'ending path']
            generation_mode = modes[random.choice(choice)]

            if not self.has_finished:
                if generation_mode == 'straight':
                    if random.choice([1, 2]) == 1:  # Straight path
                        self.generate_straight_path(self.path_tiles, colour, boosters)
                    else:  # Diagonal path
                        self.generate_diagonal_path(self.path_tiles, colour, boosters)
                elif generation_mode == 'thin':
                    if random.choice([1, 2]) == 1:  # Thin bridge (straight)
                        self.generate_thin_straight_path(colour, boosters)
                    else:  # Thin bridge (diagonal)
                        self.generate_thin_diagonal_path(colour, boosters)
                elif generation_mode == 'floating':
                    if random.choice([1, 2]) == 1:  # Floating Straight Path
                        if random.choice([1, 1, 2]) == 1:  # Invisible
                            self.generate_straight_path(self.path_tiles, colour, boosters, True)
                        else:  # Visible
                            self.generate_straight_path(self.path_tiles, colour, boosters)
                    else:  # Floating diagonal Path
                        if random.choice([1, 1, 2]) == 1:  # Invisible
                            self.generate_diagonal_path(self.path_tiles, colour, boosters, True)
                        else:  # Visible
                            self.generate_diagonal_path(self.path_tiles, colour, boosters)
                elif generation_mode == 'double thin':
                    self.generate_double_thin_path(colour, boosters)
                elif generation_mode == 'grid':
                    self.generate_reg_grid_path(colour, boosters)
                elif generation_mode == 'transition':
                    self.generate_transition(colour, boosters)
                elif generation_mode == 'ending path':
                    self.generate_ending_path(colour)
                if self.stage >= 6:
                    self.generate_side_path(self.COLOURS[random.randint(0, 5)], boosters)

        self.collide_with_player(car)
        self.remove_paths(frames)

    def remove_paths(self, frames):  # remove paths behind player
        if self.current_path > 5 and frames % 16 == 0:
            self.path_tiles = self.path_tiles[2:]
            self.current_path -= 2

    def collide_with_player(self, car):  # test which path block player is colliding with
        for count, tile in enumerate(self.path_tiles):
            tile_rect = pygame.Rect((tile.x, tile.y, tile.length, tile.width))
            if tile_rect.colliderect(car.rect):
                if count > self.current_path:
                    self.current_path = count

    def render(self, surface, left, top, player, is_paused, is_viewing_arrows=False):  # render path and coins
        for tile in self.side_path_tiles:
            if -300 <= tile.x - left <= 800 and -300 <= tile.y - top <= 800:
                pygame.draw.rect(surface, tile.colour, (tile.x - left, tile.y - top, tile.length, tile.width))
        for tile in self.path_tiles:
            if -300 <= tile.x - left <= 800 and -300 <= tile.y - top <= 800:
                if not tile.invisible:
                    pygame.draw.rect(surface, tile.colour, (tile.x - left, tile.y - top, tile.length, tile.width))
                else:
                    pygame.draw.rect(surface, (250, 250, 250), (tile.x - left, tile.y - top, tile.length, tile.width))
                if is_viewing_arrows:
                    if tile.direction == "UP":
                        self.draw_arrow(surface, (0, 0, 0), (tile.x - left + tile.length / 2, tile.y - top + 100),
                                        (tile.x - left + tile.length / 2, tile.y - top + 50))
                    elif tile.direction == "RIGHT":
                        self.draw_arrow(surface, (0, 0, 0), (tile.x - left + 50, tile.y - top + tile.width / 2),
                                        (tile.x - left + 100, tile.y - top + tile.width / 2))
        for coin in self.coins:
            if -300 <= coin.rect.x - left <= 800 and -300 <= coin.rect.y - top <= 800:
                surface.blit(coin.image, (coin.rect.x - left, coin.rect.y - top))
        for mega_score in self.mega_scores:
            if -300 <= mega_score.x - left <= 800 and -300 <= mega_score.y - top <= 800:
                pygame.draw.circle(surface, mega_score.colour, (mega_score.x - left, mega_score.y - top),
                                   mega_score.radius)
        for mega_coin in self.mega_coins:
            if -300 <= mega_coin.x - left <= 800 and -300 <= mega_coin.y - top <= 800:
                pygame.draw.circle(surface, mega_coin.colour, (mega_coin.x - left, mega_coin.y - top), mega_coin.radius)
        for car_frag in self.car_frags:
            if -300 <= car_frag.rect.x - left <= 800 and -300 <= car_frag.rect.y - top <= 800:
                surface.blit(car_frag.image, (car_frag.rect.x - left, car_frag.rect.y - top))
        for spike in self.spikes:
            if -300 <= spike.x - left <= 800 and -300 <= spike.y - top <= 800:
                pygame.draw.polygon(surface, (255, 0, 0), [(spike.x + 20 - left, spike.y - top),
                                                           (spike.x - left, spike.y + 40 - top),
                                                           (spike.x + 40 - left, spike.y + 40 - top)])
        for enemy_car in self.enemy_cars:
            if -300 <= enemy_car.rect.x - left <= 800 and -300 <= enemy_car.rect.y - top <= 800:
                if not is_paused:
                    enemy_car.move(player)
                enemy_car.render(surface, left, top)


'''Achievements'''


class Achievement:
    rewards = [30, 60, 80, 105, 150, 225, 550, 700, 900, 1300, 1800, 2400, 4000, 7000]

    def __init__(self, name, idx):
        self.name = name
        self.achieved = False
        self.reward = Achievement.rewards[idx]
        self.claimed_rewards = False

    def has_achieved(self):
        return self.achieved

    def achieve(self):
        if not self.achieved:
            self.achieved = True

    def has_claimed_rewards(self):
        return self.claimed_rewards

    def claim_rewards(self):
        if not self.claimed_rewards:
            self.claimed_rewards = True

    def load(self, achieved, claimed_rewards):
        self.achieved = str_to_bool(achieved)
        self.claimed_rewards = str_to_bool(claimed_rewards)

    def save(self):
        return self.achieved, self.claimed_rewards


class Achievements:
    def __init__(self):
        self.achievements = [Achievement("GET A PB OF 500 SCORE", 0), Achievement("GET THE TAXI CAR", 1),
                             Achievement("BUY A LEVEL 4 BOOSTER", 2), Achievement("ACQUIRE A TOTAL OF 500 COINS", 3),
                             Achievement("REACH LEVEL 25", 4), Achievement("GET AN EPIC CAR", 5),
                             Achievement("GET A LEGENDARY CAR", 6), Achievement("GET A LV. 10 CAR", 7),
                             Achievement("UPGRADE THE RARITY OF A CAR", 8),
                             Achievement("GET 3K SCORE WITH THE GREEN CAR", 9),
                             Achievement("COMPLETE A RUN IN UNDER 2 MINUTES", 10), Achievement("REACH LEVEL 50", 11),
                             Achievement("MAX OUT THE MIDAS' CAR", 12),
                             Achievement("REACH LEVEL 51", 13)]

    def update_achievements(self, player, cars, selected_car_idx, boosters, win, ach_time):
        if player.pb >= 500 and not self.achievements[0].has_achieved():
            self.achievements[0].achieve()  # get a pb of 500 score
        if not cars[4].locked and not self.achievements[1].has_achieved():
            self.achievements[1].achieve()  # get the taxi car
        if (boosters[0].lvl >= 4 or boosters[1].lvl >= 4 or boosters[2].lvl >= 4) and \
                not self.achievements[2].has_achieved():
            self.achievements[2].achieve()  # buy a level 4 booster
        if player.coins >= 500 and not self.achievements[3].has_achieved():
            self.achievements[3].achieve()  # get 500 coins
        if player.lvl >= 25 and not self.achievements[4].has_achieved():
            self.achievements[4].achieve()  # reach level 25
        if (not cars[8].locked or not cars[9].locked or not cars[10].locked) and \
                not self.achievements[5].has_achieved():
            self.achievements[5].achieve()  # get an epic car
        if (not cars[11].locked or not cars[12].locked or not cars[13].locked or not cars[14].locked) and \
                not self.achievements[6].has_achieved():
            self.achievements[6].achieve()  # get a legendary car
        for car in cars:
            if car.lvl == 10 and not self.achievements[7].has_achieved():
                self.achievements[7].achieve()  # get a lv 10 car
                break
            if car.upgraded_rarity and not self.achievements[8].has_achieved():
                self.achievements[8].achieve()  # upgrade the rarity of a car
                break
        if player.score >= 3000 and selected_car_idx == 0 and not self.achievements[9].has_achieved():
            self.achievements[9].achieve()  # get 3k score with green car
        if win and ach_time < 120 and not self.achievements[10].has_achieved():
            self.achievements[10].achieve()  # complete a run in under 2 minutes
        if player.lvl >= 50 and not self.achievements[11].has_achieved():
            self.achievements[11].achieve()  # reach level 50
        if not cars[14].locked and cars[14].lvl == 10 and cars[14].upgraded_rarity and \
                not self.achievements[12].has_achieved():
            self.achievements[12].achieve()  # max out the midas car
        if player.lvl >= 51 and not self.achievements[13].has_achieved():
            self.achievements[13].achieve()  # reach level 51

    def get_box_coords(self):
        return [(20, 80 + c * 30, 460, 25) for c in range(len(self.achievements))]

    def render(self, display):
        starting_x, starting_y = 20, 80
        for count, achievement in enumerate(self.achievements):
            pygame.draw.rect(display,
                             Colours.colours["LIGHT GREEN"] if achievement.achieved else Colours.colours["LIGHT RED"],
                             (starting_x, starting_y + count * 30, 460, 25))
            pygame.draw.rect(display, (0, 0, 0), (starting_x, starting_y + count * 30, 460, 25), width=2)
            create_text(display, achievement.name, 16, (0, 0, 0), (starting_x + 5, starting_y + 5 + count * 30))
            if achievement.achieved and not achievement.claimed_rewards:
                create_text(display, "!", 16, (255, 0, 0), (460, starting_y + 5 + count * 30))

    def load(self, load_list):
        for c, load_item in enumerate(load_list):
            achieved, claimed_rewards = load_item
            self.achievements[c].load(achieved, claimed_rewards)

    def save(self):
        return [ach.save() for ach in self.achievements]


'''Main Loop'''


def create_text(display, text, font_size, colour, pos):
    font = pygame.font.Font('files/Quick Starter.ttf', font_size)
    x, y = pos
    display.blit(font.render(text, True, colour), (x, y))


def create_multiline_text(display, text_list, font_size, colour, pos):
    for count, text in enumerate(text_list):
        create_text(display, text, font_size, colour, (pos[0], pos[1] + (font_size + 4) * count))


def load(cars, player, achievements):
    with open('game_data/cars.csv', 'r') as f:
        cars.load(list(csv.reader(f)))
    with open('game_data/player.csv', 'r') as f:
        player.load(list(csv.reader(f)))
    with open('game_data/achievements.csv', 'r') as f:
        achievements.load(list(csv.reader(f)))
    return cars, player, achievements


def save(car_list, player_list, ach_list):
    with open('game_data/cars.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(car_list)
    with open('game_data/player.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(player_list)
    with open('game_data/achievements.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(ach_list)


def main_loop():  # main loop
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Drift Boss 2D")
    mode = "title screen"
    is_viewing_arrows = False

    exp_reqs = {[n for n in range(51)][n]: [round(40 * n ** 2.15) for n in range(51)][n] for n in range(51)}
    exp_reqs[51] = 2 * exp_reqs[50]

    boosters = [DoubleScore(), CarInsurance(), CoinRush()]
    achievements = Achievements()
    selected_achievement = 0
    run_rewards = ["COINS"] + ["XP"] + ["CAR FRAGS"] * 2
    run_reward_num, run_reward_type = 0, ""

    cars = Cars()
    selected_car_index = 0
    cars.cars[0].locked = False
    path = Path()
    player = Player(cars.cars[selected_car_index])

    if os.path.exists('game_data/cars.csv') and os.path.exists('game_data/player.csv') and os.path.exists(
            'game_data/achievements.csv'):
        cars, player, achievements = load(cars, player, achievements)

    frames, respawn_frames = 0, 180
    fps_frames = 0
    fps = 0
    s_time = time.time()
    ach_time = 0
    win = False

    while True:

        clock.tick(60)

        if mode == "title screen":  # title screen mode
            if ach_time > 0:
                ach_time = 0
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        if 105 <= x <= 105 + 90 and 400 <= y <= 400 + 90:  # reset button
                            Tk().wm_withdraw()
                            ans = messagebox.askquestion("Reset Warning",
                                                         "Do you want to reset the game? You will lose all currently saved progress.")
                            if ans == "yes":
                                boosters = [DoubleScore(), CarInsurance(), CoinRush()]
                                achievements = Achievements()
                                cars.reset()
                                cars.cars[0].locked = False
                                player.reset_game()
                        elif 205 <= x <= 205 + 90 and 400 <= y <= 400 + 90:  # play button
                            if (not cars.cars[selected_car_index].locked) and \
                                    (player.lvl >= cars.cars[selected_car_index].lvl_req):
                                boosters = [DoubleScore(), CarInsurance(), CoinRush()]
                                if cars.cars[selected_car_index].type == "The Drifter":
                                    boosters = [DoubleScore(3), CarInsurance(3), CoinRush(3)]
                                mode = 'boosters'
                        elif 305 <= x <= 305 + 90 and 400 <= y <= 400 + 90:  # quit button
                            save(cars.save(), player.save(), achievements.save())
                            pygame.quit()
                            return
                        elif 175 <= x <= 205 and 230 <= y <= 270:  # left arrow
                            selected_car_index -= 1
                            if selected_car_index == -1:
                                selected_car_index = len(cars.cars) - 1
                        elif 295 <= x <= 325 and 230 <= y <= 270:  # right arrow
                            selected_car_index += 1
                            if selected_car_index == len(cars.cars):
                                selected_car_index = 0
                        elif 197 <= x <= 197 + 95 and 325 <= y <= 325 + 40:  # buy car with coins (and car fragments)
                            if cars.cars[selected_car_index].locked and player.coins >= cars.cars[
                                selected_car_index].coin_req and \
                                    player.car_fragments >= cars.cars[selected_car_index].frag_req:
                                cars.cars[selected_car_index].locked = False
                                player.coins -= cars.cars[selected_car_index].coin_req
                                player.car_fragments -= cars.cars[selected_car_index].frag_req
                        elif 440 <= x <= 490 and 10 <= y <= 60:
                            mode = 'leveling'
                        elif 440 <= x <= 490 and 70 <= y <= 120:
                            mode = 'achievements'
                    if pygame.mouse.get_pressed(3)[2]:
                        if 230 <= x <= 230 + 40 and 207 <= y <= 230 + 80:
                            mode = 'stats'

            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))  # background
            display.blit(pygame.image.load("files/coin.png").convert_alpha(), (0, 0))  # top left coin img
            create_text(display, str(round(player.coins)), 25, (0, 0, 0), (45, 17))  # number of coins
            display.blit(pygame.image.load("files/car_fragment.png").convert_alpha(), (0, 45))
            create_text(display, str(player.car_fragments), 25, (0, 0, 0), (50, 57))  # number of car fragments
            create_text(display, f"BEST: {round(player.pb)}", 25, (0, 0, 0), (190, 15))  # best score
            create_text(display, "DRIFT", 40, (0, 0, 0), (140, 100))  # title
            create_text(display, "BOSS", 40, (0, 0, 0), (190, 140))
            create_text(display, "2D", 25, (125, 125, 125), (345, 140))
            pygame.draw.rect(display, "#0096FF", (105, 400, 90, 90))  # reset
            pygame.draw.rect(display, "#0096FF", (205, 400, 90, 90))  # play
            pygame.draw.rect(display, "#0096FF", (305, 400, 90, 90))  # quit
            pygame.draw.rect(display, "#7393B3", (105, 400, 90, 90), width=3)
            pygame.draw.rect(display, "#7393B3", (205, 400, 90, 90), width=3)
            pygame.draw.rect(display, "#7393B3", (305, 400, 90, 90), width=3)
            create_text(display, "PLAY", 18, (0, 0, 0), (220, 440))
            create_text(display, "RESET", 18, (0, 0, 0), (110, 440))
            create_text(display, "QUIT", 18, (0, 0, 0), (320, 440))
            display.blit(cars.cars[selected_car_index].image, (230, 207))
            text = f"{cars.cars[selected_car_index].type.upper()} [{cars.cars[selected_car_index].lvl} ]"
            create_text(display, text, 18, cars.cars[selected_car_index].rarity_colour, (255 - len(text) * 7, 305))
            pygame.draw.polygon(surface=display, color="#0096FF", points=[(175, 250), (205, 230), (205, 270)])
            pygame.draw.polygon(surface=display, color="#7393B3", points=[(175, 250), (205, 230), (205, 270)], width=3)
            pygame.draw.polygon(surface=display, color="#0096FF", points=[(295, 230), (295, 270), (325, 250)])
            pygame.draw.polygon(surface=display, color="#7393B3", points=[(295, 230), (295, 270), (325, 250)], width=3)
            if cars.cars[selected_car_index].locked:
                if cars.cars[selected_car_index].frag_req > 0:
                    text1 = f"{cars.cars[selected_car_index].coin_req}"
                    text2 = f"{cars.cars[selected_car_index].frag_req}" if cars.cars[
                                                                               selected_car_index].frag_req > 0 else ""
                    length = len(text1) + len(text2)
                    gap = 60 if len(text2) > 0 else 0
                    pygame.draw.rect(display, '#0096FF', (197 - length * 2 - gap / 2, 325, 95 + length * 4 + gap, 40))
                    pygame.draw.rect(display, '#7393B3', (197 - length * 2 - gap / 2, 325, 95 + length * 4 + gap, 40),
                                     width=2)
                    create_text(display, text1, 18, '#FFD700', (260 - length * 2 - gap, 338))
                    create_text(display, text2, 18, '#FFD700', (345 - length * 2 - gap / 2, 338))
                    display.blit(pygame.image.load('files/coin.png').convert_alpha(), (190 - length * 2 - gap / 2, 320))
                    car_frag_img = pygame.image.load('files/car_fragment.png').convert_alpha()
                    car_frag_img = pygame.transform.scale(car_frag_img, (40, 40))
                    display.blit(car_frag_img, (190 + len(text1) * 2 + gap, 325))
                else:
                    text = f"{cars.cars[selected_car_index].coin_req}"
                    pygame.draw.rect(display, '#0096FF', (197 - len(text) * 2, 325, 95 + len(text) * 4, 40))
                    pygame.draw.rect(display, '#7393B3', (197 - len(text) * 2, 325, 95 + len(text) * 4, 40), width=2)
                    create_text(display, text, 18, '#FFD700', (260 - len(text) * 8, 338))
                    display.blit(pygame.image.load('files/coin.png').convert_alpha(), (190 - len(text) * 2, 320))

            if (0 < cars.cars[selected_car_index].lvl_req) and \
                    (not player.lvl >= cars.cars[selected_car_index].lvl_req):
                create_text(display, f"REQUIRES LEVEL {cars.cars[selected_car_index].lvl_req}", 12, (255, 0, 0),
                            (165, 380))
            pygame.draw.rect(display, '#0096FF', (440, 10, 50, 50))
            pygame.draw.rect(display, '#7393B3', (440, 10, 50, 50), width=3)
            if len(str(player.lvl)) == 1:
                create_text(display, f'{player.lvl}', 18, (0, 0, 0), (457, 28))
            else:
                create_text(display, f'{player.lvl}', 18, (0, 0, 0), (450, 28))
            pygame.draw.rect(display, '#0096FF', (440, 70, 50, 50))
            pygame.draw.rect(display, '#7393B3', (440, 70, 50, 50), width=3)
            create_text(display, 'A', 20, (0, 0, 0), (455, 88))

        elif mode == "stats":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        x, y = pygame.mouse.get_pos()
                        if 440 <= x <= 440 + 50 and 10 <= y <= 10 + 50:  # back to title screen
                            mode = "title screen"
                        elif 305 <= x <= 305 + 165 and 375 <= y <= 375 + 40:  # upgrade car level (max lv. 10)
                            player.coins = cars.cars[selected_car_index].upgrade_lvl(player.coins)
                        elif 305 <= x <= 305 + 165 and 430 <= y <= 430 + 40:  # upgrade rarity of car
                            player.coins = cars.cars[selected_car_index].upgrade_rarity(player.coins)
            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))  # background
            create_text(display, 'STATS', 28, (0, 0, 0), (200, 20))
            pygame.draw.rect(display, "#0096FF", (440, 10, 50, 50))
            pygame.draw.rect(display, "#7393B3", (440, 10, 50, 50), width=2)
            create_text(display, 'BACK', 14, (0, 0, 0), (440, 27))
            display.blit(pygame.image.load("files/coin.png").convert_alpha(), (0, 0))  # top left coin img
            create_text(display, str(round(player.coins)), 25, (0, 0, 0), (45, 17))  # number of coins
            display.blit(pygame.image.load("files/car_fragment.png").convert_alpha(), (0, 45))
            create_text(display, str(player.car_fragments), 25, (0, 0, 0), (50, 57))  # number of car fragments
            pygame.draw.rect(display, (150, 150, 150), (10, 90, 270, 400))
            pygame.draw.rect(display, (100, 100, 100), (10, 90, 270, 400), width=3)
            pygame.draw.rect(display, (150, 150, 150), (285, 90, 205, 400))
            pygame.draw.rect(display, (100, 100, 100), (285, 90, 205, 400), width=3)
            car_img = pygame.transform.scale(cars.cars[selected_car_index].image, (80, 160))
            display.blit(car_img, (350, 140))
            create_text(display, "PREVIEW: ", 18, (0, 0, 0), (330, 100))
            colour1 = '#FFD700' if cars.cars[selected_car_index].lvl < 10 else (200, 200, 200)
            colour2 = '#FFD700' if not cars.cars[selected_car_index].upgraded_rarity else (200, 200, 200)
            pygame.draw.rect(display, colour1, (305, 375, 165, 40))
            pygame.draw.rect(display, (100, 100, 100), (305, 375, 165, 40), width=2)
            pygame.draw.rect(display, colour2, (305, 430, 165, 40))
            pygame.draw.rect(display, (100, 100, 100), (305, 430, 165, 40), width=2)
            create_text(display, f'UPGRADE ({cars.cars[selected_car_index].lvl_cost})', 14, (0, 0, 0), (310, 385))
            create_text(display, f'+1 RARITY ({cars.cars[selected_car_index].upgrade_rarity_cost})', 14, (0, 0, 0),
                        (310, 440))
            text = f"{cars.cars[selected_car_index].type.upper()}"
            create_text(display, text, 18, cars.cars[selected_car_index].rarity_colour,
                        ((270 - len(text) * 14) // 2 + 10, 100))
            create_text(display, f"RARITY: {cars.cars[selected_car_index].rarity}", 16, (0, 0, 0), (15, 145))
            create_text(display, f"LEVEL: {cars.cars[selected_car_index].lvl}", 16, (0, 0, 0), (15, 170))
            create_text(display, f"DRIFT ANGLE: {round(cars.cars[selected_car_index].car_drift_angle, 2)}", 16,
                        (0, 0, 0),
                        (15, 195))
            if cars.cars[selected_car_index].flight_regen_rate is not None:
                create_text(display, f"FLIGHT TIME: {round(cars.cars[selected_car_index].flight_duration, 2)}", 16,
                            (0, 0, 0),
                            (15, 220))
                create_text(display, f"FLIGHT REGEN: {round(cars.cars[selected_car_index].flight_regen_rate, 2)}", 16,
                            (0, 0, 0),
                            (15, 245))
                abilities_start_y = 245 + 16 + 12
            else:
                abilities_start_y = 195 + 16 + 12
            if cars.cars[selected_car_index].ability == "the drifter":
                create_multiline_text(display, ["ABILITY:", "GAIN +3 BASE LEVELS", "PER BOOSTER"], 16, (0, 0, 0),
                                      (15, abilities_start_y))
            elif cars.cars[selected_car_index].ability == "timewarp":
                create_multiline_text(display,
                                      ["ABILITY 1 (PRESS 4):", "LOSE 50% OF YOUR", "SPEED FOR 5 S ", "(25% FD COST)"],
                                      16, (0, 0, 0), (15, abilities_start_y))
                create_multiline_text(display, ["ABILITY 2 (PRESS 5):", "TELEPORT 4 TILES", "FORWARD AND GAIN",
                                                "+50% SCORE AND COINS", "FOR 5 S (25% FD COST)"], 16, (0, 0, 0),
                                      (15, abilities_start_y + 16 * 5 + 12))
            elif cars.cars[selected_car_index].ability == "fortunate":
                create_multiline_text(display,
                                      ["ABILITY: ", "SACRIFICE ALL SCORE", "TO GAIN 1 COIN", "PER SCORE YOU GAIN"], 16,
                                      (0, 0, 0), (15, abilities_start_y))
            elif cars.cars[selected_car_index].ability == "midas car":
                create_multiline_text(display,
                                      ["ABILITY: ", "SACRIFICE ALL COINS", "TO GAIN 25 SCORE", "PER COIN YOU PICK UP"],
                                      16, (0, 0, 0), (15, abilities_start_y))

        elif mode == "leveling":  # leveling menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        x, y = pygame.mouse.get_pos()
                        if 440 <= x <= 490 and 10 <= y <= 60:
                            mode = 'title screen'

            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))  # background
            pygame.draw.rect(display, '#0096FF', (440, 10, 50, 50))
            pygame.draw.rect(display, '#7393B3', (440, 10, 50, 50), width=3)
            create_text(display, 'BACK', 14, (0, 0, 0), (440, 28))
            create_text(display, 'DRIFT BOSS', 30, (0, 0, 0), (115, 15))
            create_text(display, '2D', 20, (150, 150, 150), (370, 15))
            create_text(display, f'LEVEL {player.lvl}', 25, (255, 0, 0), (180, 100))
            pygame.draw.rect(display, '#1d2951', (50, 135, 400, 25))
            try:
                exp_to_next_lvl = exp_reqs[player.lvl + 1] - player.exp
                total_exp_to_next_lvl = exp_reqs[player.lvl + 1] - exp_reqs[player.lvl]
                dec_exp_to_next_lvl = (total_exp_to_next_lvl - exp_to_next_lvl) / total_exp_to_next_lvl
                pygame.draw.rect(display, '#0096FF', (50, 135, 400 * dec_exp_to_next_lvl, 25))
            except KeyError:
                exp_to_next_lvl, total_exp_to_next_lvl, dec_exp_to_next_lvl = 0, 0, 0
                pygame.draw.rect(display, '#FFD700', (50, 135, 400, 25))
            pygame.draw.rect(display, (0, 0, 0), (50, 135, 400, 25), width=3)
            if player.lvl < 51:
                create_text(display, f'{round(exp_to_next_lvl)} EXP TO NEXT LVL ({round(dec_exp_to_next_lvl * 100)}%)', 18,
                            (0, 0, 0), (95, 165))
            else:
                create_text(display, "ALL MAXED", 18, (0, 0, 0), (185, 165))
            txt = f'TOTAL EXP: {round(player.exp)}'
            create_text(display, txt, 18, (0, 0, 0), (160 - len(txt), 200))
            pygame.draw.rect(display, (160, 160, 160), (130, 230, 240, 250))
            pygame.draw.rect(display, (100, 100, 100), (130, 230, 240, 250), width=3)
            create_text(display, 'BONUSES:', 20, (0, 0, 0), (185, 245))
            if player.lvl_bonus > 0:
                create_multiline_text(display, [f'GAIN A +{round(100 * player.lvl_bonus, 3)}%', 'BOOST IN ALL',
                                                'STATS DURING', 'RUNS'], 18, (0, 0, 0), (135, 280))

        elif mode == 'achievements':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        x, y = pygame.mouse.get_pos()
                        if 440 <= x <= 490 and 10 <= y <= 60:
                            mode = 'title screen'
                        for c, achievement_box_coords in enumerate(achievements.get_box_coords()):
                            sx, sy, l, w = achievement_box_coords
                            if sx <= x <= sx + l and sy <= y <= sy + w:
                                if achievements.achievements[c].has_achieved() and \
                                        not achievements.achievements[c].has_claimed_rewards():
                                    selected_achievement = c
                                    mode = 'achievement reward'
                                    break
            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))  # background
            pygame.draw.rect(display, '#0096FF', (440, 10, 50, 50))
            pygame.draw.rect(display, '#7393B3', (440, 10, 50, 50), width=3)
            create_text(display, 'BACK', 14, (0, 0, 0), (440, 28))
            create_text(display, 'ACHIEVEMENTS', 30, (0, 0, 0), (80, 15))
            achievements.render(display)

        elif mode == 'achievement reward':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        x, y = pygame.mouse.get_pos()
                        if 180 <= x <= 180 + 150 and 250 <= y <= 250 + 150:
                            player.update_exp(exp_reqs)
                            player.reset()
                            player.coins += achievements.achievements[selected_achievement].reward
                            achievements.achievements[selected_achievement].claim_rewards()
                            mode = 'achievements'

            display.fill("#90EE90")
            create_text(display, 'REWARDS', 40, (0, 0, 0), (120, 75))
            create_text(display, f'YOU GET {achievements.achievements[selected_achievement].reward} COINS', 22,
                        (0, 0, 0), (110, 200))
            pygame.draw.rect(display, (150, 150, 150), (180, 250, 150, 150))
            pygame.draw.rect(display, (100, 100, 100), (180, 250, 150, 150), width=3)
            create_text(display, 'BACK', 25, (0, 0, 0), (210, 310))

        elif mode == "boosters":  # boosters menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed(3)[0]:
                        if 60 <= x <= 60 + 90 and 312 <= y <= 312 + 40:
                            player.coins = boosters[0].increment_level(player.coins)
                        elif 60 + 140 <= x <= 60 + 140 + 90 and 312 <= y <= 312 + 40:
                            player.coins = boosters[1].increment_level(player.coins)
                        elif 60 + 140 * 2 <= x <= 60 + 140 * 2 + 90 and 312 <= y <= 312 + 40:
                            player.coins = boosters[2].increment_level(player.coins)
                        elif 205 <= x <= 205 + 90 and 380 <= y <= 380 + 90:
                            path = Path()
                            player.set_car_type(cars.cars[selected_car_index])
                            win = False
                            mode = 'game'
                    elif pygame.mouse.get_pressed(3)[2]:
                        if 45 <= x <= 45 + 125 and 180 <= y <= 180 + 125:
                            mode = "double score stats"
                        elif 45 + 140 * 1 <= x <= 45 + 140 * 1 + 125 and 180 <= y <= 180 + 125:
                            mode = "car insurance stats"
                        elif 45 + 140 * 2 <= x <= 45 + 140 * 2 + 125 and 180 <= y <= 180 + 125:
                            mode = "coin rush stats"

            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))
            display.blit(pygame.image.load("files/coin.png").convert_alpha(), (0, 0))  # top left coin img
            create_text(display, str(round(player.coins)), 25, (0, 0, 0), (45, 17))  # number of coins
            display.blit(pygame.image.load("files/car_fragment.png").convert_alpha(), (0, 45))
            create_text(display, str(player.car_fragments), 25, (0, 0, 0), (50, 57))  # number of car fragments
            create_text(display, "SELECT", 30, (0, 0, 0), (170, 80))
            create_text(display, "BOOSTERS", 30, (0, 0, 0), (140, 120))
            for n in range(3):
                pygame.draw.rect(display, boosters[n].colour, (45 + 140 * n, 180, 125, 125))
                pygame.draw.rect(display, '#7393B3', (45 + 140 * n, 180, 125, 125), width=3)
                if boosters[n].lvl > 0:
                    create_text(display, f'{boosters[n].lvl}', 14, '#FFD700', (148 + 140 * n, 285))
                pygame.draw.rect(display, '#0096FF', (60 + n * 140, 312, 90, 40))
                pygame.draw.rect(display, '#7393B3', (60 + n * 140, 312, 90, 40), width=3)
                display.blit(pygame.image.load('files/coin.png').convert_alpha(), (60 + n * 140, 305))
                create_text(display, f'{boosters[n].cost}', 20, '#FFD700', (105 + n * 140, 323))
            create_text(display, 'DOUBLE', 16, (0, 0, 0), (65, 225))
            create_text(display, 'SCORE', 16, (0, 0, 0), (70, 245))
            create_text(display, 'CAR', 16, (0, 0, 0), (225, 225))
            create_text(display, 'INSURANCE', 16, (0, 0, 0), (185, 245))
            create_text(display, 'COIN', 16, (0, 0, 0), (365, 225))
            create_text(display, 'RUSH', 16, (0, 0, 0), (360, 245))
            pygame.draw.rect(display, "#0096FF", (205, 380, 90, 90))
            pygame.draw.rect(display, "#7393B3", (205, 380, 90, 90), width=3)
            create_text(display, 'PLAY', 18, (0, 0, 0), (220, 420))

        elif mode == "double score stats":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed(3)[0]:
                        if 440 <= x <= 440 + 50 and 10 <= y <= 10 + 50:
                            mode = "boosters"

            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))  # background
            pygame.draw.rect(display, "#0096FF", (440, 10, 50, 50))
            pygame.draw.rect(display, "#7393B3", (440, 10, 50, 50), width=2)
            create_text(display, 'BACK', 14, (0, 0, 0), (440, 27))
            create_text(display, 'DOUBLE SCORE', 28, (0, 0, 0), (95, 15))
            pygame.draw.rect(display, (160, 160, 160), (100, 120, 300, 340))
            pygame.draw.rect(display, (100, 100, 100), (100, 120, 300, 340), width=3)
            create_text(display, 'ABILITIES: ', 23, (0, 0, 0), (170, 140))
            create_multiline_text(display, ['[LV. 1+] GAIN +40% MORE', 'SCORE PER LEVEL'], 15, (0, 0, 0), (110, 180))
            create_multiline_text(display, ['[LV. 4+] CONSUME ALL', 'FLIGHT TO GAIN A SCORE ',
                                            'BOOST FOR 15 S + 5 S', 'PER LEVEL ABOVE LV. 4', '(PRESS 1)'], 15,
                                  (0, 0, 0), (110, 245))
            create_multiline_text(display, ['[LV. 7] MEGA SCORE DOTS', 'SPAWN ON PATH, GAIN', '300 SCORE WHEN',
                                            'PICKED UP (RED)'], 15,
                                  (0, 0, 0), (110, 370))

        elif mode == "car insurance stats":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed(3)[0]:
                        if 440 <= x <= 440 + 50 and 10 <= y <= 10 + 50:
                            mode = "boosters"

            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))  # background
            pygame.draw.rect(display, "#0096FF", (440, 10, 50, 50))
            pygame.draw.rect(display, "#7393B3", (440, 10, 50, 50), width=2)
            create_text(display, 'BACK', 14, (0, 0, 0), (440, 27))
            create_text(display, 'CAR INSURANCE', 28, (0, 0, 0), (85, 15))
            pygame.draw.rect(display, (160, 160, 160), (100, 120, 300, 340))
            pygame.draw.rect(display, (100, 100, 100), (100, 120, 300, 340), width=3)
            create_text(display, 'ABILITIES: ', 23, (0, 0, 0), (170, 140))
            create_multiline_text(display, ['[LV. 1+] GAIN 1 EXTRA', 'LIFE ON LVLS 1, 2, 3, AND 6'], 14, (0, 0, 0),
                                  (110, 180))
            create_multiline_text(display,
                                  ['[LV. 4+] REDUCE FLIGHT', 'COST BY 16.7%', 'PER LEVEL ABOVE LV.4',
                                   'AND RESPAWN INSTANTLY',
                                   'WITH MAX FLIGHT IF YOU DIE'],
                                  14,
                                  (0, 0, 0), (110, 230))
            create_multiline_text(display, ['[LV. 7] CONSUME ALL', 'FLIGHT TO GAIN', 'INVINCIBILITY FOR 5 S',
                                            'AND 2X FLIGHT REGEN', 'WHILST CUTTING SCORE', 'AND COINS BY 50%',
                                            '(PRESS 3)'],
                                  14, (0, 0, 0), (110, 325))

        elif mode == "coin rush stats":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed(3)[0]:
                        if 440 <= x <= 440 + 50 and 10 <= y <= 10 + 50:
                            mode = "boosters"

            display.blit(pygame.image.load("files/bg.png").convert_alpha(), (0, 0))  # background
            pygame.draw.rect(display, "#0096FF", (440, 10, 50, 50))
            pygame.draw.rect(display, "#7393B3", (440, 10, 50, 50), width=2)
            create_text(display, 'BACK', 14, (0, 0, 0), (440, 27))
            create_text(display, 'COIN RUSH', 28, (0, 0, 0), (140, 15))
            pygame.draw.rect(display, (160, 160, 160), (100, 120, 300, 340))
            pygame.draw.rect(display, (100, 100, 100), (100, 120, 300, 340), width=3)
            create_text(display, 'ABILITIES: ', 23, (0, 0, 0), (170, 140))
            create_multiline_text(display, ['[LV. 1+] GAIN A +25%', 'CHANCE TO SPAWN', 'COINS PER LEVEL'], 15,
                                  (0, 0, 0), (110, 180))
            create_multiline_text(display, ['[LV. 4+] CONSUME ALL', 'FLIGHT TO GAIN A COIN ',
                                            'BOOST FOR 15 S + 5 S', 'PER LEVEL ABOVE LV. 4', '(PRESS 2)'], 15,
                                  (0, 0, 0), (110, 255))
            create_multiline_text(display,
                                  ['[LV. 7] MEGA COINS', 'SPAWN ON PATH, GAIN', '200 COINS WHEN', 'PICKED UP (BLUE)'],
                                  15, (0, 0, 0), (110, 370))

        elif mode == "game":  # gameplay mode
            frames += 1
            fps_frames += 1
            e_time = time.time()
            if e_time - s_time >= 1:
                fps = fps_frames
                fps_frames = 0
                s_time = time.time()
                ach_time += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and boosters[0].lvl >= 4:
                        if player.flight_duration == player.max_flight_duration and player.max_flight_duration > 0:
                            player.use_ds2_ability(boosters)  # use double score second perk ability
                    if event.key == pygame.K_2 and boosters[2].lvl >= 4:
                        if player.flight_duration == player.max_flight_duration and player.max_flight_duration > 0:
                            player.use_cr2_ability(boosters)  # use coin rush second perk ability
                    if event.key == pygame.K_3 and boosters[1].lvl == 7:
                        if player.flight_duration >= player.max_flight_duration / 2 and player.max_flight_duration > 0:
                            player.use_ci3_ability(boosters)  # use car insurance third perk ability
                    if event.key == pygame.K_4:
                        if cars.cars[selected_car_index].type == "Timewarp" and player.max_flight_duration > 0 and \
                                (player.flight_duration / player.max_flight_duration) >= 0.25:
                            player.use_timewarp_lc_ability()
                    if event.key == pygame.K_5:
                        if cars.cars[selected_car_index].type == "Timewarp" and player.max_flight_duration > 0 and \
                                (player.flight_duration / player.max_flight_duration) >= 0.25:
                            player.use_timewarp_rc_ability()
                    if event.key == pygame.K_a:
                        is_viewing_arrows = not is_viewing_arrows
                    if event.key == pygame.K_p:
                        mode = "pause screen"

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                player.move_right()
            else:
                player.move_up()
            left = player.position.x - 230
            top = player.position.y - 250

            if not player.collide_path(path):  # check if player goes off path
                if not boosters[1].is_active():
                    if player.flight_duration > 0:  # check if car has available flight duration
                        player.fly(frames)
                        player.isFlying = True
                        flight_regen_amount = boosters[1].get_flight_regen_amount()
                        if flight_regen_amount is not None:  # regenerate flight duration while flying
                            player.use_ci2_ability(frames, flight_regen_amount)
                    else:
                        if boosters[1].get_num_lives() > 0:  # respawn
                            if boosters[1].lvl < 4:
                                try:  # go back to position 120 frames before
                                    player.position = player.prev_pos_list[-120]
                                    player.rect.center = player.prev_pos_list[-120]
                                    player.heading = player.prev_heading_list[-120]
                                except IndexError:
                                    player.position = player.prev_pos_list[0]
                                    player.rect.center = player.prev_pos_list[0]
                                    player.heading = player.prev_heading_list[0]
                                left = player.position[0] - 230
                                top = player.position[1] - 250
                                player.update(left, top)
                                respawn_frames = 180
                                mode = "respawn screen"
                            else:
                                player.flight_duration = player.max_flight_duration
                            boosters[1].deduct_life()  # remove 1 life
                        else:  # game over
                            mode = "death screen"
                else:
                    player.regenerate_flight_duration(frames, boosters)
                    if player.flight_duration > player.max_flight_duration:
                        player.flight_duration = player.max_flight_duration
            else:
                player.isFlying = False
                player.regenerate_flight_duration(frames, boosters)
                if player.flight_duration > player.max_flight_duration:
                    player.flight_duration = player.max_flight_duration

            path.coins = player.collect_coins(path.coins, boosters)  # collect coins on path
            if boosters[0].lvl == 7:
                path.mega_scores = player.collect_mega_scores(path.mega_scores)  # collect mega scores on path
            if boosters[2].lvl == 7:
                path.mega_coins = player.collect_mega_coins(path.mega_coins)  # collect mega coins on path
            path.car_frags = player.collect_car_frags(path.car_frags)  # collect car fragments on path
            player.collide_with_spikes(frames, path.spikes)

            if player.is_colliding_with_enemy_car(path.enemy_cars) and not boosters[1].is_active():
                if boosters[1].lives > 0:
                    if player.flight_duration > player.max_flight_duration:
                        player.flight_duration = player.max_flight_duration
                    boosters[1].deduct_life()
                else:
                    mode = "death screen"
            ending_tile_rect = pygame.Rect((path.path_tiles[-1].x, path.path_tiles[-1].y, 150, 150))
            if player.rect.colliderect(ending_tile_rect) and path.has_finished:
                run_reward_type = random.choice(run_rewards)
                if run_reward_type == "COINS":
                    run_reward_num = random.randint(300, 1000)
                elif run_reward_type == "XP":
                    run_reward_num = random.randint(1000, 4000)
                else:
                    run_reward_num = random.randint(1, 5)
                mode = "win screen"

            display.fill((255, 255, 255))  # fill background white
            path.generate_path(frames, player, boosters)  # generate new path sections
            path.render(display, left, top, player, False, is_viewing_arrows)  # render path

            player.update_ability_times(frames, boosters)
            player.update(left, top)  # update car position
            player.render(display, left, top)
            player.increment_score(frames, boosters)  # increment player score
            player.render_text(display, boosters)  # render number of coins and score
            if player.flight_regen_rate is not None:  # has flight ability
                pygame.draw.rect(display, '#1d2951', (130, 450, 200, 40))
                if player.flight_duration > 0:
                    pygame.draw.rect(display, '#0096FF',
                                     (130, 450, round(200 * player.flight_duration / player.max_flight_duration), 40))
                pygame.draw.rect(display, (0, 0, 0), (130, 450, 200, 40), width=3)
                text = f"{round(player.flight_duration)}/{round(player.max_flight_duration)}"
                create_text(display, text, 25, (0, 0, 0), (195 - len(text), 430))
            create_text(display, f"FPS: {fps}", 25, (0, 0, 0), (360, 20))
            create_text(display, f"TIME: {round(ach_time)}", 18, (0, 0, 0), (10, 470))

        elif mode == "pause screen":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        mode = "game"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed(3)[0]:
                        if 440 <= x <= 440 + 50 and 10 <= y <= 10 + 50:
                            player.update_exp(exp_reqs)
                            player.reset()
                            mode = "title screen"

            left = player.position[0] - 230
            top = player.position[1] - 250
            display.fill((255, 255, 255))
            path.render(display, left, top, player, True)
            display.blit(player.image, (player.rect.x - left, player.rect.y - top))
            player.render_text(display, boosters)  # render number of coins and score
            create_text(display, f'GAME PAUSED', 25, (255, 0, 0), (120, 225))
            pygame.draw.rect(display, "#0096FF", (440, 10, 50, 50))
            pygame.draw.rect(display, "#7393B3", (440, 10, 50, 50), width=2)
            create_text(display, 'BACK', 14, (0, 0, 0), (440, 27))

        elif mode == "respawn screen":  # screen for when player respawns
            player.flight_duration = player.max_flight_duration
            respawn_frames -= 1
            left = player.position[0] - 230
            top = player.position[1] - 250
            display.fill((255, 255, 255))
            path.render(display, left, top, player, True)
            display.blit(player.image, (player.rect.x - left, player.rect.y - top))
            player.render_text(display, boosters)  # render number of coins and score
            create_text(display, f'RESPAWNING IN {(respawn_frames // 60) + 1}', 25, (255, 0, 0),
                        (90, 225))  # render respawn timer
            if respawn_frames == 0:
                mode = "game"

        elif mode == "death screen":  # screen for when player dies
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        x, y = pygame.mouse.get_pos()
                        if 180 <= x <= 180 + 150 and 250 <= y <= 250 + 150:
                            player.update_exp(exp_reqs)
                            player.reset()
                            mode = 'title screen'

            display.fill("#ffcccb")
            create_text(display, 'GAME OVER', 40, (0, 0, 0), (100, 75))
            create_text(display, f'SCORE: {round(player.score)}', 25, (0, 0, 0), (170, 160))
            pygame.draw.rect(display, (150, 150, 150), (180, 250, 150, 150))
            pygame.draw.rect(display, (100, 100, 100), (180, 250, 150, 150), width=3)
            create_text(display, 'TITLE', 20, (0, 0, 0), (215, 300))
            create_text(display, 'SCREEN', 20, (0, 0, 0), (200, 330))

        elif mode == "win screen":
            if not win:
                win = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save(cars.save(), player.save(), achievements.save())
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]:
                        x, y = pygame.mouse.get_pos()
                        if 180 <= x <= 180 + 150 and 250 <= y <= 250 + 150:
                            player.update_exp(exp_reqs)
                            player.reset()
                            if run_reward_type == "COINS":
                                player.coins += run_reward_num
                            elif run_reward_type == "XP":
                                player.exp += run_reward_num
                            else:
                                player.car_fragments += run_reward_num
                            mode = 'title screen'

            display.fill("#90EE90")
            create_text(display, 'YOU WON', 40, (0, 0, 0), (120, 75))
            create_text(display, f'SCORE: {round(player.score)}', 25, (0, 0, 0), (170, 160))
            reward_text = f'REWARD: {run_reward_num} {run_reward_type}'
            create_text(display, reward_text, 22, (0, 0, 0), (130 - len(reward_text) * 2, 200))
            pygame.draw.rect(display, (150, 150, 150), (180, 250, 150, 150))
            pygame.draw.rect(display, (100, 100, 100), (180, 250, 150, 150), width=3)
            create_text(display, 'TITLE', 20, (0, 0, 0), (215, 300))
            create_text(display, 'SCREEN', 20, (0, 0, 0), (200, 330))

        achievements.update_achievements(player, cars.cars, selected_car_index, boosters, win, ach_time)
        pygame.display.flip()


main_loop()
