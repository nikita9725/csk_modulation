from m_code_generator import McodeGenerator
from plots import get_m_code_t_domain_figure


if __name__ == '__main__':
    m_code_gen = McodeGenerator()
    m_code = m_code_gen.generate_m_code()
    m_code_t_domain = m_code_gen.get_m_code_in_t_domain()

    get_m_code_t_domain_figure(m_code_t_domain)
