import plotly.express as px
from signal_processing import CskSignalTdomain, McodeTdomain


def get_m_code_t_domain_figure(m_code_t_domain: McodeTdomain):
    x_title = 'Время, с'
    y_title = 'Амплитуда'
    df = {x_title: m_code_t_domain.t_arr_exp,
          y_title: m_code_t_domain.m_code_exp}
    fig = px.line(df, x=x_title, y=y_title,
                  title="M-последовательность во временной области",
                  height=500, width=1400)
    return fig

def get_csk_code_t_domain_figure(csk_code_t_domain: CskSignalTdomain):
    df = {'Input Message': csk_code_t_domain.msg_bits_exp,
          'Demodulated Message': csk_code_t_domain.demodulated_msg_bits_exp,
          'CSK-code': csk_code_t_domain.modulated_code_exp,
          'Время, с': csk_code_t_domain.t_arr}
    fig = px.line(df, x='Время, с',
                  y=['Input Message', 'Demodulated Message', 'CSK-code'],
                  title='CSK-модуляция',
                  height=500, width=1400)

    # Установка толщины линии
    input_msg_line_idx = 0
    fig.data[input_msg_line_idx].update(line={'width': 5})
    demodulated_msg_line_idx = 1
    fig.data[demodulated_msg_line_idx].update(line={'width': 5})
    csk_line_idx = 2
    fig.data[csk_line_idx].update(line={'width': .5})

    return fig
