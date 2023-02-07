import matplotlib.pyplot as plt

from m_code_generator import McodeTdomain


def get_m_code_t_domain_figure(m_code_t_domain: McodeTdomain):
    plt.figure(figsize=(15, 5))
    plt.plot(m_code_t_domain.t_arr, m_code_t_domain.m_code)
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.title('M-последовательность во временной области')
    plt.show()
