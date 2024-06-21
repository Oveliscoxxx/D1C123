from dash.dependencies import Input, Output, State
from shapely.geometry import LineString, MultiLineString
from dash.dependencies import Input, Output

# from dash import Dash, dcc, html, Input, Output, callback
import dash_daq as daq

from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page

register_page(__name__, path="/")

# from urllib.request import urlopen

################################
# design for mapbox
bgcolor = "#f3f3f1"  # mapbox light map land color
row_heights = [150, 500, 300]
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}


def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }


# Create app layout
layout = html.Div(
    [
        html.Div
        (
            [
                dbc.Row
                (
                    [
                        # dbc.Col
                        # (
                        #     html.Img
                        #     (
                        #         src=".\\assets\\icon.png",
                        #         style={"float": "right",
                        #                "margin-right": "155px",
                        #                "height": "324px",
                        #                "width": "auto",
                        #                "margin-bottom": "25px",
                        #                "margin-top": "50px",
                        #                'align': 'rigth'}
                        #     ),
                        # ),
                        dbc.Col
                        (
                            html.H1
                            (
                                children='Survey Results',
                                style={"float": "center",
                                       'text-align': 'center',
                                       'color': 'white',
                                    #    'margin-right': '-1px',
                                       'margin-top': '70px',
                                       'font-weight': 'bold'}
                            )
                        ),
                    ]
                )

            ],
            style={
                'height': 'auto',
                'width': 'auto',
                'text-align': 'left',
                'background-color': '#0067b9',
                'align-items': 'center',
                "margin-bottom": "25px",
                "color": "white"},
            id="header",
            className="row flex-display"
        ),

        html.Div(
            [
                html.P(""" """,
                        className="control_label", style={"text-align": "justify"}),
                html.Br(),
                html.P(""" """,
                        className="control_label", style={"text-align": "justify"}), 
                html.Br(),
                html.P(""" """,
                        className="control_label", style={"text-align": "justify"}),
                html.Br(),
                html.P(""" """,
                        className="control_label", style={"text-align": "justify"}),      
                html.Br(),
                html.P(""" """,
                        className="control_label", style={"text-align": "justify"}),             
                html.P("We explored ... \
                        In addition ...",
                       className="control_label", style={"text-align": "justify"}),
                # html.Img(
                #     src=".\\assets\\homeimg.png",
                #     id="homeimg-image",
                #     style={
                #         "float": "right",
                #         "margin-right": "0px",
                #         "height": "-1px",
                #         "width": "auto",
                #         "margin-bottom": "-1px",
                #     },
                # ),
                # html.P("The Team ...",
                #        className="control_label", style={"text-align": "justify"}),
                # html.Img(
                #     src=".\\assets\\logos_black_background.png",
                #     id="logo-image",
                #     style={
                #         "float": "right",
                #         "margin-right": "0px",
                #         "height": "-1px",
                #         "width": "auto",
                #         "margin-bottom": "-1px",
                #     },
                # )
            ],
            className="row pretty_container",
            id="img_container",
        ),
        html.Div([
            html.Div([
                    html.P("Your Overall Score", style={"font-weight": "bold",
                                                        "font-size": "30px",
                                                        "font-family": "Frutiger LT Std-BOLD-lA8cVdsU",
                                                        "position": "relative",
                                                        "flex-direction": "column",
                                                        "align-items": "center"}), 
                html.P([
                    

                    
                    daq.Gauge(
                        color={"gradient":True,"ranges":{"blue":[1,2],"purple":[2,4],"red":[4,5]}},
                        id='our-gauge1',
                        scale={'custom':{5:"Very high",4:"High",3:"Medium",2:"Low",1:"Very low"}},
                        # label='Default',
                        value=4,
                        min=1,
                        max=5,
                        size=400,

                        ),
                        html.P(                        
                            [html.P("Developing Level", className="control_label", style={"font-size": "30px","font-weight": "bold",
                                     "text-align": "center", 
                                      "heigth":"fit-content",
                                      "font-size": "20px",
                                      "position": "relative",
                                      "width": "220px",
                                      "text-align": "center"}),
                            html.P("Your organisation is aware of the opportunities digital technology and modern IT systems can bring, but you need the momentum to push on. Maybe it's stakeholder support you need, or support with change management. Either way, it's time to get to work if you want to create a better employee experience and operate more efficiently.", className="control_label", style={"text-align": "justify", "heigth":"fit-content"})],
                            style = {"text-align": "-webkit-center"}
                            ),

                        
                        ],
                        className="control_label", style={"width": "fit-content",   
                                                          "vertical-align": "top",
                                                          "display": "inline-block",
                                                          "*display": "inline",
                                                          "zoom": "1",
                                                          "display": "grid",
                                                          "grid-template-columns": "1fr 1fr",
                                                          "column-gap": "5px",
                                                          "justify-content": "center",
                                                          "align-items": "baseline",
                                                          "justify-items": "center",},
              
                        ),

        ],className="row pretty_container",  style={"display": "flex",
                                                    #  "border": "2px dashed rgb(68, 68, 68)",
                                                     "height": "fit-content",
                                                     "text-align": "justify",
                                                     "min-width": "400px",
                                                     "align-content": "stretch",
                                                     "flex-wrap": "wrap",
                                                     "justify-content": "space-evenly",
                                                     "align-items": "flex-start"}),
        ],className="row pretty_container"),

        html.Div([
            html.Div([
                html.P(
 [                    html.P(                        
                            html.P("Digital strategy", className="control_label", style={"font-size": "30px","font-weight": "bold"}),
                            
                            ),
                   daq.Gauge(
                        color={"gradient":True,"ranges":{"blue":[1,2],"purple":[2,4],"red":[4,5]}},
                        id="our-gauge1",
                        scale={'custom':{5:"Very high",4:"High",3:"Medium",2:"Low",1:"Very low"}},
                        # label='Default',
                        value=4,
                        min=1,
                        max=5,
                        size=200,

                        ),
                        html.P("A well-defined digital strategy allows businesses to adapt to the ever-changing digital landscape, aligning their business goals with the opportunities and challenges of the digital world.", className="control_label", 
                               style={"text-align": "justify", 
                                      "heigth":"fit-content",
                                      "font-size": "20px",
                                      "position": "relative",
                                      "width": "220px",
                                      "text-align": "center"}),],
                        className="control_label", style={"width": "fit-content",   
                                                          "vertical-align": "top",
                                                          "display": "inline-block",
                                                          "*display": "inline",
                                                          "zoom": "1"},
              
                        ),
                    
                html.P([html.P(                        
                            html.P("Business model", className="control_label", style={"font-size": "30px","font-weight": "bold"}),
                            
                            ),                   daq.Gauge(
                        color={"gradient":True,"ranges":{"blue":[1,2],"purple":[2,4],"red":[4,5]}},
                        id='our-gauge1',
                        scale={'custom':{5:"Very high",4:"High",3:"Medium",2:"Low",1:"Very low"}},
                        # label='Default',
                        value=4,
                        min=1,
                        max=5,
                        size=200,

                        ),
                        html.P("A good business model can help the company identify new growth and expansion opportunities in both existing markets and new markets or segments.", className="control_label", 
                               style={"text-align": "justify", 
                                      "heigth":"fit-content",
                                      "font-size": "20px",
                                      "position": "relative",
                                      "width": "220px",
                                      "text-align": "center"}),],
                        className="control_label", style={"width": "fit-content",   
                                                          "vertical-align": "top",
                                                          "display": "inline-block",
                                                          "*display": "inline",
                                                          "zoom": "1"},
              
                        ),
                html.P([html.P(                        
                            html.P("Enhance customer experience", className="control_label", 
                               style={"font-size": "30px","font-weight": "bold",
                                     "text-align": "justify", 
                                      "heigth":"fit-content",
                                      "font-size": "20px",
                                      "position": "relative",
                                      "width": "220px",
                                      "text-align": "center"}), 
                            ),
                        daq.Gauge(
                        color={"gradient":True,"ranges":{"blue":[1,2],"purple":[2,4],"red":[4,5]}},
                        id='our-gauge1',
                        scale={'custom':{5:"Very high",4:"High",3:"Medium",2:"Low",1:"Very low"}},
                        # label='Default',
                        value=4,
                        min=1,
                        max=5,
                        size=200,

                        ),
                        html.P("Data and analytics can help businesses better understand customer needs and preferences, leading to improved customer experience and increased loyalty.", className="control_label", 
                               style={"text-align": "justify", 
                                      "heigth":"fit-content",
                                      "font-size": "20px",
                                      "position": "relative",
                                      "width": "220px",
                                      "text-align": "center"}),],
                        className="control_label", style={"width": "fit-content",   
                                                          "vertical-align": "top",
                                                          "display": "inline-block",
                                                          "*display": "inline",
                                                          "zoom": "1"},
              
                        ),
                html.P([html.P(                        
                            html.P("Orchestration", className="control_label", style={"font-size": "30px","font-weight": "bold"}),
                            
                            ),
                        daq.Gauge(
                        color={"gradient":True,"ranges":{"blue":[1,2],"purple":[2,4],"red":[4,5]}},
                        id='our-gauge1',
                        scale={'custom':{5:"Very high",4:"High",3:"Medium",2:"Low",1:"Very low"}},
                        # label='Default',
                        value=4,
                        min=1,
                        max=5,
                        size=200,

                        ),
                        html.P("Orchestration allows businesses to automate and coordinate various tasks and processes, increasing efficiency and reducing response times.", className="control_label", 
                               style={"text-align": "justify", 
                                      "heigth":"fit-content",
                                      "font-size": "20px",
                                      "position": "relative",
                                      "width": "220px",
                                      "text-align": "center"}),],
                        className="control_label", style={"width": "fit-content",   
                                                          "vertical-align": "top",
                                                          "display": "inline-block",
                                                          "*display": "inline",
                                                          "zoom": "1"},
              
                        ),

        ],className="row pretty_container",  style={"display": "flex",
                                                    #  "border": "2px dashed rgb(68, 68, 68)",
                                                     "height": "fit-content",
                                                     "text-align": "justify",
                                                     "min-width": "400px",
                                                     "align-content": "stretch",
                                                     "flex-wrap": "wrap",
                                                     "justify-content": "space-evenly",
                                                     "align-items": "flex-start"}),
        ],className="row pretty_container"),

        html.Div(
            [
                html.P("Please visit our following sections such as: ",
                       className="control_label",
                       style={
                           'text-align': 'justify',
                           'font-size': 'large'}),
                html.Label
                ([
                    '* ',
                    html.A
                    (
                        'Page of General Analysis', href='/Analysis'
                    )
                ]),
                html.Label
                ([
                    '* ',
                    html.A
                    (
                        'Page of Model', href='/Model'
                    )
                ]),
            ],
            className="row pretty_container",
        ),
    ]
)
