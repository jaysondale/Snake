import pygame, random, time
from pygame.locals import *


def on_render():
    pygame.display.update()
    pass


def on_cleanup():
    pygame.quit()


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


        self.snake_x = [random.randint(1, self.width)]
        self.snake_y = [random.randint(1, self.height)]

        for i in range(9):
            self.snake_y.append(self.snake_y[0])
            self.snake_x.append(self.snake_x[0] + self.block_width)

        self.direction = random.randint(0, 3)

        self.block_x = random.randint(1, self.width)
        self.block_y = random.randint(1, self.height)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.width, self.height + 50), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction = 0
            elif event.key == pygame.K_s:
                self.direction = 1
            elif event.key == pygame.K_a:
                self.direction = 2
            elif event.key == pygame.K_d:
                self.direction = 3

    def on_loop(self):
        if self.direction == 0:
            # UP
            self.snake_x.reverse()
            self.snake_x.append(self.snake_x[len(self.snake_x) - 1])
            self.snake_x.reverse()

            # check collision with upper boundary
            self.snake_y.reverse()
            if self.snake_y[len(self.snake_y) - 1] <= 0:
                self.snake_y.append(self.height)
            else:
                self.snake_y.append(self.snake_y[len(self.snake_y) - 1] - self.move_rate)

            self.snake_y.reverse()

        elif self.direction == 1:
            # DOWN
            self.snake_x.reverse()
            self.snake_x.append(self.snake_x[len(self.snake_x) - 1])
            self.snake_x.reverse()

            # check collision with lower boundary
            self.snake_y.reverse()
            if self.snake_y[len(self.snake_y) - 1] >= self.height - 20:
                self.snake_y.append(-20)
            else:
                self.snake_y.append(self.snake_y[len(self.snake_y) - 1] + self.move_rate)
            self.snake_y.reverse()
        elif self.direction == 2:
            # LEFT
            # check collision with left boundary
            self.snake_x.reverse()
            if self.snake_x[len(self.snake_x) - 1] <= 0:
                self.snake_x.append(self.width)
            else:
                self.snake_x.append(self.snake_x[len(self.snake_x) - 1] - self.move_rate)
            self.snake_x.reverse()

            self.snake_y.reverse()
            self.snake_y.append(self.snake_y[len(self.snake_y) - 1])
            self.snake_y.reverse()
        elif self.direction == 3:
            # RIGHT
            # check collision with right boundary
            self.snake_x.reverse()
            if self.snake_x[len(self.snake_x) - 1] >= self.width:
                self.snake_x.append(-20)
            else:
                self.snake_x.append(self.snake_x[len(self.snake_x) - 1] + self.move_rate)
            self.snake_x.reverse()

            self.snake_y.reverse()
            self.snake_y.append(self.snake_y[len(self.snake_y) - 1])
            self.snake_y.reverse()

        # check collision with food
        if self.block_y - 20 <= self.snake_y[0] <= self.block_y + 20:
            if self.block_x - 20 <= self.snake_x[0] <= self.block_x + 20:
                self.add_block = True
                self.score += 1


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
                self.block_x = random.randint(1, self.width - 20)
                self.block_y = random.randint(1, self.height - 20)
            self.count += 1
            if self.count == 11:
                self.add_block = False
                self.count = 0

        # print self.snake_x
        # print self.snake_y
        self._display_surf.fill((255, 255, 255))

        pygame.draw.rect(self._display_surf, [155, 0, 0], [self.block_x, self.block_y, 10 * self.block_width, 10 * self.block_height])
        for i in range(len(self.snake_x)):
            pygame.draw.rect(self._display_surf, [0, 155, 0], [self.snake_x[i], self.snake_y[i], 10 * self.block_width,
                                                               10 * self.block_height])
        # display bottom menu bar
        pygame.draw.rect(self._display_surf, [200, 200, 200], [0, self.height, self.width, 50])

        # print score
        font = pygame.font.SysFont(None, 24)
        text = font.render('Score: ' + str(self.score), True, (0, 0, 0))
        self._display_surf.blit(text, (self.width * 0.75, self. height + 20))
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