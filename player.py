import random
import math

from general import *

'''Player and Selected Car Stats File'''


class CarSprite(pygame.sprite.Sprite):
    def __init__(self, car, lvl_bonus):

        pygame.sprite.Sprite.__init__(self)
        self.car = car
        self.image = car.image

        self.car_drift_angle = self.car.car_drift_angle * (1 + lvl_bonus)
        self.max_health = 100 + self.car.health * (1 + lvl_bonus)
        self.health = 100 + self.car.health * (1 + lvl_bonus)
        self.health_regen = self.car.health_regen * (1 + lvl_bonus)
        self.max_mana = 100 + self.car.mana * (1 + lvl_bonus)
        self.mana = 100 + self.car.mana * (1 + lvl_bonus)
        self.mana_regen = self.car.mana_regen * (1 + lvl_bonus)
        self.score_wisdom = self.car.score_wisdom * (1 + lvl_bonus)
        self.coin_wisdom = self.car.coin_wisdom * (1 + lvl_bonus)

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
        if frames % 15 == 0:
            if self.health > 0:
                self.health -= 25

    def regenerate_health(self, frames):  # regenerate mana when on path
        if frames % 60 == 0:
            if self.health < self.max_health:
                self.health += 5 * (1 + self.health_regen / 100)

    def regenerate_mana(self, frames):
        if frames % 60 == 0:
            if self.mana < self.max_mana:
                self.mana += 5 * (1 + self.mana_regen / 100)

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
    lvl_bonuses = {[n for n in range(101)][n]: [round(0.12 * n ** 1.6, 4) for n in range(101)][n] for n in range(101)}

    def __init__(self, car):
        self.car_type = car
        self.score, self.pb = 0, 0
        self.coins, self.car_fragments = 0, 0
        self.lvl, self.exp = 0, 0
        self.lvl_bonus = 0.0
        self.timewarp_ability_time = 0

        super().__init__(self.car_type, self.lvl_bonus)

    def get_coin_multiplier(self, boosters):
        mult = 1 + self.lvl_bonus + self.coin_wisdom / 100
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
        if self.timewarp_ability_time > 0:
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
                    self.health -= self.max_health / 2
                    if self.health < 0:
                        self.health = 0

    def is_colliding_with_enemy_car(self, enemy_cars):
        for enemy_car in enemy_cars:
            if enemy_car.rect.colliderect(self.rect):
                return True
        else:
            return False

    def get_score_multiplier(self, boosters):
        mult = 1 + self.lvl_bonus + boosters[0].get_score_multiplier() + self.score_wisdom / 100
        if boosters[0].is_active():
            mult += boosters[0].get_ability_score_multiplier()
        if boosters[1].is_active():
            mult /= 2
        if self.timewarp_ability_time > 0:
            mult *= 1.5
        return mult

    def increment_score(self, f, boosters):  # increment player score
        if f % 8 == 0:
            if self.car_type.type != "Fortunate":
                self.score += self.get_score_multiplier(boosters)
            if self.car_type.type == "Fortunate":
                self.coins += self.get_score_multiplier(boosters)

    def use_ds2_ability(self, boosters):
        boosters[0].set_ability_score_multiplier(self.mana)
        self.mana -= 100

    def use_cr2_ability(self, boosters):
        boosters[2].set_ability_coin_multiplier(self.mana)
        self.mana -= 100

    def use_ci1_ability(self, boosters):
        self.health += self.max_health * boosters[1].get_instant_heal_amount() / 100
        self.mana -= 50

    def use_ci3_ability(self, boosters):
        boosters[1].set_invincibility_time()
        self.mana -= 50

    def teleport(self):
        angle = abs(self.heading)
        self.position[0] += 4 * 150 * math.cos(math.radians(angle))
        self.position[1] -= 4 * 150 * math.sin(math.radians(angle))

    def use_timewarp_ability(self):
        self.timewarp_ability_time = 5
        self.mana -= 25
        self.teleport()

    def update_ability_times(self, f, boosters):
        if f % 60 == 0:
            if boosters[0].is_active():
                boosters[0].deduct_ability_time()
            if boosters[2].is_active():
                boosters[2].deduct_ability_time()
            if boosters[1].is_active():
                boosters[1].deduct_ability_time()
            if self.timewarp_ability_time > 0:
                self.timewarp_ability_time -= 1

    def update_exp(self, exp_reqs):
        self.exp += self.score
        prev_lvl = self.lvl
        for key, value in exp_reqs.items():
            if self.exp < value:
                self.lvl = key - 1
                break
        if self.exp > exp_reqs[100]:
            self.lvl = 100
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
        txt = f'LIVES: {boosters[1].get_num_lives()}'
        create_text(surface, txt, 22, (0, 0, 0), (530 - len(txt) * 22, 80))  # render remaining lives
        if self.max_mana > 0 and boosters[0].lvl >= 4 and boosters[0].rem_time > 0:
            create_text(surface, f'A1: {boosters[0].rem_time}', 20, (255, 0, 0), (405, 370))
        if self.max_mana > 0 and boosters[2].lvl >= 4 and boosters[2].rem_time > 0:
            create_text(surface, f'A2: {boosters[2].rem_time}', 20, (0, 0, 255), (405, 390))
        if self.max_mana > 0 and boosters[1].lvl == 7 and boosters[1].rem_time > 0:
            create_text(surface, f'A3: {boosters[1].rem_time}', 20, (0, 255, 0), (405, 410))
        if self.timewarp_ability_time > 0:
            create_text(surface, f'TW: {self.timewarp_ability_time}', 20, (0, 255, 255), (400, 350))

        # draw health bar
        pygame.draw.rect(surface, '#800000', (50, 450, 190, 30))
        if self.health > 0:
            pygame.draw.rect(surface, '#FF6347', (50, 450, round(190 * self.health / self.max_health), 30))
        pygame.draw.rect(surface, (0, 0, 0), (50, 450, 190, 30), width=3)
        text = f"HP {round(self.health)}/{round(self.max_health)}"
        create_text(surface, text, 20, (0, 0, 0), (80 - len(text), 430))

        # draw mana bar
        pygame.draw.rect(surface, '#1d2951', (270, 450, 190, 30))
        if self.mana > 0:
            pygame.draw.rect(surface, '#0096FF', (270, 450, round(190 * self.mana / self.max_mana), 30))
        pygame.draw.rect(surface, (0, 0, 0), (270, 450, 190, 30), width=3)
        text = f"MANA {round(self.mana)}/{round(self.max_mana)}"
        create_text(surface, text, 20, (0, 0, 0), (300 - len(text), 430))

    def load(self, load_dict):
        pb, coins, car_fragments, lvl, exp = list(load_dict.values())
        self.pb = pb
        self.coins = coins
        self.car_fragments = car_fragments
        self.lvl = lvl
        self.exp = exp
        self.lvl_bonus = Player.lvl_bonuses[self.lvl] / 100
        super().__init__(self.car_type, self.lvl_bonus)

    def save(self):
        return {"pb": self.pb, "coins": self.coins, "car fragments": self.car_fragments, "lvl": self.lvl, "exp": self.exp}
