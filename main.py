import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Regenerative Braking for Hyperloop",layout="wide")

'''
# Regenerative Braking for Hyperloop
### [MIT Hyperloop III](https://www.mithyperloop.mit.edu/) x [ICLoop](https://www.linkedin.com/company/icloop) - European Hyperloop Week 2021
'''
st.write("")

# Sidebar with mode choices (1 or 4)
# with st.sidebar:
fpath = ''
x = st.selectbox("Select an operating mode", ['Mode 1 - 100 RPM','Mode 1 - 300 RPM','Mode 4 - Regenerative Braking'])
if x == 'Mode 1 - 100 RPM':
    fpath = 'Mode1_100.mat'
elif x == 'Mode 1 - 300 RPM':
    fpath = 'Mode1_300.mat'
else:
    fpath = 'Mode4.mat'


mat = loadmat(f'MATLAB_files/{fpath}')  # load mat-file

df = pd.DataFrame(np.hstack((mat['t'],mat['bat_soc'], mat['rotor_speed'], mat['rotor_torque'], mat['sc_soc'])),
                    columns=['Time (s)', 'Battery SoC', 'Rotor Speed', 'Rotor Torque', 'Supercapacitor SoC']).set_index('Time (s)')

# Set streamlit beta columns (2 columns)
col1, col2 = st.beta_columns(2)

with col1:
    bat_soc = st.line_chart(df['Battery SoC'])
    rotor_speed = st.line_chart(df['Rotor Speed'])
with col2:
    rotor_torque = st.line_chart(df['Rotor Torque'])
    sc_soc = st.line_chart(df['Supercapacitor SoC'])

b_soc = go.Figure(
    data=[
        go.Scatter(x=df.index, y=df['Battery SoC'], name='Battery SoC'),
    ],
    layout=go.Layout(
        title='Battery SoC',
        xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
        yaxis=dict(title='SoC (%)', showgrid=False, zeroline=False)
    )
)

r_speed = go.Figure(
    data=[
        go.Scatter(x=df.index, y=df['Rotor Speed'], name='Rotor Speed'),
    ],
    layout=go.Layout(
        title='Rotor Speed',
        xaxis=dict(title='Time (s)', showgrid=False, zeroline=False),
        yaxis=dict(title='RPM', showgrid=False, zeroline=False)
    )
)

r_torque = go.Figure(
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



with col1:
    st.plotly_chart(b_soc)
    st.plotly_chart(super_soc)
with col2:
    st.plotly_chart(r_torque)
    st.plotly_chart(r_speed)


# Use streamlit add_rows to add the data to the plotly chart once every 0.1 seconds
# for i in range(1000):
#     fig.add_rows([df['Battery SoC'][i]])
#     time.sleep(0.1)


with st.beta_expander("View raw data!"):
    st.write(df)




# st.write(mat['__function_workspace__'])  # look at the available keys
# mdata = mat['t']  # variable in mat file
# mdtype = mdata.dtype  # dtypes of structures are "unsized objects"
# # * SciPy reads in structures as structured NumPy arrays of dtype object
# # * The size of the array is the size of the structure array, not the number
# #   elements in any particular field. The shape defaults to 2-dimensional.
# # * For convenience make a dictionary of the data using the names from dtypes
# # * Since the structure has only one element, but is 2-D, index it at [0, 0]
# ndata = {n: mdata[n][0, 0] for n in mdtype.names}
# # Reconstruct the columns of the data table from just the time series
# # Use the number of intervals to test if a field is a column or metadata
# columns = [n for n, v in ndata.iteritems() if v.size == ndata['numIntervals']]
# # now make a data frame, setting the time stamps as the index
# df = pd.DataFrame(np.concatenate([ndata[c] for c in columns], axis=1),
#                   index=[datetime(*ts) for ts in ndata['timestamps']],
#                   columns=columns)











# progress_bar = st.progress(0)
# status_text = st.empty()
# chart = st.line_chart(np.random.randn(10, 2))

# for i in range(100):
#     # Update progress bar.
#     progress_bar.progress(i + 1)

#     new_rows = np.random.randn(10, 2)

#     # Update status text.
#     status_text.text(
#         'The latest random number is: %s' % new_rows[-1, 1])

#     # Append data to the chart.
#     chart.add_rows(new_rows)

#     # Pretend we're doing some computation that takes time.
#     time.sleep(0.1)

# status_text.text('Done!')
# st.balloons()