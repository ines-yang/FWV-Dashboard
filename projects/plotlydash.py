from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)
raceM = pd.read_csv("raceM.csv")
raceMP = pd.read_csv("raceMP.csv")
raceF = pd.read_csv("raceF.csv")
raceFP = pd.read_csv("raceFP.csv")
race = pd.read_csv("Race.csv")
IPV = pd.read_csv('Sexual_Violence_by_Sex.csv')
age = pd.read_csv('Age.csv')

fig2 = px.bar(raceMP, x="Race/Ethnicity", y="Lifetime Estimated # of Victims")
fig3 = px.bar(raceFP, x="Race/Ethnicity", y="Lifetime Estimated # of Victims", color="Race/Ethnicity")


#fig = go.Figure(data=[fig2, fig3])
# Change the bar mode
#fig.update_layout(barmode='group')
fig4 = px.histogram(age, x="Age", y="Percentage IPV Reported",
             color='Sex', barmode='group')


app.layout = html.Div(children=[
    html.H1(children='NISVS Race /Ethnicity and Sexual Violence Reports'),
        dash_table.DataTable(data=raceF.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'}),
        dcc.Graph(figure = fig3)
]) 

if __name__ == '__main__': 
    app.run_server(debug=True)
