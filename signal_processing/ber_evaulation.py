import numpy as np

from dataclasses import dataclass
from multiprocessing import cpu_count, Pool

from signal_processing import CskModulator, McodeGenerator
from utils import evaulation_time_count


@dataclass
class BerResults:
    snr_db_arr: np.array
    ber_arr: np.array


@dataclass
class BerResult:
    bits_count: int
    err_bits_count: int
    snr_db: float

    @property
    def ber(self) -> float:
        return self.err_bits_count / self.bits_count


def evaulate_ber_for_db_value(snr_db: float):
    message = np.array((0, 1, 0, 1, 0, 1, 0, 1, 0), dtype='int')

    m_code_gen = McodeGenerator()
    m_code_t_domain = m_code_gen.get_m_code_t_domain()

    runs_count = 5_000
    err_bits_count = 0
    bits_count = len(message) * runs_count

    for _ in range(runs_count):
        csk_modulator = CskModulator(code_t_domain=m_code_t_domain,
                                     snr_db=snr_db)
        csk_t_domain = csk_modulator.modulate_t_domain(message)

        err_bits_count += sum(
            csk_t_domain.input_msg_bits ^ csk_t_domain.demodulated_msg_bits
        )

    return BerResult(bits_count, err_bits_count, snr_db)


def _pack_results(results: list[BerResult]) -> BerResults:
    results.sort(key=lambda ber_result: ber_result.snr_db)

    snr_db_arr = np.array([], dtype='float')
    ber_arr = np.array([], dtype='float')

    for result in results:
        snr_db_arr = np.append(snr_db_arr, result.snr_db)
        ber_arr = np.append(ber_arr, result.ber)

    ber_results = BerResults(snr_db_arr, ber_arr)

    return ber_results


@evaulation_time_count
def get_ber_results() -> BerResults:
    snr_db_vals = np.arange(start=-20, step=0.5, stop=0)

    with Pool(cpu_count()) as p:
        results = list(p.map(evaulate_ber_for_db_value, snr_db_vals))

    return _pack_results(results)
