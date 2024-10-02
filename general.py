import pygame

pygame.init()

'''General File'''


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


def create_text(display, text, font_size, colour, pos):
    font = pygame.font.Font('files/Quick Starter.ttf', font_size)
    x, y = pos
    display.blit(font.render(text, True, colour), (x, y))


def create_multiline_text(display, text_list, font_size, colour, pos):
    for count, text in enumerate(text_list):
        create_text(display, text, font_size, colour, (pos[0], pos[1] + (font_size + 4) * count))
