import plotly.express as px
from ipywidgets import interact
import pandas as pd
import numpy as np
import statsmodels.api as sm

def ilinechart(df, x, y, groups=None, title=''):
    fig = px.line(df, x=x, y=y, color=groups, title=title, 
                  template='none').update(layout=dict(title=dict(x=0.5)))

    # for item in range(len(fig.data)):
      # print(fig.data[item])
      # fig.data[item].update(name=fig.data[item]['name'].split('=')[1])
    
    fig.show()
    

def ihistogram(df, field, title=''):
    fig = px.histogram(df, x=field, title=title,
                      template='none').update(layout=dict(title=dict(x=0.5)))
    
    fig.update_yaxes(title_text='Number of Records')
    fig.update_traces(marker_color ='lightskyblue',
                     marker_line_color='black',
                     marker_line_width=1)
    
    fig.show()


def ibarchart(df, x, y, order=None, title=''):
    fig = px.bar(df, x=x, y=y, title=title, template='none')
    
    fig.update_traces(marker_color='lightskyblue',
                     marker_line_color='black',
                     marker_line_width=1)
    fig.update_layout(xaxis={'categoryorder':'array',
                            'categoryarray':order})
    
    fig.show()


def iscatter(df, x, y, color=None, size=None, title=''):
    fig = px.scatter(df, x=x, y=y, color=color, size=size,
                    title=title, template='none')
    
    # for item in range(len(fig.data)):
    #     fig.data[item].update(name=fig.data[item]['name'].split('=')[1])
        
    fig.update_traces(marker_line_color='black',
                     marker_line_width=1)
    
    fig.show()


def linechart(df, x, length=8, width=15, title=""):
    if df.index.name != x:
        df = df.set_index(x)

    ax = df.plot(figsize=(width,length), cmap="Set2")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
              fancybox=True, shadow=True, ncol=4)
    
    plt.title(title + "\n", fontsize=20)


def barchart(df, x, y, groups=None, length=8, width=14, title=""):
    plt.figure(figsize=(width,length))
    sns.barplot(data=df, x=x, y=y, hue=groups)
    plt.title(title + "\n", fontsize=16)


def heatmap(df, length=8, width=18, title=""):
    plt.figure(figsize=(width,length))
    ax = sns.heatmap(df, annot=True, fmt='.1f', 
                     cmap='Reds', linewidths=.01)
    
    plt.title(title + "\n", fontsize=16)
    
    
def update_values(df):
    df = df.drop(columns = ['indv_change_per_day', 'days_btwn_sales', 'indv_pct_change', 'idx_change_per_month', 'idx_change_per_year', 'idx_change_day'])

    df = df.reset_index(drop = True)
    
    df = df.sort_values(by=['Date', 'Parcel'])
  
    df['indv_pct_change'] = (df.groupby('Parcel')['Price'].apply(pd.Series.pct_change))*100

  
    df['days_btwn_sales'] = df.groupby('Parcel')['Date'].apply(pd.Series.diff)

  
    df['days_btwn_sales'] = df['days_btwn_sales'].dt.days

  
    df['indv_change_per_day'] = df['indv_pct_change'] / df['days_btwn_sales']

    idx_change_df = df.groupby(['Date']).agg({'indv_change_per_day' : 'mean'}).reset_index()
    idx_change_df.rename(columns = {'indv_change_per_day' : 'idx_change_day'}, inplace=True)

    change_per_month_df = df.groupby(['Month', 'Year']).agg({'indv_change_per_day' : 'mean'}).reset_index()
    change_per_month_df.rename(columns = {'indv_change_per_day' : 'idx_change_per_month'}, inplace=True)

    change_per_year_df = df.groupby(['Year']).agg({'indv_change_per_day' : 'mean'}).reset_index()
    change_per_year_df.rename(columns= {'indv_change_per_day' : 'idx_change_per_year'}, inplace=True)

    df = pd.merge(df,change_per_month_df, on=['Month','Year'], how = 'left')

    df = pd.merge(df,change_per_year_df, on=['Year'], how = 'left')
    
    df = pd.merge(df,idx_change_df, on=['Date'], how = 'left')
                                                            

    df['Month_Year'] = df['Date'].dt.to_period('M').astype('str')
    return df
    
    
def sqft_index(df):

    df = df.drop(columns = ['idx_sqft_day', 'idx_sqft_month', 'idx_sqft_year'])

    df = df.sort_values(by=['Date', 'Parcel'])

    idx_change_df = df.groupby(['Date']).agg({'price_per_sqft' : 'mean'}).reset_index()
    idx_change_df.rename(columns = {'price_per_sqft' : 'idx_sqft_day'}, inplace=True)

    change_per_month_df = df.groupby(['Month', 'Year']).agg({'price_per_sqft' : 'mean'}).reset_index()
    change_per_month_df.rename(columns = {'price_per_sqft' : 'idx_sqft_month'}, inplace=True)

    change_per_year_df = df.groupby(['Year']).agg({'price_per_sqft' : 'mean'}).reset_index()
    change_per_year_df.rename(columns= {'price_per_sqft' : 'idx_sqft_year'}, inplace=True)

    df = pd.merge(df,change_per_month_df, on=['Month','Year'], how = 'left')

    df = pd.merge(df,change_per_year_df, on=['Year'], how = 'left')
    
    df = pd.merge(df,idx_change_df, on=['Date'], how = 'left')
                                                            
    return df