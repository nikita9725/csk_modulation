import numpy as np

from dataclasses import dataclass
from math import erfc
from multiprocessing import cpu_count, Pool
from typing import Optional

from const import BerEvaulationParams, McodeParams, MessageParams
from signal_processing import CskModulator
from utils import disk_cache, evaulation_time_count


@dataclass
class BerResults:
    snr_db_arr: np.array
    ber_arr: np.array
    bit_rate: Optional[float]


@dataclass
class BerResult:
    bits_count: int
    err_bits_count: int
    snr_db: float

    @property
    def ber(self) -> float:
        return self.err_bits_count / self.bits_count


def get_bpsk_theory_ber(snr_db_arr: np.array) -> BerResults:
    ber_arr = np.array(
        [_get_bpsk_theory_ber_for_db_value(snr_db) for snr_db in snr_db_arr],
        dtype='float',
    )

    return BerResults(snr_db_arr, ber_arr, None)


def _get_bpsk_theory_ber_for_db_value(snr_db: float) -> float:
    amp = 10 ** (snr_db / 20)

    return 0.5 * erfc(np.sqrt(amp))


def evaulate_ber_for_db_value(snr_db: float, bit_rate: float) -> BerResult:
    message = MessageParams.MESSAGE

    runs_count = BerEvaulationParams.RUNS_COUNT
    err_bits_count = 0
    bits_count = len(message) * runs_count

    t_period = len(McodeParams.START_BITS) / bit_rate

    for _ in range(runs_count):
        csk_modulator = CskModulator(snr_db=snr_db, t_period=t_period)
        csk_t_domain = csk_modulator.modulate_t_domain(message)

        err_bits_count += sum(
            csk_t_domain.input_msg_bits ^ csk_t_domain.demodulated_msg_bits
        )

    return BerResult(bits_count, err_bits_count, snr_db)


def _pack_results(results: list[BerResult], bit_rate: float) -> BerResults:
    results.sort(key=lambda ber_result: ber_result.snr_db)

    snr_db_arr = np.array([], dtype='float')
    ber_arr = np.array([], dtype='float')

    for result in results:
        snr_db_arr = np.append(snr_db_arr, result.snr_db)
        ber_arr = np.append(ber_arr, result.ber)

    ber_results = BerResults(snr_db_arr, ber_arr, bit_rate)

    return ber_results


@disk_cache
@evaulation_time_count
def get_ber_results(snr_db_arr: np.array,
                    bit_rate_list: list[float]) -> list[BerResults]:

    ber_results_list = []
    for bit_rate in bit_rate_list:
        with Pool(cpu_count()) as p:
            bit_rate_arg_list = [bit_rate for _ in snr_db_arr]
            results = [*p.starmap(evaulate_ber_for_db_value,
                                  zip(snr_db_arr, bit_rate_arg_list))]
        ber_results_list.append(_pack_results(results, bit_rate))

    return ber_results_list
