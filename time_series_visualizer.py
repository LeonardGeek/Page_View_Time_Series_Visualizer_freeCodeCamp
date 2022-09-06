import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
                 sep=',',
                 index_col='date',
                 parse_dates=True)

# Clean data
df = df.loc[(df['value'] < df['value'].quantile(0.975))
            & (df['value'] > df['value'].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(25, 8))
    ax = plt.axes()
    ax.plot(df, color='#D62728')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = df.index.year
    df_bar['Months'] = df.index.month_name()
    df_bar = df_bar.groupby(['Years', 'Months']).mean()
    df_bar = df_bar.reset_index().rename(columns={'value': 'Average Page Views'})
    MonthsOrder = pd.date_range(start='2022-01', freq='M',
                                periods=12).strftime('%B')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    sns.set_style('whitegrid')
    sns.barplot(x='Years',
                y='Average Page Views',
                data=df_bar,
                hue='Months',
                hue_order=MonthsOrder,
                ax=ax)
    plt.legend(title='Months', loc="upper left")
    plt.xticks(rotation=90)
    plt.xlabel('Years')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(30, 15))

    # Yearly boxplot
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Monthly boxplot
    MonthsOrder = pd.date_range(start='2022-01', freq='M',
                                periods=12).strftime('%b')
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, order=MonthsOrder)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
