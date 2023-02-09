import numpy as np
from bitarray import bitarray
from dataclasses import dataclass
from math import ceil

from const import McodeParams


@dataclass
class McodeTdomain:
    m_code: np.array
    t_arr: np.array
    tau_simb: float
    tau_simb_exp: float
    t_period: float

    def __repr__(self):
        return (f'М-последовательность во временной области со следующими '
                f'параметрами: \n'
                f'Длительность символа: {self.tau_simb}\n'
                f'Длительность символа (расширенная для графика) '
                f'{self.tau_simb_exp}\n'
                f'Период последовательности: {self.t_period}')


class McodeGenerator:
    def __init__(self):
        self.start_bits = McodeParams.start_bits
        self.t_period = McodeParams.t_period

        # Расширение кодовой последовательности
        self.expans = McodeParams.expans

        self.n = len(self.start_bits)

        # Максимальная длина последовательности
        self.m = 2 ** self.n - 1

    def generate_m_code(self) -> np.array:
        start_bits = bitarray(self.start_bits)
        m_code = np.array([], dtype='int')

        for _ in range(self.m):
            # TODO: Автоматизировать индексы
            mod2_sum = start_bits[4] ^ start_bits[8]

            start_bits >>= 1
            start_bits[0] = mod2_sum
            m_code = np.append(m_code, start_bits[6])

        return m_code

    def get_m_code_in_t_domain(self) -> McodeTdomain:
        m_code = self.generate_m_code()
        tau_simb = self.t_period / len(m_code)
        tau_simb_exp = tau_simb / self.expans
        n = ceil(self.t_period / tau_simb_exp)
        t_arr = np.arange(start=0, step=tau_simb_exp, stop=n * tau_simb_exp)
        m_code = np.repeat(m_code, self.expans)

        return McodeTdomain(
            m_code=m_code,
            t_arr=t_arr,
            tau_simb=tau_simb,
            tau_simb_exp=tau_simb_exp,
            t_period=self.t_period
        )
