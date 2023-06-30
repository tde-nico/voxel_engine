from numba import njit
import numpy as np
import glm
import math


WIDTH = 1280
HEIGHT = 720

WIN_RES = glm.vec2(WIDTH, HEIGHT)


BG_COLOR = glm.vec3(0.1, 0.16, 0.25)
