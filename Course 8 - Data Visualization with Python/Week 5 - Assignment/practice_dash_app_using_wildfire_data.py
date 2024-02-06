# import libraries required for this project
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt



#create app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
)

# --------------------------------------Explore Data Analysis for Australia wildfire-------------------------------------
 
# lets load the data and create dataframe

df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

#let's convert Date field into datetime and extract year and month from the date field

df["Date"] = pd.to_datetime(df['Date'])
df["Year"] = pd.to_datetime(df['Date']).dt.year
df["Month"] = pd.to_datetime(df['Date']).dt.month_name()

# lets create year object

Year = df.Year.unique()

#create app layout 
app.layout = html.Div( id ="layout_id", children=
    [
        html.Div(    
            html.H1(
                "Dashboard - Australia Wildfire Analysis Since 2005",
                style={
                    "textAlign": 'center',
                    'font-size': 26
                },
            ), style={"padding-top": "40px"}
        ),
        html.Div(
            [
                html.H2(
                    "Select Region:",
                ),
                dcc.RadioItems(
                    [
                        {
                            "label":"North South Wales", 
                            "value": "NSW",
                        },
                        {
                            "label": "Northern Terrority",
                            "value": "NT",
                        },
                        {
                            "label": "Queensland",
                            "value": "QL",
                        },
                        {
                            "label": "South Australia",
                            "value": "SA",
                        },
                        {
                            "label": "Tasmania",
                            "value": "TA",
                        },
                        {
                            "label": "Victoria",
                            "value": "VI",
                        },
                        {
                            "label": "Western Australia",
                            "value": "WA",
                        },
                    ],
                    id="radio-items-id",
                    inline=True,
                    value="NSW",
                ),
            ],
            style={
                "padding-left": "50px",
                "padding-top": '60px'
            },
        ),
        html.Div(
            [
                html.H2(
                    "Select Year:",
                ),
                dcc.Dropdown(
                    Year,
                    id="dropdown-year-id",
                    value=2005,
                ),
            ],
            style={
                "padding-left": "50px",
                "padding-top": '15px',
                "width": '30%'
            },
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id="pie-chart-id",
                        #figure="figure",
                    ),
                ),
                html.Div(
                    dcc.Graph(
                        id="bar-chart-id",
                        #figure="figure",
                    ),
                ),
            ],
            style={
                "padding-left": "50px",
                "padding-top": '50px',
                "display": "flex",
            },
        ),
    ],
)


@app.callback(
    [Output(component_id="pie-chart-id", component_property="figure"),
    Output(component_id="bar-chart-id", component_property="figure"),
    ],
    [Input(component_id="radio-items-id", component_property="value"),
    Input(component_id="dropdown-year-id", component_property="value")
    ]
)

def reg_year_display(input_region,input_year):  
    #data
   region_data = df[df['Region'] == input_region]
   year_region_data = region_data[region_data['Year']==input_year]
   # pie chart  
   est_data = year_region_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
   fig1 = px.pie(est_data, values='Estimated_fire_area', names='Month', title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year))   
   
   #bar chart
   veg_data = year_region_data.groupby('Month')['Count'].mean().reset_index()
   fig2 = px.bar(veg_data, x='Month', y='Count', title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year))    
   return [fig1, fig2]

if __name__ == "__main__":
    app.run_server(debug=True, port = 6605) 
