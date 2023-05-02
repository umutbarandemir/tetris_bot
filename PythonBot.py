import pygame

class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key

counter = 0
def startAI(game_field, game_figure, game_width, game_height):
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    rotation, position = bestPossibleRotation(game_field, game_figure, game_width, game_height)
    if game_figure.rotation != rotation:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
    elif game_figure.x < position:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif game_figure.x > position:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        e = Event(pygame.KEYDOWN, pygame.K_SPACE)
    return [e]

def crossing(game_field, x, y, game_width, game_height, game_figure_image):
    intersection = False
    for i in range(4):
        for j in range(4):
            if i * 4 + j in game_figure_image:
                if i + y > game_height - 1 or \
                        j + x > game_width - 1 or \
                        j + x < 0 or \
                        game_field[i + y][j + x] > 0:
                    intersection = True
    return intersection

def predict(game_field, x, y, game_width, game_height, game_figure_image):
    while not crossing(game_field, x, y, game_width, game_height, game_figure_image):
        y += 1
    y -= 1

    height = game_height
    holes = 0
    filled = []
    breaks = 0
    for i in range(game_height-1, -1, -1):
        it_is_full = True
        prev_holes = holes
        for j in range(game_width):
            u = '_'
            if game_field[i][j] != 0:
                u = "x"
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in game_figure_image:
                        if jj + x == j and ii + y == i:
                            u = "x"

            if u == "x" and i < height:
                height = i
            if u == "x":
                filled.append((i, j))
                for k in range(i, game_height):
                    if (k, j) not in filled:
                        holes += 1
                        filled.append((k,j))
            else:
                it_is_full = False
        if it_is_full:
            breaks += 1
            holes = prev_holes

    return holes, game_height-height-breaks

def bestPossibleRotation(game_field, game_figure, game_width, game_height):
    best_height = game_height
    best_holes = game_height*game_width
    best_position = None
    best_rotation = None

    for rotation in range(len(game_figure.shapes[game_figure.type])):
        fig = game_figure.shapes[game_figure.type][rotation]
        for j in range(-3, game_width):
            if not crossing( game_field, j, 0, game_width, game_height, fig):
                holes, height = predict( game_field, j, 0, game_width, game_height, fig )
                if best_position is None or best_holes > holes or \
                    best_holes == holes and best_height > height:
                    best_height = height
                    best_holes = holes
                    best_position = j
                    best_rotation = rotation
    return best_rotation, best_position




