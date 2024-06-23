# libraries
import dash
from dash import html
import dash_labs as dl
import dash_bootstrap_components as dbc

from dash_labs.plugins.pages import register_page

from callbacks import register_callbacks

# Dash instance declaration
app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[
        dbc.themes.BOOTSTRAP], update_title='Cargando...'
)
app.config.suppress_callback_exceptions = True

# Accede al servidor Flask subyacente
server = app.server

# Utiliza el decorador before_first_request del servidor Flask
@server.before_first_request
def before_first_request():
    # Aquí tu código que quieres ejecutar antes de la primera solicitud
    print("Esta función se ejecuta antes de la primera solicitud")

register_page("report", path_template="/report/<report_id>",
                   layout=layout_report)
# Top menu, items get from all pages registered with plugin.pages
navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink("Home", href="/")),
    # Continuación de la configuración de tu navbar...
],
    brand="Survey results",
    color="primary",
    dark=True,
    className="mb-2",
)



def layout_report(report_id=None, **kwargs):
    return html.Div(
        f"The user requested report ID: {report_id}."
    )



# Dash instance declaration
app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[
        dbc.themes.BOOTSTRAP], update_title='Cargando...'
)
app.config.suppress_callback_exceptions = True

register_page("report", path_template="/report/<report_id>",
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
        navbar,
        dl.plugins.page_container,

    ],
    className="dbc",
    fluid=True,
)

# Call to external function to register all callbacks
register_callbacks(app)

# This call will be used with Gunicorn server
server = app.server



# Testing server, don't use in production, host
if __name__ == "__main__":
    import os 
    # os.system('start msedge.exe --app=http://127.0.0.1:8000/')
    app.run(host='127.0.0.1', port=8000, debug=True)
