
'''
Regenerative Braking for Hyperloop
MIT Hyperloop III x Imperial College Hyperloop

Streamlit page to accompany the poster: https://www.overleaf.com/read/hssgskqhcqwz


Coded by Raihaan Usman
'''

import numpy as np
from scipy.io import loadmat
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# Page configuration
st.set_page_config(page_title="Regenerative Braking for Hyperloop", layout="wide", initial_sidebar_state="collapsed")

# Set Streamlit beta columns (3 columns)
left, centre, right = st.beta_columns([5,1,1])

with left:
    '''
    # Regenerative Braking for Hyperloop
    ### [MIT Hyperloop III](https://www.mithyperloop.mit.edu/) x [ICLoop](https://www.linkedin.com/company/icloop) - European Hyperloop Week 2021
    '''

with centre:
    st.write("")
    st.write("")
    '''
    ### Scan for our [poster](https://www.researchgate.net/publication/363641006_Simulation_of_a_Hybrid_Energy_Storage_System_Enabling_Regenerative_Braking_of_a_BLDC)!
    '''

with right:
    st.image('qr-code.png', width=150)

# Mode choices (1 or 4)
left, middle, right = st.beta_columns([2,2,3])

with left:
    fpath = ''
    x = st.selectbox("Select an operating mode to view simulation results", ['Mode 1 - 100 RPM','Mode 1 - 300 RPM','Mode 4 - Regenerative Braking'])

    if x == 'Mode 1 - 100 RPM': fpath = 'Mode1_100.mat'; x=1
    elif x == 'Mode 1 - 300 RPM': fpath = 'Mode1_300.mat'; x=2
    else: fpath = 'Mode4.mat'; x=3

with right:
    # Documentation for the app
    st.write("")
    with st.beta_expander("What is this mode about?"):
        if x != 3:
            """
            Mode 1 is the standard pushing state for the pod - the battery system solely powers the motor. The RPM represents different setpoints for the system.
            """
        else:
            """
            Mode 4 is regenerative braking with the battery system as the power sink.
            """

# Load mat-file
mat = loadmat(f'MATLAB_files/{fpath}')

# Conversion to pandas dataframe
df = pd.DataFrame(np.hstack((mat['t'],mat['bat_soc'], mat['rotor_speed'], mat['sc_soc'])),
                    columns=['Time (s)', 'Battery SoC', 'Rotor Speed', 'Supercapacitor SoC']).set_index('Time (s)')

df_torque = pd.DataFrame(np.hstack((mat['t_torque'], mat['rotor_torque'])),
                    columns=['Time (s)', 'Rotor Torque']).set_index('Time (s)')

# Set Streamlit beta columns (2 columns)
col1, col2 = st.beta_columns(2)

# Creating the Plotly figures
bat_soc = go.Figure(
    data=[
        go.Scatter(x=df.index, y=df['Battery SoC'], name='Battery SoC'),
    ],
    layout=go.Layout(
        title='Battery SoC',
        xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
        yaxis=dict(title='SoC (%)', showgrid=False, zeroline=False)
    )
)
rotor_speed = go.Figure(
    data=[
        go.Scatter(x=df.index, y=df['Rotor Speed'], name='Rotor Speed'),
    ],
    layout=go.Layout(
        title='Rotor Speed',
        xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
        yaxis=dict(title='RPM', showgrid=False, zeroline=False)
    )
)
rotor_torque = go.Figure(
    data=[
        go.Scatter(x=df_torque.index, y=df_torque['Rotor Torque'], name='Rotor Torque'),
    ],
    layout=go.Layout(
        title='Rotor Torque',
        xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
        yaxis=dict(title='Nm', showgrid=False, zeroline=False)
    )
)

# Selecting SoC range for demo - won't scale well but will do for the presentation
if x == 1: ran = [90, 100]
elif x == 2: ran = [90, 100]
else: ran = [0, 15]

super_soc = go.Figure(
    data=[
        go.Scatter(x=df.index, y=df['Supercapacitor SoC'], name='Supercapacitor SoC'),
    ],
    layout=go.Layout(
        title='Supercapacitor SoC',
        xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
        yaxis=dict(title='SoC (%)', showgrid=False, zeroline=False, range=ran)
    )
)

# Plotting the graphs
with col1:
    st.plotly_chart(bat_soc)
    st.plotly_chart(super_soc)

with col2:
    st.plotly_chart(rotor_torque)
    st.plotly_chart(rotor_speed)

# Show the raw data in a panda dataframe
with st.beta_expander("View raw data!"):
    one, two = st.beta_columns(2)
    with one:
        st.write(df)
    try:
        with two:
            st.write(df_torque)
    except: pass



st.image('statemach.png')
st.image('dyn.png')
st.image('dyn2.png')
st.image('dyn3.png')
st.image('rl.png')
