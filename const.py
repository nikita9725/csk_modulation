import numpy as np


class McodeParams:
    START_BITS = (1, 1, 1, 1, 1, 1, 1, 1, 1)
    T_PERIOD = 1e-3
    EXPANS = 20  # Расширение кодовой последовательности


class MessageParams:
    MESSAGE = np.array((0, 1, 0, 1, 0, 1, 0, 1 ,0), dtype='int')
