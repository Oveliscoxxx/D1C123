# libraries
import dash
from dash import html
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import pandas as pd 
import numpy as np
import textwrap

from dash_labs.plugins.pages import register_page

from callbacks import register_callbacks



def customwrap(s,width=100):
    return "<br>".join(textwrap.wrap(s,width=width))

# Function to check if number has decimals (without converting to string)
def has_decimals(num):
    return abs(num - round(num)) > 1e-6  # Tolerance for floating-point precision

# function for average of questions
def promanswer(temp, question):
    testval = temp[temp["variable_1"]==question]
    comp = temp[temp["variable_1"]==question]["variable_0"].unique()[0]
    promvalans = np.sum(testval["value"])/testval.shape[0] 
    num_answers = testval["value"].shape[0]
    return comp, question, promvalans,num_answers

# Topic filter
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




def layout_report(report_id=None,company_id=None, **kwargs):
    global table_placeholder 
    return html.Div([
        dcc.Location(id='current-page', refresh=False),
        html.Div(id='hidden'),
        f"The user requested report ID: {company_id} and {report_id}.",
        html.Div(
            [
            html.Div(
                [
                table_placeholder := html.Div(id="tab-descriptive1")
                ],  # , figure=fig_bar)],
                className="pretty_container twelve columns"),
            ],
            className="row pretty_container",)
    ])



# Dash instance declaration
app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[
        dbc.themes.BOOTSTRAP], update_title='Cargando...',
        suppress_callback_exceptions = True,
)
# app.config.suppress_callback_exceptions = True

register_page("report", path_template="/report/<company_id>/<report_id>",
                   layout=layout_report)
# Top menu, items get from all pages registered with plugin.pages
navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink("Home", href="/")),
    # dbc.NavItem(dbc.NavLink("Report", href="/report")),
    # dbc.NavItem(dbc.NavLink("Model", href="/Model")),
    # dbc.DropdownMenu(
    #     [

    #         dbc.DropdownMenuItem(page["name"], href=page["path"])
    #         for page in dash.page_registry.values()
    #         if page["module"] != "pages.not_found_404"
    #     ],
    #     nav=True,
    #     label="Data Science",
    # ),
    # dbc.NavItem(dbc.NavLink("We are", href="/nosotros")),
],
    brand="Survey results",
    color="primary",
    dark=True,
    className="mb-2",
)

# Main layout
app.layout = dbc.Container(
    [
        # navbar,
        dl.plugins.page_container,
        # html.Footer([html.P("Copyright FSA 2024")])
    ],
    className="dbc",
    fluid=True,
)

# # Call to external function to register all callbacks
# register_callbacks(app)

# # This call will be used with Gunicorn server
# server = app.server

@callback(
[Output("tab-descriptive1", 'children')],
Input('current-page', 'href'),
)

def update_graph(path):
    print(path.split('/')[-1])
    print(path.split('/')[-2])

# Testing server, don't use in production, host
if __name__ == "__main__":
    import os 
    # os.system('start msedge.exe --app=http://127.0.0.1:8000/')
    app.run_server(host='127.0.0.1', port=8000, debug=False)

