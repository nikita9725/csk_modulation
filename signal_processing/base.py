import numpy as np

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SignalTdomainBase(ABC):
    input_msg_bits: np.array

    @property
    @abstractmethod
    def demodulated_msg_bits(self):
        ...


class ModulatorBase(ABC):
    @abstractmethod
    def __init__(self, snr_db: float):
        pass

    @abstractmethod
    def modulate_t_domain(self, message: np.array) -> SignalTdomainBase:
        ...
