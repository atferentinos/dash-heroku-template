import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc, html, Dash  
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
markdown_text = '''
## Websites About Gender Wage Gap: 

First Website: 
https://www.aauw.org/issues/equity/pay-gap/

Summary: 
The AAUW article the various examples of what the gender wage gap is, and how it impacts women. Firstly, the article explains that due to the wage gap women have less money for a "rainy day," which means they are less financially equipped to deal with a financial emergency then compared to men of similar education, and career field. Furthermore, the article states that women roughly make 84% of what men make and that there wont be gender pay equality till roughly the year 2088. Additionally, the elaboration on how this pay disparity trickles into other facets of financial security throughout a womans life time: including money set aside for retirement, and amount of student debt women have (women carry more of the debt compared to that of men). 

Second Website: 
https://www.forbes.com/advisor/business/gender-pay-gap-statistics/

Summary: 
The next article I read through was by Forbes which in my opinion is either hit or miss in terms of article intereset and accuracy. However, the article defines the pay gap as the difference in average earnings, rather than straight comparison of annual salaries amongst the sexes which I found to be a simple, but important nuance. Currently, women earn 16% less than men on average, however it does not specifiy if that is for other features: such as education, and career field. Interesting the article also defines the controlled vs the uncontrolled pay gap, which is as I hinted at before controlled being of the same job, and uncontrolled being a different job/career entire of the sexes. So I interpret this as perhaps women are trending towards jobs that inherently pay less than the male counterparts, but the article does not give conclusive hints as that being the sole contributor, as there are quite a few influential factors. 

## What the GSS is: 

GSS Website: http://www.gss.norc.org/About-The-GSS

Summary: GSS stands for The General Social Survey, and has been conducted sine 1972. The GSS collects data on the American society to see trends and important features that society follows. The data contains various feature trends of Americans ranging to ages of 80 years old, the data is collected by in person interviews, along with other statistic research data collection methods (surveys for example). Importantly, from the GSS data one can see the trends of Americans with various relevant factors: such as gender, marital status, and income. For example, these features can be compared with levels of education and location. 
'''
#creating table
display = gss_clean.groupby('sex').agg({
    'income': ['mean'],
    'job_prestige': ['mean'],
    'socioeconomic_index': ['mean'],
    'education': ['mean']
})
#renaming columns to better names 
display.columns = ['Mean Income', 
                 'Mean Occupational Prestige', 
                 'Mean Socioeconomic Index', 
                 'Mean Education (Years)']

#here im rounding the table
display = display.round(2)
table = ff.create_table(display)
#grouping my data
gss_bar = gss_clean.groupby(['sex', 'male_breadwinner']).size()
gss_bar = gss_bar.reset_index()
#renaming to counts
gss_bar = gss_bar.rename({0:'count'}, axis=1)
gss_bargraph = px.bar(gss_bar, x='male_breadwinner', y='count', color='sex',
       labels={'count':'Number of Respondents', 'male_breadwinner':'Male Breadwinner Perspective'})
gss_bargraph.update_layout(height=400, width=600)
fig = px.scatter(gss_clean.head(200), x='job_prestige', y='income', 
                 color = 'sex',
                 trendline='ols',
                 height=600, width=600,
                 labels={'job_prestige':'Job Satisfaction Rating', 
                        'income':'Income'},
                 hover_data=['education', 'socioeconomic_index']
                )
fig_income = px.box(gss_clean, x='sex', y='income', 
                    color='sex',
                    labels={'sex': 'Gender', 'income': 'Income'},)
fig_income.update_layout(showlegend=False,height=400, width=600)
fig_prestige = px.box(gss_clean, x='sex', y='job_prestige', 
                    color='sex',
                    labels={'sex': 'Gender', 'job_prestige': 'Job Prestige Score'},)
fig_prestige.update_layout(showlegend=False,height=400, width=600)
gss_clean['job_prestige'] = gss_clean['job_prestige'].astype('category')
gss_clean['job_prestige_cat'] = pd.cut(gss_clean['job_prestige'],
 bins = [16,26,33,40,47,55,80],
 labels = ('dissatisfied', 
           'a little disastisfied',
           'little satisfied',
           'moderate sastisfied', 
           'very satisfied',
           'completly satisfied'))
#pull the cols
df6 = gss_clean[['income', 'sex', 'job_prestige_cat']]

#drop na
df6 = df6.dropna()
fig6 = px.box(df6, x='sex', y='income', color='sex', facet_col='job_prestige_cat',
             facet_row=None, color_discrete_map={'male':'blue', 'female':'red'}, facet_col_wrap=2)
#updating the sizing from inclass method
fig6.update_layout(
    height=600,  
    width=600,   
)
custom_css = [
    {
        "href": "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/cerulean/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-1BtIRu74gPjT6hGmmF2eGw7TCsfJT0Il8zZu2KB+7rPA9z2PLLojF2kFNYM6pB+7",
        "crossorigin": "anonymous",
    },
    {
        "href": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap",
        "rel": "stylesheet"
    },
    {
        "href": "custom.css",
        "rel": "stylesheet"
    }
]

app = Dash(__name__, external_stylesheets=custom_css)


app.layout = html.Div(
    [
        html.H1("GSS Various Visualizations"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Gender Differences in Socioeconomic Status: Income, Occupational Prestige, Education"),
        
        dcc.Graph(figure=table),
        
        html.H2("Agreement with Male Breadwinner Perspective by Sex"),
        
        dcc.Graph(figure=gss_bargraph),
        
        html.H2("Job Prestige against Income by sex"),
        
        dcc.Graph(figure=fig),
        
        html.Div([
            
            html.H2("Distribution of Income by Sex"),
            
            dcc.Graph(figure=fig_income)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("Distribution of Income by Job Prestige"),
            
            dcc.Graph(figure=fig_prestige)
            
        ], style = {'width':'48%', 'float':'right'}),
        #faceted
        html.H2("Income Distribution by Sex of Job Satisfaction Categories"),
        dcc.Graph(figure=fig6),
    
    ]
)

if __name__ == '__main__':
    app.run_server(mode='inline', debug=True, port=8051)
