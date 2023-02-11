import numpy as np
from signal_processing.m_code_generator import McodeTdomain


class CskModulator:
    def __init__(self, code_t_domain: McodeTdomain):
        # Начальные параметры:
        # Частота колебаний
        # Кол-во модулируемых бит
        # Кол-во чипов последовательности
        # Маппинг номера символа и сдвига
        self.code = code_t_domain


    def modulate(self, message):
        # TODO: Сделать валидацию сообщения. Написать тест для модуляции
        code_arr = self.code.m_code

        mod_arr = np.array([], dtype='int')
        for symb in message:
            mod_arr = np.append(
                mod_arr,
                np.roll(code_arr, symb)
            )

        return mod_arr


    def add_noise(self):
        pass
