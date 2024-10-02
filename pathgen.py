import math
import random

from general import *

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
                    self.coins.append(
                        Coin(last.x + (last.length - 50) / 2, last.y + (last.width - 50) / 2))  # Generate 1 coin

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
