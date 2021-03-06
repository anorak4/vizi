# Import required libraries
import pickle
import pathlib
import dash

import datetime as dt
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from ..Dash_fun import apply_layout_with_auth, load_object, save_object
from .callbacks import register_callbacks

# Multi-dropdown options
from .controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS


url_base = '/dash/appoil/'

def Add_Dash(server):
    # get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    app = dash.Dash(__name__,server=server, url_base_pathname=url_base, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
    )
    #server = app.server

    # Create controls
    county_options = [
        {"label": str(COUNTIES[county]), "value": str(county)} for county in COUNTIES
    ]

    well_status_options = [
        {"label": str(WELL_STATUSES[well_status]), "value": str(well_status)}
        for well_status in WELL_STATUSES
    ]

    well_type_options = [
        {"label": str(WELL_TYPES[well_type]), "value": str(well_type)}
        for well_type in WELL_TYPES
    ]


    # Load data
    df = pd.read_csv(DATA_PATH.joinpath("wellspublic.csv"), low_memory=False)
    df["Date_Well_Completed"] = pd.to_datetime(df["Date_Well_Completed"])
    df = df[df["Date_Well_Completed"] > dt.datetime(1960, 1, 1)]

    trim = df[["API_WellNo", "Well_Type", "Well_Name"]]
    trim.index = trim["API_WellNo"]
    dataset = trim.to_dict(orient="index")

    points = pickle.load(open(DATA_PATH.joinpath("points.pkl"), "rb"))


    # Create global chart template
    mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

    layout = dict(
        autosize=True,
        automargin=True,
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=10), orientation="h"),
        title="Satellite Overview",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style="light",
            center=dict(lon=-78.05, lat=42.54),
            zoom=7,
        ),
    )
    apply_layout_with_auth(app, layout)
    # Create app layout
    app.layout = html.Div(
        [
            dcc.Store(id="aggregate_data"),
            # empty Div to trigger javascript file for graph resizing
            html.Div(id="output-clientside"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url("dash-logo.png"),
                                id="plotly-image",
                                style={
                                    "height": "60px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            )
                        ],
                        className="one-third column",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "New York Oil and Gas",
                                        style={"margin-bottom": "0px"},
                                    ),
                                    html.H5(
                                        "Production Overview", style={"margin-top": "0px"}
                                    ),
                                ]
                            )
                        ],
                        className="one-half column",
                        id="title",
                    ),
                    html.Div(
                        [
                            html.A(
                                html.Button("Learn More", id="learn-more-button"),
                                href="https://plot.ly/dash/pricing/",
                            )
                        ],
                        className="one-third column",
                        id="button",
                    ),
                ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                "Filter by construction date (or select range in histogram):",
                                className="control_label",
                            ),
                            dcc.RangeSlider(
                                id="year_slider",
                                min=1960,
                                max=2017,
                                value=[1990, 2010],
                                className="dcc_control",
                            ),
                            html.P("Filter by well status:", className="control_label"),
                            dcc.RadioItems(
                                id="well_status_selector",
                                options=[
                                    {"label": "All ", "value": "all"},
                                    {"label": "Active only ", "value": "active"},
                                    {"label": "Customize ", "value": "custom"},
                                ],
                                value="active",
                                labelStyle={"display": "inline-block"},
                                className="dcc_control",
                            ),
                            dcc.Dropdown(
                                id="well_statuses",
                                options=well_status_options,
                                multi=True,
                                value=list(WELL_STATUSES.keys()),
                                className="dcc_control",
                            ),
                            dcc.Checklist(
                                id="lock_selector",
                                options=[{"label": "Lock camera", "value": "locked"}],
                                className="dcc_control",
                                value=[],
                            ),
                            html.P("Filter by well type:", className="control_label"),
                            dcc.RadioItems(
                                id="well_type_selector",
                                options=[
                                    {"label": "All ", "value": "all"},
                                    {"label": "Productive only ", "value": "productive"},
                                    {"label": "Customize ", "value": "custom"},
                                ],
                                value="productive",
                                labelStyle={"display": "inline-block"},
                                className="dcc_control",
                            ),
                            dcc.Dropdown(
                                id="well_types",
                                options=well_type_options,
                                multi=True,
                                value=list(WELL_TYPES.keys()),
                                className="dcc_control",
                            ),
                        ],
                        className="pretty_container four columns",
                        id="cross-filter-options",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [html.H6(id="well_text"), html.P("No. of Wells")],
                                        id="wells",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="gasText"), html.P("Gas")],
                                        id="gas",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="oilText"), html.P("Oil")],
                                        id="oil",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(id="waterText"), html.P("Water")],
                                        id="water",
                                        className="mini_container",
                                    ),
                                ],
                                id="info-container",
                                className="row container-display",
                            ),
                            html.Div(
                                [dcc.Graph(id="count_graph")],
                                id="countGraphContainer",
                                className="pretty_container",
                            ),
                        ],
                        id="right-column",
                        className="eight columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="main_graph")],
                        className="pretty_container seven columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="individual_graph")],
                        className="pretty_container five columns",
                    ),
                ],
                className="row flex-display",
            ),
            html.Div(
                [
                    html.Div(
                        [dcc.Graph(id="pie_graph")],
                        className="pretty_container seven columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="aggregate_graph")],
                        className="pretty_container five columns",
                    ),
                ],
                className="row flex-display",
            ),
        ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"},
    )




    register_callbacks(app,df,layout,dataset,points)
    
    return app.server

    # # Main
    # if __name__ == "__main__":
    #     app.run_server(debug=True)
