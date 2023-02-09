import plotly.express as px
from signal_processing.m_code_generator import McodeTdomain


def get_m_code_t_domain_figure(m_code_t_domain: McodeTdomain):
    x_title = 'Время, с'
    y_title = 'Амплитуда'
    df = {x_title: m_code_t_domain.t_arr,
          y_title: m_code_t_domain.m_code}
    fig = px.line(df, x=x_title, y=y_title,
                  title="M-последовательность во временной области",
                  height=500, width=1400)
    return fig
