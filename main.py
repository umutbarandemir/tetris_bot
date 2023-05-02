import pygame
import random
import PythonBot
import StartButtons

colours = [
        (0, 0, 0),
        (120, 37, 179),
        (100, 179, 179),
        (80, 34, 22),
        (80, 134, 22),
        (180, 34, 22),
        (180, 34, 122),
]

class Figure:
    x = 0
    y = 0

    shapes = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.shapes) - 1)
        self.color = random.randint(1, len(colours) - 1)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes[self.type])

    def image(self):
        return self.shapes[self.type][self.rotation]

class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None

        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"

        for i in range(height):
            newLINE = []
            for j in range(width):
                newLINE.append(0)
            self.field.append(newLINE)

    def newSHAPE(self):
        self.figure = Figure(3, 0)

    def crossing(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def lineBREAK(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.crossing():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.crossing():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.lineBREAK()
        self.newSHAPE()
        if self.crossing():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.crossing():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.crossing():
            self.figure.rotation = old_rotation


# Initialize the game engine
pygame.init()

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

''' 
#starting buttons
bot_image = pygame.image.load('botbutton.png').convert_alpha()
user_image = pygame.image.load('userbutton.png').convert_alpha()

startBot = StartButtons.Button(100,200,bot_image,0.8)
startUser = StartButtons.Button(400,200,user_image,0.8)
'''

# GAME LOOP
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0
pressing_down = False

'''
    screen.fill((202,228,241))
    
    if startBot.draw(screen):
        game.state == "start"      
    if startUser.draw(screen):
        game.state == "start"
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    pygame.display.update()
'''

while not done:

    if game.figure is None:
        game.newSHAPE()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in list(pygame.event.get()) + PythonBot.startAI(game.field, game.figure, game.width, game.height): #this is the line where AI gets the control. With this -> for event in pygame.event.get(): user gets the control
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.fill((255, 255, 255))

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, (128, 128, 128), [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colours[game.field[i][j]], [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colours[game.figure.color], [game.x + game.zoom * (j + game.figure.x) + 1, game.y + game.zoom * (i + game.figure.y) + 1, game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, (0, 0, 0))
    gameover1 = font1.render("Game Over", True, (255, 125, 0))
    gameover2 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(gameover1, [20, 200])
        screen.blit(gameover2, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

