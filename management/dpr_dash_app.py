from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = DjangoDash("DPRStatisticsApp")

def hrs_from_string(duration):
    try:
        hours, minutes = map(int, duration.split(":"))
        return hours + minutes/60
    except (ValueError, AttributeError):
        return 0

app.layout = html.Div([
    html.Div([
        html.H3("Time Stats"),
        dcc.Dropdown(
            id='time_usage_dropdown',
            options=[
                {'label': 'Time Stats', 'value': 'time_usage'},
            ],
            value='time_usage',
            style={'width': '90%', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '5px', 'padding': '5px'}
        ),
        dcc.Graph(
            id='time_usage',
            config={'displayModeBar': False},
            style={'width': '100%', 'height': '100%'}
        )
    ], style={'width': '47%', 'display': 'inline-block', 'horizontalAlign': 'center', 'verticalAlign': 'top', 'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
], style={'width': '100%', 'maxWidth': '1800px', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#b0b0b0', 'padding': '20px', 'borderRadius': '10px'})

@app.callback(
    [Output('time_usage', 'figure')],
    [Input('time_usage_dropdown', 'value')]
)
def get_data(time_usage_dropdown):
    from .models import DPRs
    dpr = DPRs.objects.all().order_by('-date').first()

    mob = hrs_from_string(dpr.mob_duration_total)
    t   = hrs_from_string(dpr.t_duration_total)
    i   = hrs_from_string(dpr.i_duration_total)
    cs  = hrs_from_string(dpr.cs_duration_total)
    wdt = hrs_from_string(dpr.wdt_duration_total)
    tbw = hrs_from_string(dpr.tbw_duration_total)
    cc  = hrs_from_string(dpr.cc_duration_total)
    tdt = hrs_from_string(dpr.tdt_duration_total)
    
    data = {
        "category": ["Mob and Demob", "Transit Time", "Survey spread", "Client Standby", "Weather DT", "Time Based Work", "Crew Change", "Technical DT"],
        "hours": [mob, t, i, cs, wdt, tbw, cc, tdt]
    }

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=data["category"],
        values=data["hours"],
        text=[f"{int(v)} hrs" for v in data["hours"]],
        textinfo='label+percent+text',
        name="Daily Progress Report Statistics"
    ))

    fig.update_layout(
        margin={'l': 40, 'r': 10, 't': 40, 'b': 40},
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="#4a4a4a"
        )
    )

    return [fig]