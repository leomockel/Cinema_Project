from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import statsmodels
import numpy as np


app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

server = app.server




app.title = "Your Movie Playlist Statistics"

# Markdown Text

markdown_text = """
This app is a personnal training project. The movie list comes from a kaggle challenge (IMDB movie extensive dataset),
enriched with a scraping of the website www.imdb.com that i made (scraper_imdb.ipynb). It contains more than 85000 titles with their
imdb id, 
the statistics of every players and every
teams since the 2000-01 season, which means that the stats of a players that plays before are not taken into consideration.
"""





###### Beginning of callbacks ##########################################################################################

@app.callback(
    dash.dependencies.Output('output-container-button1', 'children'),
    [dash.dependencies.Input('position to predict', 'value'), dash.dependencies.Input('stat_category', 'value'), dash.dependencies.Input('my_slider', 'value')])
def pos_predict(value2, value3, value4):

        if len(value3) != 3:
            return "Please select at least 3 column"
        else:
            fig1 = px.scatter_3d(df_stat[df_stat["MPG"] > value4], x=value3[0], y=value3[1], z=value3[2], color=value2)
            fig1.update_layout(title_text='3D plot of stats in function of position', title_x=0.5)

        return html.Div([
            html.Br(),
            dcc.Graph(id='g1', figure=fig1)
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
