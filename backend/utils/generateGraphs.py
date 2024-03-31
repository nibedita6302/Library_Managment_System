import os
from flask import current_app as app
from datetime import datetime
import plotly.graph_objs as go
import plotly.io as pio

month = datetime.now().strftime('%B')
year = datetime.now().strftime('%Y')

def create_pie_chart(data, title, filename):    ## Image Only
    labels = list(data.keys())
    values = list(data.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text=title, width=500, height=500)
    
    # pio.show(fig)
    file_path = './static/graphs/'+filename + ".jpeg"
    pio.write_image(fig, file_path)   
    return file_path


def create_bar_graph(data, title, filename):    ## Image Only
    x = list(data.keys())
    y = list(data.values())
    
    color = ['cyan', 'purple', 'green', 'orange', 'pink', 'lightgreen','violet', 'blue', 'red', 'yellow', 'olive']
    color_set = color*(len(x)//len(color) + 1)

    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color=color_set[:len(x)], line=dict(width=0.4)))])
    fig.update_layout(title_text=title, xaxis_title='Author', yaxis_title='Reads',
                      paper_bgcolor='white',  # Set background color
                      plot_bgcolor='lightyellow',  # Set plot area color
                      width=800, height=600)    # Set overall graph size

    # pio.show(fig)
    file_path = './static/graphs/'+filename + ".jpeg"
    pio.write_image(fig, file_path)   
    return file_path

def html_pie_chart(data, title, filename):  ## HTML Only
    # print(data)
    labels = [d[0] for d in data]
    values = [d[1] for d in data]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text=title, width=500, height=500)

    file_path = os.path.join(app.config['UPLOAD_FOLDER']+'graphs/',filename+'.html')
    pio.write_html(fig, file_path)   
    return filename+'.html'

def html_bar_chart(data, title, filename):  ## HTML Only
    # print(data)
    x = [d[0] for d in data]
    y = [d[1] for d in data]

    color = ['cyan', 'purple', 'green', 'orange', 'pink', 'lightgreen','violet', 'blue', 'red', 'yellow', 'olive']
    color_set = color*(len(x)//len(color) + 1)

    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color=color_set[:len(x)], line=dict(width=0.4)))])
    fig.update_layout(title_text=title, xaxis_title='Author', yaxis_title='Reads',
                      paper_bgcolor='white',  # Set background color
                      plot_bgcolor='lightyellow',  # Set plot area color
                      width=800, height=600)    # Set overall graph size
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER']+'graphs/',filename+'.html')
    pio.write_html(fig, file_path)   
    return filename+'.html'