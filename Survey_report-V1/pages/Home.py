from dash.dependencies import Input, Output, State
from shapely.geometry import LineString, MultiLineString
from dash.dependencies import Input, Output

# from dash import Dash, dcc, html, Input, Output, callback
import dash_daq as daq
import dash_svg
import dash_dangerously_set_inner_html

from dash import html, dcc, callback, callback_context,Input, Output, State
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page

import pandas as pd 
import numpy as np



register_page(__name__, path="/")

# from urllib.request import urlopen
################################
# design for mapbox
bgcolor = "#f3f3f1"  # mapbox light map land color
row_heights = [150, 500, 300]
template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}

df = pd.read_csv("data/data.csv", sep=";")
topicdf = np.char.split(df.columns.values.astype("str"), '.')
topicdf = np.array([item[0] for item in topicdf])
df.columns =[[i for i in df.columns],[i for i in df.iloc[0].values.reshape(-1)]]
textdf = df.iloc[1].values.reshape(-1)
df = df.drop([0,1]).reset_index(drop=True)

texttopicdf = pd.DataFrame([topicdf,textdf])
texttopicdf = texttopicdf.T.drop_duplicates(subset=0,keep="first").reset_index(drop=True)

# function for average of questions
def promanswer(temp, question):
    testval = temp[temp["variable_1"]==question]
    testval["value"] = testval["value"].apply(pd.to_numeric)
    comp = temp[temp["variable_1"]==question]["variable_0"].unique()[0]
    promvalans = np.sum(testval["value"])/testval.shape[0] 
    num_answers = testval["value"].shape[0]
    return comp, question, promvalans,num_answers

# Filter topic
def tables_per_topic(temp, topic):
    temp_topic = temp[temp["variable_0"]==topic]
    topic_valcount = temp_topic.groupby("variable_1").value_counts().reset_index()

    # Long format
    prev_topic = topic_valcount.pivot_table('count', ['variable_1', 'variable_0'], 'value').fillna(0).reset_index()
    prev_topic.columns = ["Question", "Topic", "Disagree", "Neither agree or disagree", "Agree"]
    prev_topic["Total Points"] = prev_topic["Disagree"]*1+prev_topic["Neither agree or disagree"]*2+prev_topic["Agree"]*3

    # Get values from questions
    aver_val_question = []
    aver_val = []
    comp_val = []
    num_val = []
    for question in temp_topic["variable_1"].unique():
        comp,quest, aver,num = promanswer(temp, question)
        aver_val.append(aver)
        aver_val_question.append(quest)
        comp_val.append(comp)
        num_val.append(num)
    tesdddf = pd.DataFrame([comp_val,aver_val_question,num_val,aver_val])

    tesdddf = tesdddf.T
    tesdddf.columns = ["Topic","Question", "Total Answers","Average"]

    #final table 
    finaltable = pd.merge(prev_topic, tesdddf, on=["Topic",	"Question"])

    # Total metrics
    metrics_df = pd.DataFrame([temp_topic['value'].value_counts(normalize=False),temp_topic['value'].value_counts(normalize=True) * 100])
    metrics_df.columns = ["Agree","Neither agree or disagree", "Disagree"]

    metrics_df["Total Answers"] = metrics_df["Agree"]+	metrics_df["Neither agree or disagree"]	+ metrics_df["Disagree"]
    metrics_df["Total Points"] = [np.sum(prev_topic["Disagree"]*1+prev_topic["Neither agree or disagree"]*2+prev_topic["Agree"]*3)," "]
    metrics_df["Total Average"] = [np.sum(prev_topic["Disagree"]*1+prev_topic["Neither agree or disagree"]*2+prev_topic["Agree"]*3)
                                /np.sum(prev_topic["Disagree"]+prev_topic["Neither agree or disagree"]+prev_topic["Agree"])," "]
    
    return finaltable,metrics_df

def total_average(temp):
    testval = temp
    testval["value"] = testval["value"].apply(pd.to_numeric)
    promvalans = np.sum(testval["value"])/testval.shape[0] 
    return int(promvalans)

temp= pd.melt(df)
temp.variable_0 = temp.variable_0.str.replace(r'\..', r'', regex=True)
temp.variable_0 = temp.variable_0.str.replace(r' \..', r'', regex=True)
temp.variable_0 = temp.variable_0.str.replace(r' 0', r'', regex=True)
temp.variable_0 = temp.variable_0.str.replace(r'tools ', r'tools', regex=True)
temp.variable_0 = temp.variable_0.str.replace(r'architecture ', r'architecture', regex=True)

testavetotal = total_average(temp)

def svggraph(val):
    transformed = "rotate(" + str(val * (170 / 3) - 56.6) + "deg)"
    return [dash_svg.Svg(
                        xmlns="http://www.w3.org/2000/svg",
                        version="1.1",
                        id="Layer_2_00000110442368763714192000000013104631710973740196_62ff96a196be6",
                        viewBox="0 0 1353.2 744.9",
                        style={
                            "width":"100%",
                            "height":"100%",
                            "display": "block",
                            "transform": "scale(1, 1)",
                            "transitionProperty": "none",
                        },
                        **{"aria-hidden": "true"},
                        children=[
                            dash_svg.Text(x="1160", y="730", fontSize="80", fill="red", children=["HIGH"]),
                            dash_svg.Text(x="0", y="730", fontSize="80", fill="blue", children=["LOW"]),
                            dash_svg.Defs(
                                children=[
                                    dash_svg.LinearGradient(
                                        className="cerosgradient",
                                        **{"data-cerosgradient": "true"},
                                        id="CerosGradient_ida8d2fd22c",
                                        gradientUnits="userSpaceOnUse",
                                        x1="50%",
                                        y1="100%",
                                        x2="50%",
                                        y2="0%",
                                        children=[
                                            dash_svg.Stop(
                                                stopColor="#d1d1d1", style={"transitionProperty": "none"}
                                            ),
                                            dash_svg.Stop(
                                                stopColor="#d1d1d1", style={"transitionProperty": "none"}
                                            ),
                                        ]
                                    ),
                                    dash_svg.LinearGradient(),
                                ]
                            ),
                            dash_svg.G(
                                id="Layer_1-262ff96a196be6",
                                children=[
                                    dash_svg.G(
                                        children=[
                                            dash_svg.Path(
                                                className="st0-62ff96a196be6",
                                                d="M1081.4,398.3c52.3,75.9,83.8,167.2,86.3,265.7h185.4c-2.6-139.2-47.2-268.2-121.7-374.7L1081.4,398.3    L1081.4,398.3z",
                                                style={"transitionProperty": "none"},
                                            ),
                                            dash_svg.Path(
                                                className="st1-62ff96a196be6",
                                                d="M840.5,213.4c90.4,32,168.7,89.7,226,164.3l150-109C1136.4,162.8,1025.8,81.2,897.8,37L840.5,213.4    L840.5,213.4z",
                                                style={"transitionProperty": "none"},
                                            ),
                                            dash_svg.Path(
                                                className="st2-62ff96a196be6",
                                                d="M536.9,205.6c44.3-13.1,91.2-20.2,139.7-20.2s95.4,7.1,139.7,20.2l57.3-176.4C811.3,10.2,745.2,0,676.6,0    s-134.7,10.2-197,29.1L536.9,205.6z",
                                                style={"transitionProperty": "none"},
                                            ),
                                            dash_svg.Path(
                                                className="st3-62ff96a196be6",
                                                d="M286.7,377.7c57.3-74.6,135.6-132.4,226-164.3L455.4,37c-128,44.2-238.6,125.8-318.7,231.7L286.7,377.7    L286.7,377.7z",
                                                style={"transitionProperty": "none"},
                                            ),
                                            dash_svg.Path(
                                                className="st4-62ff96a196be6",
                                                d="M185.4,664c2.5-98.5,34-189.9,86.3-265.7l-150-109C47.2,395.8,2.6,524.8,0,664H185.4z",
                                                style={"transitionProperty": "none"},
                                            ),
                                        ]
                                    ),
                                    dash_svg.Path(
                                        id="pointneedle",
                                        d="M687.9,627.2l-461.7-92.3l424.2,204.3c31.7,15.2,69.5-0.7,80.7-34.1l0.7-2.1   C743,669.6,722.4,634.1,687.9,627.2L687.9,627.2z M715.5,698.6c-7.2,21.4-30.3,32.9-51.6,25.7c-21.4-7.2-32.9-30.3-25.7-51.6   c7.2-21.4,30.3-32.9,51.6-25.7S722.7,677.3,715.5,698.6z",
                                        style={
                                            "transition": "all 0.3s ease-in-out 0s",
                                            "transformOrigin": "730px 650px",
                                            "transform":transformed,
                                        },
                                    ),
                                ],
                            ),
                        ]
                    )]

def textscoreall(val):
    if (val >= 1) and (val < 1.65):
        text = ["low level title","Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Molestie at elementum eu facilisis sed. Nibh sit amet commodo nulla facilisi nullam vehicula ipsum. Quis viverra nibh cras pulvinar mattis nunc sed blandit. At varius vel pharetra vel. Id eu nisl nunc mi ipsum faucibus vitae aliquet. Etiam sit amet nisl purus in. Et netus et malesuada fames ac turpis egestas integer. Pulvinar proin gravida hendrerit lectus. Eget nunc scelerisque viverra mauris in aliquam."]
    elif (val >= 1.65) and (val < 2.3):
        text = ["mid level title","Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Molestie at elementum eu facilisis sed. Nibh sit amet commodo nulla facilisi nullam vehicula ipsum. Quis viverra nibh cras pulvinar mattis nunc sed blandit. At varius vel pharetra vel. Id eu nisl nunc mi ipsum faucibus vitae aliquet. Etiam sit amet nisl purus in. Et netus et malesuada fames ac turpis egestas integer. Pulvinar proin gravida hendrerit lectus. Eget nunc scelerisque viverra mauris in aliquam."]
    elif (val >= 2.3) and (val < 2.3):
        text = ["high level title", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Molestie at elementum eu facilisis sed. Nibh sit amet commodo nulla facilisi nullam vehicula ipsum. Quis viverra nibh cras pulvinar mattis nunc sed blandit. At varius vel pharetra vel. Id eu nisl nunc mi ipsum faucibus vitae aliquet. Etiam sit amet nisl purus in. Et netus et malesuada fames ac turpis egestas integer. Pulvinar proin gravida hendrerit lectus. Eget nunc scelerisque viverra mauris in aliquam."]
    else:
        text = ["[INFO] Error Text","[INFO] Error title"]
    return text

# Generate div elements from the DataFrame
div_elements_topics = []

for _, row in texttopicdf.iterrows():
    cat = row[0]
    text = row[1]
    _, table_2 = tables_per_topic(temp, cat)
    # print(table_2)
    # print(table_2["Total Average"].iloc[0])
    gauge_chart = svggraph(table_2["Total Average"].iloc[0])
    
    div_elements_topics.append(

                html.Div( [ 
                    html.H5(cat, className="control_label", 
                            style={"display": "flex",
                                   "fontWeight": "bold",
                                   "flexDirection": "row",
                                   "flexWrap": "nowrap",
                                   "alignContent": "center",
                                   "justifyContent": "center",
                                   "alignItems": "center",}
                            ),

                    html.P(children=gauge_chart),
                    html.P(text, className="control_label", 
                               style={"textAlign": "justify", 
                                      "heigth":"fit-content",
                                      "fontSize": "20px",
                                      "position": "relative",
                                      "textAlign": "center"}),],
                        className="control_label", style={"width": "fit-content",   
                                                          "verticalAlign": "top",
                                                          "display": "inline-block",
                                                          "*display": "inline",
                                                          "zoom": "1"},
              
                        ),
    )
# Generate div elements from the DataFrame
div_elements_buttons = []

for _, row in texttopicdf.iterrows():
    cat = row[0]
    text = row[1]
    _, table_2 = tables_per_topic(temp, cat)
    button = dbc.Button(cat, id= "id_"+str(cat),color="primary")
    
    div_elements_buttons.append(
        button
    )

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
layout = html.Div([
    dcc.Location(id='current-page', refresh=False),
    html.Div(id='hidden'),
    html.Div([
        html.A(
[            html.Img(
                src=".\\assets\\icon.png",
                style={"width": "5vw"}),
            html.Span(['Survey Results'],
                      style={"float": "center",
                             'textAlign': 'center',
                             'color': 'white',
                             'fontWeight': 'bold',
                             "font-size": "40px", 
                             "text-decoration": "none"},)],style={                "display":"flex",
                'alignItems': 'center',})
            ],style={

                'height': 'auto',
                'width': 'auto',
                'textAlign': 'left',
                'backgroundColor': '#0067b9',

                "marginBottom": "25px",
                "color": "white",
                "align-items": "center"},
            id="header",
            className="row flex-display"
        ),




        html.Div([
            html.Div("Your Overall Score", style={"fontWeight": "bold",
                                    "fontSize": "30px",
                                    "fontFamily": "Frutiger LT Std-BOLD-lA8cVdsU",
                                    "position": "relative",
                                    "flexDirection": "column",
                                    "alignItems": "center"}), 
            html.Div([

                html.Div([
                    html.Div(children=svggraph(testavetotal)),                               
                    

                        html.Div(                        
                            [html.P(textscoreall(testavetotal)[0], className="control_label", style={"fontSize": "30px","fontWeight": "bold",
                                     "textAlign": "center", 
                                      "heigth":"fit-content",
                                      "fontSize": "20px",
                                      "position": "relative",
                                      "width": "220px",
                                      "textAlign": "center"}),
                            html.P(textscoreall(testavetotal)[1], className="control_label", style={"textAlign": "justify", "heigth":"fit-content"})],
                            style = {"textAlign": "-webkit-center","alignItems": "center"}
                            ),

                        
                        ],
                        className="control_label", style={"width": "fit-content",   
                                                          "verticalAlign": "top",
                                                          "display": "inline-block",
                                                          "*display": "inline",
                                                          "zoom": "1",
                                                          "display": "grid",
                                                          "gridTemplateColumns": "1fr 1fr",
                                                          "columnGap": "5px",
                                                          "justifyContent": "center",
                                                          "alignItems": "center",
                                                          "justifyItems": "center",},
              
                        ),

        ],className="row pretty_container",  style={"display": "flex",
                                                    #  "border": "2px dashed rgb(68, 68, 68)",
                                                     "height": "fit-content",
                                                     "textAlign": "justify",
                                                     "minWidth": "400px",
                                                     "alignContent": "stretch",
                                                     "flexWrap": "wrap",
                                                     "justifyContent": "space-evenly",
                                                     "alignItems": "flex-start"}),
        ],className="row pretty_container"),



        html.Div(children=div_elements_topics,className="row pretty_container", 
                 style={"flexFlow": "wrap",
                        "placeContent": "center space-around",
                        "alignItems": "stretch",
                        "flexDirection": "row",
                        "flexWrap": "wrap",
                        "alignContent": "stretch",
                        "justifyContent": "center",}),
        html.Div(
            [
                dbc.Button("Click Here for more details",id="details", color="warning"),
                # dbc.Button("Click Here to save this page",id="printpage", color="primary"),
            ],
            className="d-grid gap-2 d-md-flex",style={"justify-content": "space-between"}
        ),

        html.Div([],id="empty"),
        


    ]
)

# @callback(
# [Output("printpage", 'n_clicks')],
# Input("printpage","n_clicks"),
# Input('current-page', 'href'),
# # prevent_initial_call=True,
# )
# def printpag(nclicks, path):
#     if nclicks == None:
#         return [0]
#     elif nclicks >=1:
#         print(path)
#         import pdfkit
#         path_wkthmltopdf = "./assets/wkhtmltopdf.exe"
#         config = pdfkit.configuration(wkhtmltopdf = path_wkthmltopdf)
#         async def f(path):
#             pdf= await pdfkit.from_url(path, 'report.pdf')
#             return [pdf]
#         pdf = f(path)
#         return [pdf]
    


@callback(
[Output("empty", 'children')],
[Input("details","n_clicks")],
prevent_initial_call=True,
)
def update_details(nclicks):
    if nclicks >=1:
        return [
            html.Div([
            html.Div(children=div_elements_buttons,
                 className="d-grid gap-2 d-md-flex justifyContent-md-begin", 
                 style={"justifyContent": "center"}),
            html.Div([
                
            ],id = "tab",className="row pretty_container",  style={"display": "flex",
                                                    #  "border": "2px dashed rgb(68, 68, 68)",
                                                     "height": "fit-content",
                                                     "textAlign": "justify",
                                                     "minWidth": "400px",
                                                     "alignContent": "stretch",
                                                     "flexWrap": "wrap",
                                                     "justifyContent": "space-evenly",
                                                     "alignItems": "flex-start"}),
        ],className="row pretty_container"),
        
        ]

@callback(
[Output("tab", 'children')],
[Input("id_"+str(i), "n_clicks") for i in texttopicdf[0].values],
prevent_initial_call=True,
)
def update_tab(*args):
    trigger = callback_context.triggered[0]
    print(trigger)
    valtrigger = trigger["value"]
    if valtrigger == None:
        cat = texttopicdf[0].values[0]
        table_1, table_2 = tables_per_topic(temp, str(cat))
    else:
        catid = trigger["prop_id"].split(".")[0]
        cat = catid.split("_")[1]
        print(cat)
        table_1, table_2 = tables_per_topic(temp, str(cat))
    return [html.Div([
            html.H5(cat, className="control_label", 
                            style={"display": "flex",
                                   "fontWeight": "bold",
                                   "flexDirection": "row",
                                   "flexWrap": "nowrap",
                                   "alignContent": "center",
                                   "justifyContent": "center",
                                   "alignItems": "center",}
                            ),
            dbc.Table.from_dataframe(
            table_1.round(2), striped=True, bordered=True, hover=True, index=True,responsive =True),
        dbc.Table.from_dataframe(
            table_2.round(2), striped=True, bordered=True, hover=True, index=True,responsive =True, 
            style={"float": "right",
                   "width": "auto"}),
            ])
        ]

