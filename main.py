import numpy as np
from scipy.io import loadmat  # this is the SciPy module that loads mat-files
import pandas as pd
import streamlit as st
import plotly.express as px

st.markdown('<style>a{color: white;}</style>', unsafe_allow_html=True)
'''
# Regenerative Braking for Hyperloop '''
st.markdown("### <a href=\"https://www.mithyperloop.mit.edu/\">MIT Hyperloop III</a> x [ICLoop](https://www.linkedin.com/company/icloop) - European Hyperloop Week 2021", unsafe_allow_html=True)

st.write("")

# Sidebar with mode choices (1 or 4)
with st.sidebar:
    fpath = ''
    x = st.selectbox("Select an operating mode", ['Mode 1 - 100 RPM','Mode 1 - 300 RPM','Mode 4 - Regenerative Braking'])
    if x == 'Mode 1 - 100 RPM':
        fpath = 'Mode1_100.mat'
    elif x == 'Mode 1 - 300 RPM':
        fpath = 'Mode1_300.mat'
    else:
        fpath = 'Mode4.mat'


mat = loadmat(f'MATLAB_files/{fpath}')  # load mat-file

df = pd.DataFrame(np.hstack((mat['t'], mat['bat_soc'], mat['rotor_speed'], mat['rotor_torque'], mat['sc_soc'])),
                    columns=['Time (s)', 'Battery SoC', 'Rotor Speed', 'Rotor Torque', 'Supercapacitor SoC'])

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