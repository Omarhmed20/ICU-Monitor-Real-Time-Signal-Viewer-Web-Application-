import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
import plotly_express as px
from plotly.subplots import make_subplots

import plotly.io as pio
pio.templates.default = "simple_white"

def getnums(s, e,i):
   return list(range(s, e,i))
frames =[]

st.sidebar.subheader("Dataset")
file = st.sidebar.file_uploader("Upload Files", type={"csv", "txt", "xlsx"})
file2 = st.sidebar.file_uploader("Upload Files", type={"csv", "txt", "xlsx"},key = '2nd File')
num_of_traces = st.sidebar.number_input('Select Number of traces', min_value=1)
if 'read1' not in st.session_state:
            st.session_state['read1'] = 0
if 'read2' not in st.session_state:
            st.session_state['read2'] = 0

color1 = st.sidebar.color_picker( 'Pick A Color', '#00f900',label_visibility="visible",key = "Color 1")
color2 = st.sidebar.color_picker( 'Pick A Color', '#00f900',label_visibility="visible",key = "Color 2")
signalname1 = st.sidebar.text_input("signal 1", value="title",)
signalname2 = st.sidebar.text_input("signal 2",value ="title")
link = st.checkbox('link', value=False)

if 'frames' not in st.session_state:
            st.session_state['frames'] = []

if 'frames2' not in st.session_state:
            st.session_state['frames2'] = []
if 'frames3' not in st.session_state:
            st.session_state['frames3'] = []

if 'x' not in st.session_state:
        st.session_state['x'] = []
if 'x2' not in st.session_state:
        st.session_state['x2'] = []

if 'y' not in st.session_state:
        st.session_state['y'] = []
if 'y2' not in st.session_state:
        st.session_state['y2'] = []
if 'x_int' not in st.session_state:
    st.session_state['x_int'] = np.array([1])

if 'int_data' not in st.session_state:
    st.session_state['int_data'] = []

if 'current_data' not in st.session_state:
    st.session_state['current_data'] = []

if 'current_data2' not in st.session_state:
    st.session_state['current_data2'] = []

if 'y_int' not in st.session_state:
    st.session_state['y_int'] = []


#-----------------------------------------------------------------------------------------

if file is not None and st.session_state['read1'] == 0:
    print(st.session_state['read1'] )
    print(np.arange(1,num_of_traces+1))
    st.session_state['read1'] = 1
    st.write(type(file))
    File = pd.read_csv(file)

    # st.experimental_rerun()

    for f in range(1,File.shape[0]+1):
        st.session_state['x'] = np.arange(1,f+1)
        st.session_state['y'] = np.array(File.iloc[0:f+1,0])
        st.session_state['current_data'] = []
        st.session_state['current_data'].append(go.Scatter(x =  st.session_state['x'], y = st.session_state['y'],mode = "lines",))
        curr_frame = go.Frame( dict(
            data = [go.Scatter(x =  st.session_state['x'], y = st.session_state['y'],mode = "lines",),#update the trace 1 in (1,1)
                    go.Scatter(x =  st.session_state['x'], y = st.session_state['y'],mode = "lines",),
                    go.Scatter(x =  st.session_state['x'], y = st.session_state['y'],mode = "lines",),
                    go.Scatter(x =  st.session_state['x'], y = st.session_state['y'],mode = "lines",),
                    ],
            traces=getnums(0, num_of_traces,1)# the elements of the list [0,1,2] give info on the traces in fig.data
                                    # that are updated by the above three go.Scatter instances
            ))
        st.session_state['frames'].append(curr_frame)
        
#---------------------------------------------------------------------------------------

if file2 is not None and st.session_state['read2'] == 0:
    print(st.session_state['read2'] )
    st.session_state['read2'] = 1
    st.write(type(file2))
    File2 = pd.read_csv(file2)

    # st.experimental_rerun()

    
    for f in range(1,File2.shape[0]+1):
        st.session_state['x2'] = np.arange(1,f+1)
        st.session_state['y2'] = np.array(File2.iloc[0:f+1,0])
        st.session_state['current_data2'] = []
        st.session_state['current_data2'].append(go.Scatter(x =  st.session_state['x2'], y = st.session_state['y2'],mode = "lines",))
        curr_frame2 = go.Frame( dict(
            data = [go.Scatter(x =  st.session_state['x2'], y = st.session_state['y2'],mode = "lines",)#update the trace 1 in (1,1)
                    ],
            traces=[0] # the elements of the list [0,1,2] give info on the traces in fig.data
                                    # that are updated by the above three go.Scatter instances
            ))
        st.session_state['frames2'].append(curr_frame2)
        
#---------------------------------------------------------------------------------------


if link == False:

    
    figure = go.Figure(
        frames = [fr.update(
            layout={
                "xaxis": {"range": [max(fr.data[0].x) - 10, max(fr.data[0].x)]},
            }
        )for fr in st.session_state['frames']]
        )
    figure.update_layout(width=700, height=475)


    figure.update_layout(title=dict(text="Graph #1"), 
                        xaxis={
                            'showgrid':False,
                            'linecolor':'#000000',
                            'mirror':True,
                            'ticks':'outside',
                            'showline':True
                        },
                        updatemenus=[dict(buttons = [dict(
                                               args = [None, {"frame": {"duration": 200, 
                                                                        "redraw": True},
                                                              "fromcurrent": False, 
                                                              "transition": {"duration": 0}}],
                                               label = "Play",
                                               method = "animate"),dict(
                                               args = [None, {"frame": {"duration": 50, 
                                                                        "redraw": True},
                                                              "fromcurrent": False, 
                                                              "transition": {"duration": 0}}],
                                               label = "Play X2",
                                               method = "animate"),dict(
                                               args = [[None], {"frame": {"duration": 0, "redraw": False},
                                                                "mode": "immediate",
                                                                "transition": {"duration": 0}}],
                                               label = "Pause",
                                               method = "animate")],
                                type='buttons',
                                showactive=False,
                                xanchor='right',
                                yanchor='top')]
                        )

    figure.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=color1),name=signalname1),)
    figure.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=color1),name=signalname1),)
    figure.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=color1),name=signalname1),)
    figure.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=color1),name=signalname1),)


    


    st.write(figure)

#--------------------------------------------------------------------------------------

    figure2 = go.Figure(
        frames = [fr.update(
            layout={
                "xaxis": {"range": [max(fr.data[0].x) - 10, max(fr.data[0].x)]},
            }
        )for fr in st.session_state['frames2']]
        )
    figure2.update_layout(width=700, height=475)


    figure2.update_layout(title=dict(text="Graph #2"), 
                        xaxis={
                            'showgrid':False,
                            'linecolor':'#000000',
                            'mirror':True,
                            'ticks':'outside',
                            'showline':True
                        },
                        updatemenus=[dict(buttons = [dict(
                                               args = [None, {"frame": {"duration": 200, 
                                                                        "redraw": True},
                                                              "fromcurrent": False, 
                                                              "transition": {"duration": 0}}],
                                               label = "Play",
                                               method = "animate"),dict(
                                               args = [None, {"frame": {"duration": 50, 
                                                                        "redraw": True},
                                                              "fromcurrent": False, 
                                                              "transition": {"duration": 0}}],
                                               label = "Play X2",
                                               method = "animate"),dict(
                                               args = [[None], {"frame": {"duration": 0, "redraw": False},
                                                                "mode": "immediate",
                                                                "transition": {"duration": 0}}],
                                               label = "Pause",
                                               method = "animate")],
                                type='buttons',
                                showactive=False,
                                xanchor='right',
                                yanchor='top')]
                        )

    figure2.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=color2),name=signalname2),)
    


    st.write(figure2)



#--------------------------------------------------------------------------------------

if link ==True:
    st.session_state['frames3'] =  st.session_state['frames'] +st.session_state['frames2']

    frames2 = [fr.update(
                layout={
                    "xaxis": {"range": [max(fr.data[0].x) - 10, max(fr.data[0].x)]},
                }
            )for fr in st.session_state['frames3']]
    fig = make_subplots(rows=2, cols=1, subplot_titles = ('Subplot (1,1)', 'Subplot(1,2)'),shared_xaxes='all',shared_yaxes='all')
    fig.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=color1)), row=1, col=1);
    fig.add_trace(go.Scatter(x =st.session_state['x_int'], y = st.session_state['y_int'],mode = "lines",line=dict(color=color2)), row=2, col=1);
    len(fig.data)

    fig.layout
    fig.update_layout(width=700, height=475)
    fig.update_yaxes(range=[0, 9]);#this line updates both yaxis, and yaxis2 range


    updatemenus=[dict(buttons = [dict(
                                                args = [None, {"frame": {"duration": 200, 
                                                                            "redraw": True},
                                                                "fromcurrent": True, 
                                                                "transition": {"duration": 0},
                                                                "visible": [True, False]}],
                                                label = "Play",
                                                method = "animate"),dict(
                                                args = [None, {"frame": {"duration": 50, 
                                                                            "redraw": True},
                                                                "fromcurrent": True, 
                                                                "transition": {"duration": 0}}],
                                                label = "Play X2",
                                                method = "animate"),dict(
                                                args = [[None], {"frame": {"duration": 0, "redraw": False},
                                                                    "mode": "immediate",
                                                                    "transition": {"duration": 0}}],
                                                label = "Pause",
                                                method = "animate"),],
                                    type='buttons',
                                    showactive=False,
                                    xanchor='right',    
                                    yanchor='top')]


    fig.update(frames=frames2),
    fig.update_layout(updatemenus=updatemenus,
                    );
    st.write(fig)


