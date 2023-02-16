import numpy as np
from dataclasses import dataclass
from math import ceil
from functools import cache

from const import McodeParams


@dataclass
class McodeTdomain:
    m_code: np.array
    m_code_exp: np.array
    t_arr_exp: np.array
    t_arr: np.array
    tau_chip: float
    tau_chip_exp: float
    t_period: float
    n: int

    @property
    def expans(self) -> int:
        return int(self.tau_chip/self.tau_chip_exp)

    def __repr__(self):
        return (f'М-последовательность во временной области со следующими '
                f'параметрами: \n'
                f'Длительность символа: {self.tau_chip}\n'
                f'Длительность символа (расширенная для графика) '
                f'{self.tau_chip_exp}\n'
                f'Период последовательности: {self.t_period}')


class McodeGenerator:
    def __init__(self):
        self.start_bits = McodeParams.START_BITS
        self.t_period = McodeParams.T_PERIOD

        # Расширение кодовой последовательности
        self.expans = McodeParams.EXPANS

        self.n = len(self.start_bits)

        # Максимальная длина последовательности
        self.m = 2 ** self.n

    @cache
    def generate_m_code(self) -> np.array:
        start_bits = np.array(self.start_bits, dtype='int')
        m_code = np.array([], dtype='int')

        for _ in range(self.m):
            # TODO: Автоматизировать индексы
            mod2_sum = start_bits[4] ^ start_bits[8]

            start_bits = np.roll(start_bits, 1)
            start_bits[0] = mod2_sum
            m_code = np.append(m_code, start_bits[6])

        return m_code

    @cache
    def get_m_code_t_domain(self) -> McodeTdomain:
        m_code = self.generate_m_code()
        tau_chip = self.t_period / len(m_code)
        tau_chip_exp = tau_chip / self.expans
        n = ceil(self.t_period / tau_chip_exp)
        t_arr = np.arange(start=0, step=tau_chip, stop=n * tau_chip_exp)
        t_arr_exp = np.arange(
            start=0, step=tau_chip_exp, stop=n * tau_chip_exp)
        m_code_exp = np.repeat(m_code, self.expans)

        return McodeTdomain(
            m_code=m_code,
            m_code_exp=m_code_exp,
            t_arr=t_arr,
            t_arr_exp=t_arr_exp,
            tau_chip=tau_chip,
            tau_chip_exp=tau_chip_exp,
            t_period=self.t_period,
            n=self.n
        )
