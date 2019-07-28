from enum import Enum
import pygame


class Images(Enum):
    core1 = pygame.image.load('res/core1.png')
    core2 = pygame.image.load('res/core2.png')
    core3 = pygame.image.load('res/core3.png')
    core4 = pygame.image.load('res/core4.png')
    core1_light = pygame.image.load('res/core1_light.png')
    core2_light = pygame.image.load('res/core2_light.png')
    core3_light = pygame.image.load('res/core3_light.png')
    core4_light = pygame.image.load('res/core4_light.png')
    line = pygame.image.load('res/pipe1.png')
    angle = pygame.image.load('res/pipe2.png')
    triple = pygame.image.load('res/pipe3.png')
    cross = pygame.image.load('res/pipe4.png')
    restart = pygame.image.load('res/restart_press.png')
    mini_btn_restart = pygame.image.load('res/restart_mini_btn.png')
    alpha_fill = pygame.image.load('res/alpha_fill.png')




IMAGE_SWITCHER = {
    1: Images.core1.value,
    2: Images.line.value,
    3: Images.angle.value,
    4: Images.triple.value,
    5: Images.cross.value,
}

CORES = {
    0: Images.core1.value,
    1: Images.core2.value,
    2: Images.core3.value,
    3: Images.core4.value,
}

CORES_LIGHT = {
    0: Images.core1_light.value,
    1: Images.core2_light.value,
    2: Images.core3_light.value,
    3: Images.core4_light.value,
}