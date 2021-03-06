from flask import Flask
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from flask_app import FLASK_APP
from password_generation import generatePassword 

DEFAULT_PASSWORD_LENGTH = 15


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "/css/main.css",
]

#  external_scripts = [
    #  "/js/confirm_password.js",
#  ]

meta_tags = [
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    }
]

APP = Dash(__name__, server=FLASK_APP, meta_tags=meta_tags, external_stylesheets=external_stylesheets)

layout = html.Div([
    html.Div(id="background-image"),
    html.Div([
        dbc.Row([
            dbc.Col(
                [],
                sm=0,
                md=2,
                className="buffer",
            ),
            dbc.Col(
                [
                    dcc.Markdown("""
                        # Generate a Password

                        Generate an easy-to-type and readable random password.
                    """),
                    dcc.Markdown("""
                        Security was not taken into consideration in this app so I
                        do not advise using it for sensitive purposes. If you like
                        it, clone it and run the server on a trusted local machine. See
                        [the source](https://github.com/ekoly/passwordgen-dash).
                    """, className="disclaimer"),
                    html.Div([], id="length-indicator"),
                    dcc.Slider(
                        id="password-length",
                        min=5,
                        max=80,
                        step=1,
                        value=DEFAULT_PASSWORD_LENGTH,
                    ),
                    html.Button("Generate Another", id="generate-another"),
                    html.Div([], id="generated-password"),
                    dcc.Input(
                        id="confirm-password",
                        spellCheck=False,
                        autoComplete="off",
                    ),
                    html.Div([], id="confirm-password-indicator"),
                    dcc.Markdown("""
                        ### What does "easy to type" and "easy to read" mean?

                        "Easy to type" means:
                        * Alternating between keys typed by the left hand and right hand
                        * Avoiding keys that require moving the hands too far away from the home row
                        * If the previous letter required the Shift key, the next letter will not use
                        the pinky finger (and vice versa)

                        "Easy to read" simply means avoiding letters that are easily mistaken for other
                        letters, such as 1/l, 0/O, etc.
                    """),
                ],
                sm=12,
                md=6,
                className="main-area",
            ),
            dbc.Col(
                [],
                sm=0,
                md=4,
                className="buffer",
            ),

        ])
    ], id="content")
])

APP.layout = layout

@APP.callback(
    (
        Output("generated-password", "children"),
        Output("length-indicator", "children"),
        Output("confirm-password", "value"),
    ),
    (
        Input("password-length", "value"),
        Input("generate-another", "n_clicks"),
    ),
)
def updateGeneratedPassword(num_letters, *args):
    """
        Update the generated password.
    """
    #print(f"Number of letters selected: {num_letters}")

    indicator_text = f"""
        Select length with the slider: {num_letters}
    """
    current_generated_password = generatePassword(int(num_letters))
    return (
        current_generated_password,
        dcc.Markdown(indicator_text),
        "",
    )

@APP.callback(
    (
        Output("confirm-password-indicator", "children"),
        Output("confirm-password", "className"),
    ),
    (
        Input("confirm-password", "value"),
        Input("generated-password", "children"),
    )
)
def confirmPassword(entered_password, generated_password):
    """
        User practices entering the password.
    """

    #print(f"generated password: {generated_password}")
    #print(f"entered password:   {entered_password}")

    if entered_password == generated_password:
        return (
            dcc.Markdown("correct!"),
            "affirm",
        )
    elif entered_password == "":
        return (
            dcc.Markdown("try typing the password!"),
            "",
        )
    else:
        return (
            dcc.Markdown("wrong!"),
            "scold",
        )


if __name__ == "__main__":
    APP.run_server(debug=True)
