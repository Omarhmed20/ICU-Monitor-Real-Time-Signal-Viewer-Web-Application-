import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from plotly.subplots import make_subplots
import plotly.io as pio
from PyPDF2 import PdfFileReader, PdfFileMerger
import PyPDF2
st. set_page_config(layout="wide")
pio.templates.default = "simple_white"

# Enable sticky sidebar
st.markdown(
    """
    <style>
        .css-1544g2n {
        padding: 1rem 1rem 1.5rem;
        }
  </style>
    """,
    unsafe_allow_html=True,
)
st.title("Signal Viewer")
col5, col6 = st.columns(2)

side=st.sidebar
frames =[]
with side:
    link = st.checkbox('Linking Graphs', value=False)


    st.subheader("Signal 1")
    file = st.file_uploader("Upload Files", type={"csv", "txt", "xlsx"})


    signalSpeed = st.slider('Signal Speed', min_value= 1, max_value =4, step =1)
    col1, col2 = st.columns(2)
    
    with col1:
        signalname1 = st.text_input("signal 1", value="title",)
    with col2:
        SignalColor1 = st.color_picker( 'Pick A Color', '#00f900',label_visibility="visible",key = "Color 1")



    st.subheader("Signal 2")    
    file2 = st.file_uploader("Upload Files", type={"csv", "txt", "xlsx"},key = '2nd File')

    
    if link ==False:
        signalSpeed2 = st.slider('Signal Speed', min_value= 1, max_value =4, step =1,key='sigSpeed2')

    col3, col4 = st.columns(2)
    
    with col3:
        signalname2 = st.text_input("signal 2",value ="title")
    with col4:
        SignalColor2 = st.color_picker( 'Pick A Color', '#00f900',label_visibility="visible",key = "Color 2")

    

if 'IsRead1' not in st.session_state:
    st.session_state['IsRead1'] = 0
if 'Isread2' not in st.session_state:
    st.session_state['Isread2'] = 0
if 'Isread3' not in st.session_state:
    st.session_state['Isread3'] = 0
    
    

if 'Signal1frames' not in st.session_state:
    st.session_state['Signal1frames'] = []
if 'Signal2Frames' not in st.session_state:
    st.session_state['Signal2Frames'] = []
if 'LinkedGraphFrames' not in st.session_state:
    st.session_state['LinkedGraphFrames'] = []


if 'LinkedSignal2X' not in st.session_state:
    st.session_state['LinkedSignal2X'] = []
if 'LinkedSignal2Y' not in st.session_state:
    st.session_state['LinkedSignal2Y'] = []
if 'LinkedSignal1X' not in st.session_state:
    st.session_state['LinkedSignal1X'] = []           
if 'LinkedSignal1Y' not in st.session_state:
    st.session_state['LinkedSignal1Y'] = []


if 'Signal1X' not in st.session_state:
    st.session_state['Signal1X'] = []
if 'Signal2X' not in st.session_state:
    st.session_state['Signal2X'] = []
if 'Signal1Y' not in st.session_state:
    st.session_state['Signal1Y'] = []
if 'Signal2Y' not in st.session_state:
    st.session_state['Signal2Y'] = []


if 'x_int' not in st.session_state:
    st.session_state['x_int'] = []
if 'y_int' not in st.session_state:
    st.session_state['y_int'] = []


#-----------------------------------------------------------------------------------------

if file is not None and st.session_state['IsRead1'] == 0:
    st.session_state['IsRead1'] = 1
    File = pd.read_csv(file)

    for f in range(1,500+1):
        st.session_state['Signal1X'].append(File.iloc[f,0])
        st.session_state['Signal1Y'].append(File.iloc[f,1])
        
        curr_frame = go.Frame( dict(
            data = [go.Scatter(x =  st.session_state['Signal1X'], y = st.session_state['Signal1Y'],mode = "lines",),#update the trace 1 in (1,1)
                    ],
            traces=[0]# the elements of the list [0,1,2] give info on the traces in fig.data
                                    # that are updated by the above three go.Scatter instances
            ))
        st.session_state['Signal1frames'].append(curr_frame)

#---------------------------------------------------------------------------------------

if file2 is not None and st.session_state['Isread2'] == 0:
    st.session_state['Isread2'] = 1
    File2 = pd.read_csv(file2)

    for f in range(1,500+1):
        st.session_state['Signal2X'] = np.array(File2.iloc[0:f+1,0])
        st.session_state['Signal2Y'] = np.array(File2.iloc[0:f+1,1])
        curr_frame2 = go.Frame( dict(
            data = [go.Scatter(x =  st.session_state['Signal2X'], y = st.session_state['Signal2Y'],mode = "lines",)#update the trace 1 in (1,1)
                    ],
            traces=[0] # the elements of the list [0,1,2] give info on the traces in fig.data
                                    # that are updated by the above three go.Scatter instances
            ))
        st.session_state['Signal2Frames'].append(curr_frame2)
        
#---------------------------------------------------------------------------------------


if link == False:

    
    figure = go.Figure(
        frames = [fr.update(
            layout={
                "xaxis": {"range": [max(fr.data[0].x) - 1, max(fr.data[0].x) + 0.1]},
                "yaxis": {"range": [min(fr.data[0].y) - 0.2, max(fr.data[0].y) + 0.2]}
            }
        )for fr in st.session_state['Signal1frames']]
        )
    figure.update_layout(width=600, height=475)


    figure.update_layout(showlegend=True,title=dict(text="Graph #1"), 
                        xaxis={
                            'showgrid':False,
                            'linecolor':'#000000',
                            
                            'ticks':'outside',
                            'showline':True
                        },
                        updatemenus=[dict(buttons = [dict(
                                               args2 = [None, {"frame": {"duration": (300/signalSpeed), 
                                                                        "redraw": True},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 0}}],
                                                 args = [[None], {"frame": {"duration": 0, "redraw": False},
                                                                "mode": "immediate",
                                                                "transition": {"duration": 0}}],
                                               label = "▶ / ❚❚",
                                               method = "animate"),dict(
                                               args = [None, {"frame": {"duration": (300/signalSpeed), 
                                                                        "redraw": True},
                                                              "fromcurrent": False, 
                                                              "transition": {"duration": 0}}],
                                               label = "■",
                                               method = "animate")],
            type='buttons',
            showactive=False,
            xanchor='left',
            yanchor='bottom',
            x=-0.1,
            y=-0.3,
            direction='right',
            pad={"r": 10, "t": 10},
)]
                        )

    figure.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=SignalColor1),name=signalname1),)


    

    if file is not None:
        with col5:
            st.write(figure)
        plot=go.Figure(go.Scatter(x =st.session_state['Signal1X'], y = st.session_state['Signal1Y'],mode = "lines",line=dict(color=SignalColor1)))

#--------------------------------------------------------------------------------------

    figure2 = go.Figure(
        frames = [fr.update(
            layout={
                "xaxis": {"range": [max(fr.data[0].x) - 1, max(fr.data[0].x)]},
                "yaxis": {"range": [min(fr.data[0].y), max(fr.data[0].y)]}
            }
        )for fr in st.session_state['Signal2Frames']]
        )
    figure2.update_layout(width=600, height=475)


    figure2.update_layout(showlegend=True,title=dict(text="Graph #2"), 
                        xaxis={
                            'showgrid':False,
                            'linecolor':'#000000',
                            
                            'ticks':'outside',
                            'showline':True
                        },
                        updatemenus=[dict(buttons = [dict(
                                               args2 = [None, {"frame": {"duration": (300/signalSpeed2), 
                                                                        "redraw": True},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 0}}],
                                                 args = [[None], {"frame": {"duration": 0, "redraw": False},
                                                                "mode": "immediate",
                                                                "transition": {"duration": 0}}],
                                               label ="▶ / ❚❚",
                                               method = "animate"),dict(
                                               args = [None, {"frame": {"duration": (300/signalSpeed2), 
                                                                        "redraw": True},
                                                              "fromcurrent": False, 
                                                              "transition": {"duration": 0}}],
                                               label = "■",
                                               method = "animate")],
            type='buttons',
            showactive=False,
            xanchor='left',
            yanchor='bottom',
            x=-0.1,
            y=-0.3,
            direction='right',
            pad={"r": 10, "t": 10},
)]
                        )

    figure2.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=SignalColor2),name=signalname2),)
    

    if file2 is not None:
        with col6:
            st.write(figure2)


#--------------------------------------------------------------------------------------
j=-1
i = -1
if link ==True:
    if st.session_state['Isread3'] == 2:
        del st.session_state['LinkedGraphFrames']
        st.session_state['LinkedGraphFrames'] = []

    if st.session_state['Isread3'] != 2:
        st.session_state['Isread3'] =2


    for fr in st.session_state['Signal2Frames']:  
        
        st.session_state['LinkedSignal2X'].append(fr.data[0].x)
        st.session_state['LinkedSignal2Y'].append(fr.data[0].y)
        j=j+1
    
    if len(st.session_state['Signal2Frames'])>1 and len(st.session_state['Signal1frames'])>1:    
        for fr in  st.session_state['Signal1frames']:
                st.session_state['LinkedSignal1X'].append(fr.data[0].x)
                st.session_state['LinkedSignal1Y'].append(fr.data[0].y)
                curr_frame = go.Frame( dict(
                data = [go.Scatter(x =  st.session_state['LinkedSignal1X'][i], y = st.session_state['LinkedSignal1Y'][i],mode = "lines",),#update the trace 1 in (1,1)
                        go.Scatter(x =  st.session_state['LinkedSignal2X'][i], y = st.session_state['LinkedSignal2Y'][i],mode = "lines",)
                        ],
                traces=[0,1]# the elements of the list [0,1] give info on the traces in fig.data
                                        # that are updated by the above three go.Scatter instances
                ))
                i=i+1
                st.session_state['LinkedGraphFrames'].append(curr_frame)

    if len(st.session_state['Signal2Frames'])<1 and len(st.session_state['Signal1frames'])>1:    
        for fr in  st.session_state['Signal1frames']:
                st.session_state['LinkedSignal1X'].append(fr.data[0].x)
                st.session_state['LinkedSignal1Y'].append(fr.data[0].y)
                curr_frame = go.Frame( dict(
                data = [go.Scatter(x =  st.session_state['LinkedSignal1X'][i], y = st.session_state['LinkedSignal1Y'][i],mode = "lines",),#update the trace 1 in (1,1)
                        ],
                traces=[0]# the elements of the list [0] give info on the traces in fig.data
                                        # that are updated by the above three go.Scatter instances
                ))
                i=i+1
                st.session_state['LinkedGraphFrames'].append(curr_frame)
    
    if len(st.session_state['Signal2Frames'])>1 and len(st.session_state['Signal1frames'])<1:    
        for fr in  st.session_state['Signal2Frames']:
                curr_frame = go.Frame( dict(
                data = [
                        go.Scatter(x =  st.session_state['LinkedSignal2X'][i], y = st.session_state['LinkedSignal2Y'][i],mode = "lines",)
                        ],
                traces=[1]# the elements of the list [1] give info on the traces in fig.data
                                        # that are updated by the above three go.Scatter instances
                ))
                j=j+1
                st.session_state['LinkedGraphFrames'].append(curr_frame)

    frames5 = [fr.update(
        layout={
            "xaxis": {"range": [max(fr.data[0].x) - 1, max(fr.data[0].x)]},
            "yaxis": {"range": [-1,1]}
        }
    )for fr in st.session_state['LinkedGraphFrames']]
           
                       
    fig = make_subplots(rows=2, cols=1, subplot_titles = ('Graph #1', 'Graph #2'),shared_xaxes='all',shared_yaxes='all',)
    fig.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=SignalColor1),name = signalname1), row=1, col=1);
    fig.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=SignalColor2),name = signalname2), row=2, col=1);
    fig.update_layout(width=1500, height=750)
    
    fig.update_yaxes(range=[0, 9]);#this line updates both yaxis, and yaxis2 range


    updatemenus=annotations=[dict(buttons = [dict(
                                               args2 = [None, {"frame": {"duration": (200/signalSpeed), 
                                                                        "redraw": True},
                                                              "fromcurrent": True, 
                                                              "transition": {"duration": 0}}],
                                                 args = [[None], {"frame": {"duration": 0, "redraw": False},
                                                                "mode": "immediate",
                                                                "transition": {"duration": 0}}],
                                               label = "▶ / ❚❚",
                                               method = "animate"),dict(
                                               args = [None, {"frame": {"duration": (200/signalSpeed), 
                                                                        "redraw": True},
                                                              "fromcurrent": False, 
                                                              "transition": {"duration": 0}}],
                                               label = "■",
                                               method = "animate")],
            type='buttons',
            showactive=False,
            xanchor='left',
            yanchor='bottom',
            x=-0.1,
            y=-0.3,
            direction='right',
            pad={"r": 10, "t": 10},
)]
                        


    fig.update(frames=frames5)
    fig.update_layout(updatemenus=updatemenus, )
    

    st.write(fig)
