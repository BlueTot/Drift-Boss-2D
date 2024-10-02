from general import *

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
        self.achieved = achieved
        self.claimed_rewards = claimed_rewards

    def save(self):
        return {"achieved": self.achieved, "claimed rewards": self.claimed_rewards}


class Achievements:
    def __init__(self):
        self.achievements = [Achievement("GET A PB OF 500 SCORE", 0), Achievement("GET THE TAXI CAR", 1),
                             Achievement("BUY A LEVEL 4 BOOSTER", 2), Achievement("ACQUIRE A TOTAL OF 500 COINS", 3),
                             Achievement("REACH LEVEL 25", 4), Achievement("GET AN EPIC CAR", 5),
                             Achievement("GET A LEGENDARY CAR", 6), Achievement("GET A LV. 5 CAR", 7),
                             Achievement("UPGRADE THE RARITY OF A CAR", 8),
                             Achievement("GET 3K SCORE WITH THE GREEN CAR", 9),
                             Achievement("COMPLETE A RUN IN UNDER 2 MINUTES", 10), Achievement("REACH LEVEL 50", 11),
                             Achievement("MAX OUT THE MIDAS' CAR", 12),
                             Achievement("REACH LEVEL 100", 13)]

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
            if car.lvl == 5 and not self.achievements[7].has_achieved():
                self.achievements[7].achieve()  # get a lv 5 car
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
        if player.lvl >= 100 and not self.achievements[13].has_achieved():
            self.achievements[13].achieve()  # reach level 100

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

    def load(self, load_dict):
        for c, load_item in enumerate(list(load_dict.values())):
            achieved, claimed_rewards = list(load_item.values())
            self.achievements[c].load(achieved, claimed_rewards)

    def save(self):
        return {ach.name: ach.save() for ach in self.achievements}
