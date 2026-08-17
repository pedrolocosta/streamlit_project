import pandas as pd
import scipy.stats
import streamlit as st
import time

# estas são variáveis persistentes preservadas à medida que o Streamlin executa novamente esse script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iterations', 'mean'])

if 'coin_series' not in st.session_state:
    st.session_state['coin_series'] = []

st.header('Jogando uma moeda')

chart_placeholder = st.empty()
chart_placeholder.line_chart(pd.DataFrame({'mean': [0.5]}))


def toss_coin(n):
    '''This function simulates tossing a coin n times and returns the mean of the outcomes.'''

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0
    series = []

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        series.append(mean)
        chart_placeholder.line_chart(pd.DataFrame({'mean': series}))
        time.sleep(0.05)

    return mean


number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
start_button = st.button('Executar')

if start_button:
    st.write(f'Executando o experimento de {number_of_trials} tentativas.')
    st.session_state['experiment_no'] += 1
    st.session_state['coin_series'] = []
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iterations', 'mean'])
    ],
        axis=0)
    st.session_state['df_experiment_results'] = \
        st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
