import numpy as np
from numpy.fft import fftshift, ifftshift
from operator import mod
from dataclasses import dataclass
from signal_processing.m_code_generator import McodeTdomain


@dataclass
class CskSignalTdomain:
    modulated_code: np.array
    m_code: np.array
    m_code_repeated: np.array
    m_code_repeated_exp: np.array
    modulated_code_exp: np.array
    t_arr: np.array

    @property
    def symbols_exp(self) -> np.array:
        demod_arr = np.abs(
            ifftshift(
                fftshift(self.m_code_repeated_exp) *
                fftshift(self.modulated_code_exp)
            )
        )
        return demod_arr / max(demod_arr)


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
                [
                    code_arr[mod(m-symb, len(code_arr))]
                    for m in range(len(code_arr))
                ]
            )
        return mod_arr

    def modulate_t_domain(self, message) -> CskSignalTdomain:
        mod_arr = self.modulate(message)
        mod_arr = np.array(mod_arr.copy(), dtype='float')
        expans = self.code.expans

        m_code_arr_rep = np.tile(self.code.m_code, len(message))
        m_code_arr_rep_exp = np.repeat(m_code_arr_rep, expans)
        mod_arr_exp = np.repeat(mod_arr, expans)
        mod_arr_exp *= np.cos(100e6 * 2 * np.pi)

        tau_chip_exp = self.code.tau_chip / expans

        t_arr = np.arange(start=0,
                          step=tau_chip_exp,
                          stop=len(mod_arr_exp) * tau_chip_exp)

        return CskSignalTdomain(modulated_code=mod_arr,
                                m_code=self.code.m_code,
                                m_code_repeated=m_code_arr_rep,
                                m_code_repeated_exp=m_code_arr_rep_exp,
                                modulated_code_exp=mod_arr_exp,
                                t_arr=t_arr)

    def add_noise(self):
        pass
