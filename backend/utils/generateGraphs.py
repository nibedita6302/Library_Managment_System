from datetime import datetime
import plotly.graph_objs as go
import plotly.io as pio

month = datetime.now().strftime('%B')
year = datetime.now().strftime('%Y')

def create_pie_chart(data, title, filename):    ## Image Only
    labels = data.keys()
    values = data.values()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text=title, width=500, height=500)
    
    # pio.show(fig)
    pio.write_image(fig, './static/graphs/'+filename + ".jpeg")      

def create_bar_graph(data, title, filename):    ## Image Only
    x = data.keys()
    y = data.values()
    color = ['cyan', 'purple', 'green', 'orange', 'pink', 'lightgreen','violet', 'blue', 'red', 'yellow', 'olive']
    color_set = color*(len(x)//len(color) + 1)

    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color=color_set[:len(x)], line=dict(width=0.4)))])
    fig.update_layout(title_text=title, xaxis_title='Author', yaxis_title='Reads',
                      paper_bgcolor='white',  # Set background color
                      plot_bgcolor='lightyellow',  # Set plot area color
                      width=800, height=600)    # Set overall graph size

    # pio.show(fig)
    pio.write_image(fig, './static/graphs/'+filename + ".jpeg")  

def html_pie_chart(data, title, filename):  ## HTML Only
    labels = data.keys()
    values = data.values()

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text=title, width=500, height=500)

    pio.write_html(fig, './static/graphs/'+filename+'.html')    

def html_bar_chart(data, title, filename):  ## HTML Only
    x = data.keys()
    y = data.values()

    color = ['cyan', 'purple', 'green', 'orange', 'pink', 'lightgreen','violet', 'blue', 'red', 'yellow', 'olive']
    color_set = color*(len(x)//len(color) + 1)

    fig = go.Figure([go.Bar(x=x, y=y, marker=dict(color=color_set[:len(x)], line=dict(width=0.4)))])
    fig.update_layout(title_text=title, xaxis_title='Author', yaxis_title='Reads',
                      paper_bgcolor='white',  # Set background color
                      plot_bgcolor='lightyellow',  # Set plot area color
                      width=800, height=600)    # Set overall graph size
    
    pio.write_html(fig, './static/graphs/'+filename+'.html') 