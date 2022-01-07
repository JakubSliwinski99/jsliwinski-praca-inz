import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

from scripts import facebook_model

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_portal",
                 options=[
                     {"label": "Facebook", "value": 0},
                     {"label": "LinkedIn", "value": 1}],
                 multi=False,
                 value=0,
                 style={'width': "40%"}
                 ),

    html.Br(),

    html.Div([
        dcc.Textarea(
            id='my_txt_input',
            name='text',
            style={'width': '300px', 'height': '200px'}
        ),
    ]),

    html.Br(),

    html.Div(id='output_container', children=[])

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children')],
    [Input(component_id='slct_portal', component_property='value'),
     Input(component_id='my_txt_input', component_property='value')]
)
def update_text(selected_portal, text):
    print(selected_portal)
    print(type(text))

    result = facebook_model.get_reactions_prediction(text)

    return [str(result)]

#     container = "The year chosen by user was: {}".format(option_slctd)
#
#     dff = df.copy()
#     dff = dff[dff["Year"] == option_slctd]
#     dff = dff[dff["Affected by"] == "Varroa_mites"]
#
#     # Plotly Express
#     fig = px.choropleth(
#         data_frame=dff,
#         locationmode='USA-states',
#         locations='state_code',
#         scope="usa",
#         color='Pct of Colonies Impacted',
#         hover_data=['State', 'Pct of Colonies Impacted'],
#         color_continuous_scale=px.colors.sequential.YlOrRd,
#         labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
#         template='plotly_dark'
#     )
#
#     # Plotly Graph Objects (GO)
#     # fig = go.Figure(
#     #     data=[go.Choropleth(
#     #         locationmode='USA-states',
#     #         locations=dff['state_code'],
#     #         z=dff["Pct of Colonies Impacted"].astype(float),
#     #         colorscale='Reds',
#     #     )]
#     # )
#     #
#     # fig.update_layout(
#     #     title_text="Bees Affected by Mites in the USA",
#     #     title_xanchor="center",
#     #     title_font=dict(size=24),
#     #     title_x=0.5,
#     #     geo=dict(scope='usa'),
#     # )
#
#     return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)