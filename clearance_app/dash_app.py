import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models import Sum, F, ExpressionWrapper, DurationField, Avg,  Count, Case, When, CharField, Value, Q

from django.utils.translation import gettext_lazy as _

# Initialize the Dash app
app = DjangoDash('StatisticsApp')

# Dataset label mapping
dataset1_labels = {
    'clearance': 'Geräumte Objekte (Gewicht >= 50kg)',
    'clearance_all': 'Geräumte Objekte (alle Gewichte)',

    None: 'Geräumte Objekte',
}

dataset2_labels = {
    'clear': 'Geräumt',
    'todo': 'To Do',
    'uxo': 'UXO',
    'prio': 'Priorität',
    'vessel': 'Schiff',

    None: 'To Do',
}

def get_data_for_graph1(model):
    from .models import MtlItem
    if model == 'clearance':
        model_data = MtlItem.objects.filter(clear='y', model_weight__gte=50).values('cl_date').annotate(count=Count('id')).order_by('cl_date')
        categories = [item['cl_date'] for item in model_data]
        values = [item['count'] for item in model_data]
        yaxis = "Objektanzahl"
    elif model == 'clearance_all':
        model_data = MtlItem.objects.filter(clear='y').values('cl_date').annotate(count=Count('id')).order_by('cl_date')
        categories = [item['cl_date'] for item in model_data]
        values = [item['count'] for item in model_data]
        yaxis = "Objektanzahl"
    else: #model = 'clearance'
        model_data = MtlItem.objects.filter(clear='y', model_weight__gte=50).values('cl_date').annotate(count=Count('id')).order_by('cl_date')
        categories = [item['cl_date'] for item in model_data]
        values = [item['count'] for item in model_data]
        yaxis = "Objektanzahl"

    return {'categories': categories, 'values': values, 'yaxis': yaxis}

def get_data_for_graph2(model):
    from .models import MtlItem
    if model == 'clear':
        items = MtlItem.objects.filter(todo_target='x')
        categories = ['Nicht geräumt(Gewicht >= 50kg)', 'Nicht Geräumt(Gewicht < 50kg)', 'Geräumt(Gewicht >= 50kg)', 'Geräumt(Gewicht < 50kg)', 'In Arbeit']
        values = [0, 0, 0, 0, 0]
        for item in items:
            if item.clear == 'y':
                if item.model_weight >= 50:
                    values[2] += 1
                else:
                    values[3] += 1
            elif item.clear == 'w':
                values[4] += 1
            elif item.clear == 'n' or item.clear == None:
                if item.model_weight >= 50:
                    values[0] += 1
                else:
                    values[1] += 1
    elif model == 'todo':
        items = MtlItem.objects.all()
        categories = ['ToDo (Gewicht >= 50kg)', 'ToDo (Gewicht < 50kg)', 'Nicht zu räumen (Kein ToDo)']
        values = [0, 0, 0]
        for item in items:
            if item.todo_target == 'x' and item.model_weight >= 50:
                values[0] += 1
            elif item.todo_target == 'x' and item.model_weight < 50:
                values[1] += 1
            else:
                values[2] += 1
    elif model == 'uxo':
        items = MtlItem.objects.all()
        categories = ['UXO', 'Nicht UXO', 'Keine Angabe']
        values = [0, 0, 0]
        for item in items:
            if item.uxo == 'x':
                values[0] += 1
            elif item.clear == 'y':
                values[1] += 1
            else:
                values[2] += 1
    elif model == 'prio':
        model_data = (
            MtlItem.objects.all().values('prio')
            .annotate(count=Count('id'))
            .order_by('prio')
        )
        categories = []
        values = []
        for item in model_data:
            classification = item['prio'] if item['prio'] else 'null'
            if classification in categories:
                index = categories.index(classification)
                values[index] += item['count']
            else:
                categories.append(classification)
                values.append(item['count']
        )
    elif model == 'vessel':
        model_data = (
            MtlItem.objects.filter(clear='y').values('vessel')
            .annotate(count=Count('id'))
            .order_by('vessel')
        )
        categories = []
        values = []
        for item in model_data:
            classification = item['vessel'] if item['vessel'] else 'null'
            
            if classification in categories:
                index = categories.index(classification)
                values[index] += item['count']
            else:
                categories.append(classification)
                values.append(item['count'])
    else: #model = 'todo'
        items = MtlItem.objects.all()
        categories = ['x', '']
        values = [0, 0]
        for item in items:
            if item.todo_target == 'x':
                values[0] += 1
            else:
                values[1] += 1
    
    return {'categories': categories, 'values': values}

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2("Statistiken nach Datum", style={'textAlign': 'center', 'color': '#4a4a4a', 'fontFamily': 'Arial, sans-serif'}),
            dcc.Dropdown(
                id='dataset-selector-1',
                options=[
                    {'label': dataset1_labels['clearance'], 'value': 'clearance'},
                    {'label': dataset1_labels['clearance_all'], 'value': 'clearance_all'},
                ],
                value='clearance',
                style={'width': '90%', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '5px', 'padding': '5px'}
            ),
            dcc.Graph(
                id='bar-graph1',
                config={'displayModeBar': False},
                style={'width': '100%', 'height': '400px'}
            )
        ], style={'width': '47%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
        html.Div([
            html.H2("Objekt Statistik", style={'textAlign': 'center', 'color': '#4a4a4a', 'fontFamily': 'Arial, sans-serif'}),
            dcc.Dropdown(
                id='dataset-selector-2',
                options=[
                    {'label': dataset2_labels['clear'], 'value': 'clear'},
                    {'label': dataset2_labels['todo'], 'value': 'todo'},
                    {'label': dataset2_labels['uxo'], 'value': 'uxo'},
                    {'label': dataset2_labels['prio'], 'value': 'prio'},
                    {'label': dataset2_labels['vessel'], 'value': 'vessel'},
                ],
                value='clear',
                style={'width': '90%', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '5px', 'padding': '5px'}
            ),
            dcc.Graph(
                id='pie-chart1',
                config={'displayModeBar': False},
                style={'width': '100%', 'height': '400px'}
            )
        ], style={'width': '47%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'}),
], style={'width': '100%', 'maxWidth': '1800px', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#b0b0b0', 'padding': '20px', 'borderRadius': '10px'})

@app.callback(
    [Output('bar-graph1', 'figure'), Output('pie-chart1', 'figure')],
    [Input('dataset-selector-1', 'value'), Input('dataset-selector-2', 'value')]
)
def update_graphs(selected_dataset1, selected_dataset2):
    data1 = get_data_for_graph1(selected_dataset1)
    label1 = dataset1_labels[selected_dataset1]

    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(
        x=data1['categories'],
        y=data1['values'],
        marker_color='rgb(55, 83, 109)',
        name='Items'
    ))

    bar_fig.update_layout(
        #title=label1,
        xaxis_title="Daten",
        yaxis_title=data1['yaxis'],
        xaxis=dict(
            tickformat='%d.%m',  # Format the x-axis labels to show only the date part
            tickmode='array',       # Make sure that the tickmode is set to 'array'
            tickvals=data1['categories'],  # Use the categories (dates) as tick values
        ),
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

    data2 = get_data_for_graph2(selected_dataset2)
    label2 = dataset2_labels[selected_dataset2]

    pie_fig = go.Figure()
    pie_fig.add_trace(go.Pie(
        labels=data2['categories'],
        values=data2['values'],
        textinfo='label+percent+value',
        marker=dict(colors=['#ff9999','#ffcc99','#99ff99', 'blue', 'yellow']),
    ))

    pie_fig.update_layout(
        #title=label2,
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

    return bar_fig, pie_fig
