import dash
#import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import pandas as pd
from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html
from flask_pymongo import PyMongo

url_base = '/dash/test1/'

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

#external_stylesheets = ['test1.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'test': 'test'
}

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#pip install dash==1.12.0
#pip install dash-auth==1.3.2
# auth = dash_auth.BasicAuth(app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )


def Add_Dash(server, mongo):
    #server.config["MONGO_URI"] = "mongodb://localhost:27017/Dashboard"
    app = Dash(__name__,server=server, url_base_pathname=url_base,external_stylesheets = external_stylesheets, )
    
    #app.config["MONGO_URI"] = "mongodb://localhost:27017/Dashboard"
    #mongo = PyMongo()
    #mongo.init_app(server)
    #df = pd.read_json(mongo.db.gapminderDataFiveYear)
    # Make a query to the specific DB and Collection
    cursor = mongo.db['gapminderDataFiveYear'].find({})

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    layout = html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            step=None
        )
    ])
    apply_layout_with_auth(app, layout)
    @app.callback(
        Output('graph-with-slider', 'figure'),
        [Input('year-slider', 'value')])
    def update_figure(selected_year):
        cursor = mongo.db['gapminderDataFiveYear'].find({})
        df =  pd.DataFrame(list(cursor))
        filtered_df = df[df.year == selected_year]
        traces = []
        for i in filtered_df.continent.unique():
            df_by_continent = filtered_df[filtered_df['continent'] == i]
            traces.append(dict(
                #type='bar',
                x=df_by_continent['gdpPercap'],
                y=df_by_continent['lifeExp'],
                text=df_by_continent['country'],
                mode='lines',
                opacity=0.7,
                markers={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))

        return {
            'data': traces,
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita',
                    'range':[2.3, 4.8]},
                yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                transition = {'duration': 500},
            )
        }
    return app.server

#if __name__ == '__main__':
#    app.run_server(debug=True)
