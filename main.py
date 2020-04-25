# pylint:disable=E1101
import pygame
import numpy as np

# set defaults
FPS = 60
SW = 800
SH = 800

running = True
screen = None
clock = pygame.time.Clock()
active_pixels = []
reduction = 5


def limit(val, low, high):
    val = max(low, val)
    val = min(high, val)
    return val

def is_quit(event):
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
        return False

class pixel:
    def __init__(self, x=0, y=0, w=1, colour = (255,255,255)):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.start = (x,y)

        self.pos = (x,y)
        self.colour = colour
        self.width = w
        active_pixels.append(self)

        self.age = 0

    def draw(self):
        
        if self.width == 1:
            screen.set_at(self.pos, self.colour)
        else:
            
            half_width = self.width // 2

            rng_x = range(self.x - half_width, self.x + half_width)
            rng_y = range(self.y - half_width, self.y + half_width)

            for dx in rng_x:
                for dy in rng_y:
                    pos = dx, dy
                    screen.set_at(pos, self.colour)
                

    def update(self):
        self.use_interp(self.age / 60)
        self.age += 1 / reduction

    def use_interp(self, time):
        percentage = limit(self.interp(time), 0, 1)

        if percentage <= 0:
            new_x, new_y = self.start
        elif percentage >= 1:
            new_x, new_y = self.target
        else:
            new_x = self.start_x + int(percentage * self.target_vec[0])
            new_y = self.start_y + int(percentage * self.target_vec[1])

        self.x, self.y = new_x, new_y

    # pylint:disable=method-hidden
    def interp(self, time = 60): # time is in frames
        return 0

    def set_interp(self, func):
        self.interp = func
        return self

    def set_target(self, x, y):
        self.target = x, y
        self.target_vec = (x - self.x, y - self.y)
        return self

def setup():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((SW, SH))

    lerp = lambda t: t
    qerp = lambda t: (t)**2
    eerp = lambda t: np.e ** t - 1
    

    p = pixel(100, 100, w = 10, colour=(0,0,255)).set_target(700,700).set_interp(lerp)
    p = pixel(100, 100, w = 10, colour=(0,255,0)).set_target(700,700).set_interp(qerp)
    p = pixel(100, 100, w = 10, colour=(255,0,0)).set_target(700,700).set_interp(eerp)
    

def update():
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if is_quit(event):
            global running
            running = False
    for obj in active_pixels:
        obj.update()
    for obj in active_pixels:
        obj.draw()

    pygame.display.flip()
    clock.tick(FPS)

def main():
    setup()

    while running:
        update()


if __name__ == '__main__':
    main()


