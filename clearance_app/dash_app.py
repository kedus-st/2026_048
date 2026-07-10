import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.graph_objs as go
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField, Avg, Case, When, CharField, Value, Q
from django.utils.translation import gettext as _   # gettext, not gettext_lazy — see prior explanation re: Plotly figures

app = DjangoDash('StatisticsApp')

# Stable, language-independent KEYS used for dropdown `value` and callback logic.
# Never translate these — they are identifiers, not display text.
DATASET1_KEYS = ['clearance', 'clearance_all']
DATASET2_KEYS = ['clear', 'todo', 'uxo', 'prio', 'vessel']

def dataset1_label(key):
    return {
        'clearance': _('Geräumte Objekte (Gewicht >= 50kg)'),
        'clearance_all': _('Geräumte Objekte (alle Gewichte)'),
    }.get(key, _('Geräumte Objekte'))

def dataset2_label(key):
    return {
        'clear': _('Geräumt'),
        'todo': _('To Do'),
        'uxo': _('UXO'),
        'prio': _('Priorität'),
        'vessel': _('Schiff'),
    }.get(key, _('To Do'))


def get_data_for_graph1(model):
    from .models import MtlItem
    if model == 'clearance_all':
        qs = MtlItem.objects.filter(clear='y')
    else:  # default / 'clearance'
        qs = MtlItem.objects.filter(clear='y', model_weight__gte=50)
    model_data = qs.values('cl_date').annotate(count=Count('id')).order_by('cl_date')
    categories = [item['cl_date'] for item in model_data]
    values = [item['count'] for item in model_data]
    return {'categories': categories, 'values': values, 'yaxis': _('Objektanzahl')}


def get_data_for_graph2(model):
    from .models import MtlItem
    if model == 'clear':
        items = MtlItem.objects.all()
        categories = [
            _('Nicht geräumt (Gewicht >= 50kg)'),
            _('Nicht geräumt (Gewicht < 50kg)'),
            _('Geräumt (Gewicht >= 50kg)'),
            _('Geräumt (Gewicht < 50kg)'),
            _('In Arbeit'),
        ]
        values = [0, 0, 0, 0, 0]
        for item in items:
            weight = item.model_weight or 0
            if item.clear == 'y':
                values[2 if weight >= 50 else 3] += 1
            elif item.clear == 'w':
                values[4] += 1
            elif item.clear in ('n', None):
                values[0 if weight >= 50 else 1] += 1

    elif model == 'todo':
        items = MtlItem.objects.all()
        categories = [_('ToDo (Gewicht >= 50kg)'), _('ToDo (Gewicht < 50kg)'), _('Nicht zu räumen (kein ToDo)')]
        values = [0, 0, 0]
        for item in items:
            weight = item.model_weight or 0
            if item.todo_target == 'x' and weight >= 50:
                values[0] += 1
            elif item.todo_target == 'x':
                values[1] += 1
            else:
                values[2] += 1

    elif model == 'uxo':
        items = MtlItem.objects.all()
        categories = [_('UXO'), _('Nicht UXO'), _('Keine Angabe')]
        values = [0, 0, 0]
        for item in items:
            if item.uxo == 'x':
                values[0] += 1
            elif item.clear == 'y':
                values[1] += 1
            else:
                values[2] += 1

    elif model == 'prio':
        model_data = MtlItem.objects.all().values('prio').annotate(count=Count('id')).order_by('prio')
        categories, values = [], []
        for item in model_data:
            classification = item['prio'] or _('null')
            if classification in categories:
                values[categories.index(classification)] += item['count']
            else:
                categories.append(classification)
                values.append(item['count'])

    elif model == 'vessel':
        model_data = MtlItem.objects.filter(clear='y').values('vessel').annotate(count=Count('id')).order_by('vessel')
        categories, values = [], []
        for item in model_data:
            classification = item['vessel'] or _('null')
            if classification in categories:
                values[categories.index(classification)] += item['count']
            else:
                categories.append(classification)
                values.append(item['count'])

    else:  # default / 'todo'
        items = MtlItem.objects.all()
        categories = ['x', '']
        values = [0, 0]
        for item in items:
            values[0 if item.todo_target == 'x' else 1] += 1

    return {'categories': categories, 'values': values}


# Layout as a callable, not a static attribute, so gettext() re-resolves
# against the currently-active request language on every page load.
def serve_layout():
    return html.Div([
        html.Div([
            html.Div([
                html.H2(_("Statistiken nach Datum"), style={'textAlign': 'center', 'color': '#4a4a4a', 'fontFamily': 'Arial, sans-serif'}),
                dcc.Dropdown(
                    id='dataset-selector-1',
                    options=[{'label': dataset1_label(k), 'value': k} for k in DATASET1_KEYS],
                    value='clearance',
                    style={'width': '90%', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '5px', 'padding': '5px'}
                ),
                dcc.Graph(id='bar-graph1', config={'displayModeBar': False}, style={'width': '100%', 'height': '400px'})
            ], style={'width': '47%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}),
            html.Div([
                html.H2(_("Objekt Statistik"), style={'textAlign': 'center', 'color': '#4a4a4a', 'fontFamily': 'Arial, sans-serif'}),
                dcc.Dropdown(
                    id='dataset-selector-2',
                    options=[{'label': dataset2_label(k), 'value': k} for k in DATASET2_KEYS],
                    value='clear',
                    style={'width': '90%', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'borderRadius': '5px', 'padding': '5px'}
                ),
                dcc.Graph(id='pie-chart1', config={'displayModeBar': False}, style={'width': '100%', 'height': '400px'})
            ], style={'width': '47%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#f9f9f9', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'})
        ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'}),
    ], style={'width': '100%', 'maxWidth': '1800px', 'margin': '0 auto', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#b0b0b0', 'padding': '20px', 'borderRadius': '10px'})

app.layout = serve_layout


@app.callback(
    [Output('bar-graph1', 'figure'), Output('pie-chart1', 'figure')],
    [Input('dataset-selector-1', 'value'), Input('dataset-selector-2', 'value')]
)
def update_graphs(selected_dataset1, selected_dataset2):
    data1 = get_data_for_graph1(selected_dataset1)

    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=data1['categories'], y=data1['values'], marker_color='rgb(55, 83, 109)', name=_('Objekte')))
    bar_fig.update_layout(
        xaxis_title=_("Daten"),
        yaxis_title=data1['yaxis'],
        xaxis=dict(tickformat='%d.%m', tickmode='array', tickvals=data1['categories']),
        margin={'l': 40, 'r': 10, 't': 40, 'b': 40},
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=14, color="#4a4a4a")
    )

    data2 = get_data_for_graph2(selected_dataset2)

    pie_fig = go.Figure()
    pie_fig.add_trace(go.Pie(
        labels=data2['categories'],
        values=data2['values'],
        textinfo='label+percent+value',
        marker=dict(colors=['#ff9999', '#ffcc99', '#99ff99', 'blue', 'yellow']),
    ))
    pie_fig.update_layout(
        margin={'l': 40, 'r': 10, 't': 40, 'b': 40},
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=14, color="#4a4a4a")
    )

    return bar_fig, pie_fig