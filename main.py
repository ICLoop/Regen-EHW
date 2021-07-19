
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
    ### Link to our poster!
    '''
with right:
    st.image('qr-code.png', width=150)


# Mode choices (1 or 4)
fpath = ''
x = st.selectbox("Select an operating mode to view simulation results", ['Mode 1 - 100 RPM','Mode 1 - 300 RPM','Mode 4 - Regenerative Braking'])

if x == 'Mode 1 - 100 RPM': fpath = 'Mode1_100.mat'
elif x == 'Mode 1 - 300 RPM': fpath = 'Mode1_300.mat'
else: fpath = 'Mode4.mat'

# Load mat-file
mat = loadmat(f'MATLAB_files/{fpath}')

# Conversion to pandas dataframe
try:
    df = pd.DataFrame(np.hstack((mat['t'],mat['bat_soc'], mat['rotor_speed'], mat['rotor_torque'], mat['sc_soc'])),
                        columns=['Time (s)', 'Battery SoC', 'Rotor Speed', 'Rotor Torque', 'Supercapacitor SoC']).set_index('Time (s)')

# Rotor torques throw an error caused by increased precision - save to new dataframe
except ValueError:
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
try:
    rotor_torque = go.Figure(
        data=[
            go.Scatter(x=df.index, y=df['Rotor Torque'], name='Rotor Torque'),
        ],
        layout=go.Layout(
            title='Rotor Torque',
            xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
            yaxis=dict(title='Nm', showgrid=False, zeroline=False)
        )
    )
    super_soc = go.Figure(
        data=[
            go.Scatter(x=df.index, y=df['Supercapacitor SoC'], name='Supercapacitor SoC'),
        ],
        layout=go.Layout(
            title='Supercapacitor SoC',
            xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
            yaxis=dict(title='SoC (%)', showgrid=False, zeroline=False, range=[90,100])
        )
    )
except:
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
    super_soc = go.Figure(
        data=[
            go.Scatter(x=df.index, y=df['Supercapacitor SoC'], name='Supercapacitor SoC'),
        ],
        layout=go.Layout(
            title='Supercapacitor SoC',
            xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
            yaxis=dict(title='SoC (%)', showgrid=False, zeroline=False, range=[0,15])
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

