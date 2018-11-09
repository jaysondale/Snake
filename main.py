import pygame, random, time
from pygame.locals import *


def on_render():
    pygame.display.update()
    pass


def on_cleanup():
    pygame.quit()


def move(dir, x, y, mr):
    x.reverse()
    y.reverse()

    x.append(x[len(x) - 1] + (dir[0] * mr))
    y.append(y[len(y) - 1] + (dir[1] * mr))

    x.reverse()
    y.reverse()


def does_exist(li, index):
    i = 0
    verdict = []
    for point in li:
        if point == li[index] and not i == index:
            verdict.append(i)
        i += 1
    return verdict




class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.rate = 0.000000005
        self.move_rate = 4
        self.add_block = False
        self.count = 0

        self.score = 0

        # Snake parameters

        self.block_width = 2
        self.block_height = 2

        self.square_side = 20

        self.snake_x = [200]
        self.snake_y = [200]

        self.lose = False

        for i in range(9):
            self.snake_y.append(self.snake_y[0])
            self.snake_x.append(self.snake_x[0] + self.block_width)

        self.direction = [[1, 0], [1, 0]]

        self.block_x = (self.square_side * random.randint(1, (self.width - self.square_side) / self.square_side))
        self.block_y = (self.square_side * random.randint(1, (self.height - self.square_side) / self.square_side))

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.width, self.height + 50), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction.append([0, -1])
            elif event.key == pygame.K_s:
                self.direction.append([0, 1])
            elif event.key == pygame.K_a:
                self.direction.append([-1, 0])
            elif event.key == pygame.K_d:
                self.direction.append([1, 0])

            self.direction.remove(self.direction[0])

            print self.direction

    def on_loop(self):
        if self.direction[1] == [0, -1]:
            if self.snake_x[0] % self.square_side == 0:
                # up
                move(self.direction[1], self.snake_x, self.snake_y, self.move_rate)

            else:
                move(self.direction[0], self.snake_x, self.snake_y, self.move_rate)

        elif self.direction[1] == [0, 1]:
            if self.snake_x[0] % self.square_side == 0:
                # down
                move(self.direction[1], self.snake_x, self.snake_y, self.move_rate)

            else:
                move(self.direction[0], self.snake_x, self.snake_y, self.move_rate)

        elif self.direction[1] == [-1, 0]:
            if self.snake_y[0] % self.square_side == 0:
                # left
                move(self.direction[1], self.snake_x, self.snake_y, self.move_rate)

            else:
                move(self.direction[0], self.snake_x, self.snake_y, self.move_rate)

        elif self.direction[1] == [1, 0]:
            if self.snake_y[0] % self.square_side == 0:
                # right
                move(self.direction[1], self.snake_x, self.snake_y, self.move_rate)

            else:
                move(self.direction[0], self.snake_x, self.snake_y, self.move_rate)

        # check collision with food
        if self.block_y - 19 <= self.snake_y[0] <= self.block_y + 19:
            if self.block_x - 19 <= self.snake_x[0] <= self.block_x + 19:
                self.add_block = True
                self.score += 1

        # check collision with itself
        if does_exist(self.snake_x, 0) and does_exist(self.snake_y, 0):
            print self.snake_x
            print self.snake_y
            self.lose = True

        if self.snake_y[0] < 0 or self.snake_y[0] > self.height - 19 or self.snake_x[0] < 0 or self.snake_x[0] > self.width - 19:
            self.lose = True

        # remove last block
        if not self.add_block:
            self.snake_x.reverse()
            self.snake_y.reverse()
            self.snake_x.remove(self.snake_x[0])
            self.snake_y.remove(self.snake_y[0])
            self.snake_x.reverse()
            self.snake_y.reverse()

        else:
            if self.count == 0:
                self.block_x = (self.square_side * random.randint(1, (self.width - self.square_side) / self.square_side))
                self.block_y = (self.square_side * random.randint(1, (self.height - self.square_side) / self.square_side))
            self.count += 1
            if self.count == 11:
                self.add_block = False
                self.count = 0

        # print self.snake_x
        # print self.snake_y
        self._display_surf.fill((255, 255, 255))

        # draw grid
        for i in range(self.width / self.square_side):
            pygame.draw.rect(self._display_surf, [100, 100, 100], [i * self.square_side, 0, 2, self.height])

        for i in range(self.height / self.square_side):
            pygame.draw.rect(self._display_surf, [100, 100, 100], [0, i * self.square_side, self.width, 2])

        pygame.draw.rect(self._display_surf, [155, 0, 0], [self.block_x, self.block_y, 10 * self.block_width, 10 * self.block_height])
        for i in range(len(self.snake_x)):
            pygame.draw.rect(self._display_surf, [0, 155, 0], [self.snake_x[i], self.snake_y[i], 10 * self.block_width,
                                                               10 * self.block_height])
        # display bottom menu bar
        pygame.draw.rect(self._display_surf, [200, 200, 200], [0, self.height, self.width, 50])


        # print score
        font = pygame.font.SysFont(None, 24)
        text = font.render('Score: ' + str(self.score), True, (0, 0, 0))
        lost = font.render("You Lost! Hahahaha you're terrible", True, (0, 0, 0))
        self._display_surf.blit(text, (self.width * 0.75, self. height + 20))
        if self.lose:
            self._display_surf.blit(lost, (self.width * 0.1, self.height + 20))
        pass

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running :
            time.sleep(self.rate)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            on_render()


if __name__ == "__main__":
    snake = Game()
    snake.on_execute()