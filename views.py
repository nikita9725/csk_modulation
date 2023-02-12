from dash import dcc

from signal_processing.m_code_generator import McodeGenerator
from signal_processing.csk_modulator import CskModulator
from figures import (
    get_m_code_t_domain_figure,
    get_csk_code_t_domain_figure,
)
from utils import HtmlDivRegister


@HtmlDivRegister()
def show_m_code():
    m_code_gen = McodeGenerator()
    m_code_t_domain = m_code_gen.get_m_code_t_domain()
    fig = get_m_code_t_domain_figure(m_code_t_domain)

    return dcc.Graph(figure=fig)


@HtmlDivRegister()
def show_csk_code():
    m_code_gen = McodeGenerator()
    m_code_t_domain = m_code_gen.get_m_code_t_domain()

    csk_modulatior = CskModulator(m_code_t_domain)
    message = (0, 0, 3, 3, 1, 1)
    csk_t_domain = csk_modulatior.modulate_t_domain(message)
    fig = get_csk_code_t_domain_figure(csk_t_domain)

    return dcc.Graph(figure=fig)