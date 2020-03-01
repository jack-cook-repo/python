from typing import List

import pygame
import os
import neat
# import time
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

PATH = "/Users/jackcook/Documents/GitHub/python/Flappy bird NEAT algorithm/imgs/{}.png"


def load_and_scale(img):
    img_path = PATH.format(img)
    img_loaded = pygame.image.load(img_path)
    img_2x = pygame.transform.scale2x(img_loaded)

    return img_2x

BIRDS = ["bird1","bird2","bird3"]
BIRD_IMGS = [load_and_scale(bird) for bird in BIRDS]

PIPE_IMG = load_and_scale("pipe")
BASE_IMG = load_and_scale("base")
BG_IMG = load_and_scale("bg")

STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

pygame.display.set_caption("Flappy Bird")


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 15
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5  # In pygame negative velocity means moving upwards
        self.tick_count = 0  # Keeps track of when we last jumped
        self.height = self.y  # Tracks where the bird jumps FROM

    @staticmethod
    def get_displacement(vel, tick_count):
        # s = ut + 1/2at^2, tracks vertical displacement
        displacement = vel*tick_count + 0.5*3*tick_count**2
        return displacement

    def move(self):
        # Calculate previous displacement
        if self.tick_count == 0:
            previous_d = 0
        else:
            previous_d = self.get_displacement(self.vel, self.tick_count)

        # Calculate new displacement, and then movement
        self.tick_count += 1
        d = self.get_displacement(self.vel, self.tick_count)
        movement = d - previous_d
        if movement >= 16:
            movement = 16 # Prevent too fast a drop

        # Move bird
        self.y += movement

        # If moving upwards, or within 50 pixels below initial height
        if movement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
            elif self.tilt <= -90:
                self.tilt = -90

    def draw(self, win):
        self.img_count += 1 #How many times have we shown one image

        # In increments of animation time, show different images
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        #If bird is pointing down, only show the downward flapping image
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft= (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        # Creates list showing non-empty pixels in an image, used for collision detection
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200 # Gap between pipes
    VEL = 15 # Pipe movement speed

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) # Flip bottom pipe image in y axis
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_heights()

    def set_heights(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Figure out overlaps of bird & pipes
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # Returns None if no overlap
        t_point = bird_mask.overlap(top_mask, top_offset) # Returns None if no overlap

        if t_point or b_point:
            return True
        else:
            return False

class Base:
    VEL = 15
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0 # 1st image
        self.x2 = self.WIDTH # 2nd image

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # If first image completely off screen, move it back behind second image on the right
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0,0)) # Draw background image (blit means draw)

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (237,86,86))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update() # Refresh screen


def main(genomes, config):
    birds = []
    nets = []
    ge = []
    pygame.mixer.init()

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(200, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run_loop = True
    while run_loop:

        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
                pygame.quit()
                quit()

        # Pick which pipe to look at
        pipe_ind = 0
        if len(birds) > 0:
            # Check if birds have moved past first pipe
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run_loop = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1  # Small amount as this will run every time clock ticks!

            output = nets[x].activate((bird.y,
                                       abs(bird.y - pipes[pipe_ind].height), # Distance from top pipe
                                       abs(bird.y - pipes[pipe_ind].bottom))) # Distance from bottom pipe

            if output[0] > 0.5: # Only one output neuron
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird, win):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # Check if pipe is off screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5 # Plus 5 fitness every time pipe is passed
            pipes.append(Pipe(600))

        # Delete unused pipes
        for r in rem:
            pipes.remove(r)

        # Check collision with floor or movement above screen
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)