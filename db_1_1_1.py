import time
import json
import os
from tkinter import *
from tkinter import messagebox

from carstats import *
from achievements import *
from pathgen import *
from player import *
from boosters import *

'''Main File'''


def load(cars, player, achievements):
    with open("gamedata.json") as f:
        data = json.load(f)
    cars_data, player_data, ach_data = data["carstats"], data["player"], data["ach"]
    cars.load(cars_data)
    player.load(player_data)
    achievements.load(ach_data)
    return cars, player, achievements


def save(car_dict, player_dict, ach_dict):
    data = {"carstats": car_dict, "player": player_dict, "ach": ach_dict}
    data_string = json.dumps(data, indent=4)
    with open("gamedata.json", "w") as outfile:
        outfile.write(data_string)


def main_loop():  # main loop
    pygame.init()
    display = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Drift Boss 2D (v1.1.1)")
    mode = "title screen"
    is_viewing_arrows = False

    exp_reqs = {[n for n in range(101)][n]: [round(40 * n ** 2.15) for n in range(101)][n] for n in range(101)}

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

    if os.path.exists('gamedata.json'):
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
                                if cars.cars[selected_car_index].type == "Drifter":
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
            text = f"{'' if cars.cars[selected_car_index].reforge is None else cars.cars[selected_car_index].reforge } {cars.cars[selected_car_index].type.upper()} [{cars.cars[selected_car_index].lvl} ]"
            create_text(display, text, 18, cars.cars[selected_car_index].rarity_colour, (255 - len(text) * 7, 305))
            pygame.draw.polygon(surface=display, color="#0096FF", points=[(175, 250), (205, 230), (205, 270)])
            pygame.draw.polygon(surface=display, color="#7393B3", points=[(175, 250), (205, 230), (205, 270)], width=3)
            pygame.draw.polygon(surface=display, color="#0096FF", points=[(295, 230), (295, 270), (325, 250)])
            pygame.draw.polygon(surface=display, color="#7393B3", points=[(295, 230), (295, 270), (325, 250)], width=3)
            if cars.cars[selected_car_index].locked:
                if cars.cars[selected_car_index].frag_req > 0:
                    text1 = f"{cars.cars[selected_car_index].coin_req}"
                    text2 = f"{cars.cars[selected_car_index].frag_req}" if cars.cars[selected_car_index].frag_req > 0 else ""
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
                        elif 305 <= x <= 305 + 165 and 320 <= y <= 320 + 40:  # reforge car
                            player.coins = cars.cars[selected_car_index].change_reforge(player.coins)
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
            colour1 = '#FFD700' if cars.cars[selected_car_index].lvl < 5 else (200, 200, 200)
            colour2 = '#FFD700' if not cars.cars[selected_car_index].upgraded_rarity else (200, 200, 200)
            pygame.draw.rect(display, colour1, (305, 375, 165, 40))
            pygame.draw.rect(display, (100, 100, 100), (305, 375, 165, 40), width=2)
            pygame.draw.rect(display, colour2, (305, 430, 165, 40))
            pygame.draw.rect(display, (100, 100, 100), (305, 430, 165, 40), width=2)
            pygame.draw.rect(display, '#FFD700', (305, 320, 165, 40))
            pygame.draw.rect(display, (100, 100, 100), (305, 320, 165, 40), width=2)
            create_text(display, f'UPGRADE ({cars.cars[selected_car_index].lvl_cost})', 14, (0, 0, 0), (310, 385))
            create_text(display, f'+1 RARITY ({cars.cars[selected_car_index].upgrade_rarity_cost})', 14, (0, 0, 0),
                        (310, 440))
            create_text(display, f'REFORGE ({cars.cars[selected_car_index].reforge_cost})', 14, (0, 0, 0),
                        (310, 330))
            prefix = f"{cars.cars[selected_car_index].reforge.upper()} " if cars.cars[selected_car_index].reforge is not None else ""
            text = f"{prefix}{cars.cars[selected_car_index].type.upper()} [{cars.cars[selected_car_index].lvl} ]"
            create_text(display, text, 15, cars.cars[selected_car_index].rarity_colour,
                        ((270 - len(text) * 11) // 2 + 10, 100))

            start_y = 145
            stats_to_render = {"DRIFT ANGLE: ": (round(cars.cars[selected_car_index].car_drift_angle, 3), round(cars.cars[selected_car_index].reforge_drift_bonus, 3)),
                               "HEALTH: ": (round(cars.cars[selected_car_index].health, 3), round(cars.cars[selected_car_index].reforge_health_bonus, 3)),
                               "HEALTH REGEN: ": (round(cars.cars[selected_car_index].health_regen, 3), round(cars.cars[selected_car_index].reforge_health_regen_bonus), 3),
                               "MANA: ": (round(cars.cars[selected_car_index].mana, 3), round(cars.cars[selected_car_index].reforge_mana_bonus, 3)),
                               "MANA REGEN: ": (round(cars.cars[selected_car_index].mana_regen, 3), round(cars.cars[selected_car_index].reforge_mana_regen_bonus, 3)),
                               "SCORE WISDOM: ": (round(cars.cars[selected_car_index].score_wisdom, 3), round(cars.cars[selected_car_index].reforge_score_wisdom_bonus, 3)),
                               "COIN WISDOM: ": (round(cars.cars[selected_car_index].coin_wisdom, 3), round(cars.cars[selected_car_index].reforge_coin_wisdom_bonus, 3))
                               }
            for tag, val in stats_to_render.items():
                if float(val[0]) != 0:
                    add_on = f" (+{str(val[1])})" if float(val[1]) > 0 else ""
                    create_text(display, str(tag) + "+" + str(val[0]) + add_on, 14, (0, 0, 0), (15, start_y))
                    start_y += 25

            abilities_start_y = start_y + 12

            if cars.cars[selected_car_index].ability == "drifter":
                create_multiline_text(display, ["ABILITY:", "GAIN +3 BASE LEVELS", "PER BOOSTER"], 15, (0, 0, 0), (15, abilities_start_y))
                last_y = abilities_start_y + 20 * 3 + 10
            elif cars.cars[selected_car_index].ability == "timewarp":
                create_multiline_text(display, ["ABILITY (PRESS 5):", "TELEPORT 4 TILES", "FORWARD AND GAIN",
                                                "+50% SCORE AND COINS", "FOR 5 S (25 MANA)"], 14, (0, 0, 0),
                                      (15, abilities_start_y))
                last_y = abilities_start_y + 20 * 5 + 10
            elif cars.cars[selected_car_index].ability == "fortunate":
                create_multiline_text(display,
                                      ["ABILITY: ", "SACRIFICE ALL SCORE", "TO GAIN 1 COIN", "PER SCORE YOU GAIN"], 14,
                                      (0, 0, 0), (15, abilities_start_y))
                last_y = abilities_start_y + 20 * 4 + 10
            elif cars.cars[selected_car_index].ability == "midas car":
                create_multiline_text(display,
                                      ["ABILITY: ", "SACRIFICE ALL COINS", "TO GAIN 25 SCORE", "PER COIN YOU PICK UP"],
                                      14, (0, 0, 0), (15, abilities_start_y))
                last_y = abilities_start_y + 20 * 4 + 10
            else:
                last_y = abilities_start_y

            create_text(display, f"{cars.cars[selected_car_index].rarity} CAR", 14, cars.cars[selected_car_index].rarity_colour, (15, last_y))

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
            if player.lvl < 100:
                create_text(display, f'{round(exp_to_next_lvl)} EXP TO NEXT LVL ({round(dec_exp_to_next_lvl * 100)}%)',
                            18,
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
            create_multiline_text(display, ['[LV. 4+] ABILITY [100 MANA]:', 'GAIN A SCORE BOOST FOR',
                                            '15 S + 5 S PER LEVEL', 'ABOVE LV. 4 (PRESS 1)'], 15,
                                  (0, 0, 0), (110, 245))
            create_multiline_text(display, ['[LV. 7] MEGA SCORE DOTS', 'SPAWN ON PATH, GAIN', '300 SCORE WHEN',
                                            'PICKED UP (RED)'], 15,
                                  (0, 0, 0), (110, 350))

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
            create_multiline_text(display, ['[LV. 1+] ABILITY [50 MANA]: ', 'INSTANTLY HEAL TO', 'REGAIN 3% OF YOUR MAX', 'HEALTH PER LVL (PRESS 3)'], 14, (0, 0, 0),
                                  (110, 180))
            create_multiline_text(display,
                                  ['[LV. 4+] GAIN 1 EXTRA', 'LIFE PER LEVEL ABOVE LV.4', 'AND RESPAWN INSTANTLY IF', 'YOU DIE'],
                                  14,
                                  (0, 0, 0), (110, 260))
            create_multiline_text(display, ['[LV. 7] ABILITY [50 MANA]: ', 'GAIN INVINCIBILITY FOR 5 S',
                                            'AND 2X FLIGHT REGEN', 'WHILST CUTTING SCORE', 'AND COINS BY 50%',
                                            '(PRESS 4)'],
                                  14, (0, 0, 0), (110, 340))

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
            create_multiline_text(display, ['[LV. 4+] ABILITY [100 MANA]:', 'GAIN A COIN BOOST FOR ',
                                            '15 S + 5 S PER LEVEL ', 'ABOVE LV. 4 (PRESS 2)'], 15,
                                  (0, 0, 0), (110, 255))
            create_multiline_text(display,
                                  ['[LV. 7] MEGA COINS', 'SPAWN ON PATH, GAIN', '200 COINS WHEN', 'PICKED UP (BLUE)'],
                                  15, (0, 0, 0), (110, 350))

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
                        if player.mana >= 100:
                            player.use_ds2_ability(boosters)  # use double score second perk ability
                    if event.key == pygame.K_2 and boosters[2].lvl >= 4:
                        if player.mana >= 100:
                            player.use_cr2_ability(boosters)  # use coin rush second perk ability
                    if event.key == pygame.K_3 and boosters[1].lvl >= 1:  # use car insurance first perk ability
                        if player.mana >= 50:
                            player.use_ci1_ability(boosters)
                    if event.key == pygame.K_4 and boosters[1].lvl == 7:  # use car insurance third perk ability
                        if player.mana >= 50:
                            player.use_ci3_ability(boosters)
                    if event.key == pygame.K_5:  # use timewarp teleport ability
                        if cars.cars[selected_car_index].type == "Timewarp" and player.mana >= 25:
                            player.use_timewarp_ability()
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
                    if player.health > 0:
                        player.fly(frames)
                    else:
                        if boosters[1].get_num_lives() > 0:  # respawn
                            player.health = player.max_health
                            player.mana = player.max_mana
                            boosters[1].deduct_life()  # remove 1 life
                        else:  # game over
                            mode = "death screen"

            player.regenerate_health(frames)
            if player.health > player.max_health:
                player.health = player.max_health
            player.regenerate_mana(frames)
            if player.mana > player.max_mana:
                player.mana = player.max_mana

            path.coins = player.collect_coins(path.coins, boosters)  # collect coins on path
            if boosters[0].lvl == 7:
                path.mega_scores = player.collect_mega_scores(path.mega_scores)  # collect mega scores on path
            if boosters[2].lvl == 7:
                path.mega_coins = player.collect_mega_coins(path.mega_coins)  # collect mega coins on path
            path.car_frags = player.collect_car_frags(path.car_frags)  # collect car fragments on path
            player.collide_with_spikes(frames, path.spikes)

            if player.is_colliding_with_enemy_car(path.enemy_cars) and not boosters[1].is_active():
                if boosters[1].lives > 0:
                    if player.mana > player.max_mana:
                        player.mana = player.max_mana
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

            txt1 = f"FPS: {fps}"
            create_text(display, txt1, 22, (0, 0, 0), (515 - len(txt1) * 22, 20))
            txt2 = f"TIME: {round(ach_time)}"
            create_text(display, txt2, 22, (0, 0, 0), (530 - len(txt2) * 22, 50))

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


if __name__ == "__main__":
    main_loop()
