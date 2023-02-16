import numpy as np
from numpy.fft import fftshift, ifftshift
from operator import mod
from dataclasses import dataclass
from signal_processing.m_code_generator import McodeTdomain


@dataclass
class CskSignalTdomain:
    modulated_code: np.array
    m_code: np.array
    msg_bits: np.array
    m_code_exp: np.array
    msg_bits_exp: np.array
    msg_bits_count: int
    modulated_code_exp: np.array
    t_arr: np.array

    @property
    def expans(self) -> int:
        return int(len(self.m_code_exp) / len(self.m_code))

    @property
    def demodulated_msg_bits_exp(self) -> np.array:
        cor_arr = np.array([], dtype='float')
        for shift in range(len(self.m_code)):
            cor_arr = np.append(cor_arr, self._get_corr(shift))

        code_offset = int(np.where(cor_arr == np.max(cor_arr))[0])
        message = self._get_msg_from_offset(code_offset)
        msg_bit_expans = int(np.ceil(len(self.m_code) / len(message)))
        message = np.repeat(message, self.expans * msg_bit_expans)

        return message[:len(self.m_code_exp)]

    def _get_msg_from_offset(self, offset: int) -> np.array:
        msg_bits = np.array([int(bit) for bit in
                             bin(offset).replace('0b', '')],
                            dtype='int')
        if msg_bits.shape[0] < self.msg_bits_count:
            msg_bits =np.insert(
                msg_bits,
                *(0 for _ in range((self.msg_bits_count-len(msg_bits)) + 1))
            )
        return msg_bits

    def _get_corr(self, shift: int):
        corr_arr = np.abs(
            ifftshift(
                fftshift(np.roll(self.m_code_exp, shift * self.expans)) *
                fftshift(self.modulated_code_exp)
            )
        )
        return np.sum(corr_arr)


class CskModulator:
    def __init__(self, code_t_domain: McodeTdomain):
        # Начальные параметры:
        # Частота колебаний
        # Кол-во модулируемых бит
        # Кол-во чипов последовательности
        # Маппинг номера символа и сдвига
        self.code = code_t_domain
        self.snr_db = snr_db

    def modulate(self, message):
        code_arr = self.code.m_code
        code_offset = int(''.join(str(bit) for bit in message), 2)
        mod_arr = np.array([code_arr[mod(m-code_offset, len(code_arr))]
                            for m in range(len(code_arr))], dtype='int')
        return mod_arr

    def modulate_t_domain(self, message) -> CskSignalTdomain:
        msg_bits = self._get_message_bits(message)
        mod_arr = self.modulate(message)
        mod_arr = np.array(mod_arr.copy(), dtype='float')
        expans = self.code.expans

        msg_bits_exp = np.repeat(msg_bits, expans)
        mod_arr_exp = np.repeat(mod_arr, expans)
        mod_arr_exp *= np.cos(100e6 * 2 * np.pi)
        mod_arr_exp = self._add_noise(mod_arr_exp)

        tau_chip_exp = self.code.tau_chip / expans

        t_arr = np.arange(start=0,
                          step=tau_chip_exp,
                          stop=len(mod_arr_exp) * tau_chip_exp)

        return CskSignalTdomain(modulated_code=mod_arr,
                                m_code=self.code.m_code,
                                m_code_exp=self.code.m_code_exp,
                                msg_bits=msg_bits,
                                msg_bits_exp=msg_bits_exp,
                                msg_bits_count=self.code.n,
                                modulated_code_exp=mod_arr_exp,
                                t_arr=t_arr)

    def _get_message_bits(self, message) -> np.array:
        msg_bit_expans = int(np.ceil(len(self.code.m_code) / len(message)))

        message_bits = np.array([], dtype='int')
        for bit in message:
            message_bits = np.append(message_bits,
                                     np.repeat([bit], msg_bit_expans))
        return message_bits[:len(self.code.m_code)]

    def _add_noise(self, signal: np.array) -> np.array:
        # TODO: подумать о выносе данного метода в другое место
        signal_amp = 10 ** (self.snr_db / 20)
        signal = signal_amp * signal
        noise = np.random.normal(0, 1, len(signal))
        noisy_signal = signal + noise
        return noisy_signal


