import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def plot_stock_signals(df=None, tickerSymbol=None, chart_directory='static/images'):
   
    # Print data types of the dataframe
    print('3.1) load final dataframe')
    print('')
    print('~~~~~~~~~~~~~')
    print(df.dtypes)
    print('~~~~~~~~~~~~~')
    current_directory = os.getcwd()

    # Plotting chart
    plt.figure(figsize=(15, 5))
    plt.plot(df.index, df['Close'].values, label=tickerSymbol)
    plt.plot(df.index, df['pricebuy'].values, color='red', label='Buy signal', marker='^', markersize=12)
    plt.plot(df.index, df['pricesell'].values, color='green', label='Sell signal', marker='v', markersize=12)

    # Setting x-axis ticks
    n = 5  # Adjust n as per your data
    plt.xticks(ticks=df.index[::n], labels=df.index[::n])
    plt.xticks(rotation=-75)

    # Adding legend, labels, and grid
    plt.legend()
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('price USD ($)', fontsize=12)
    plt.grid()

    # Exporting chart image
    chart_path = os.path.join(current_directory, chart_directory, 'chart.png')
    print('')
    print('3.1) export chart image')
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()


def interactive_plot_stock_signals(df=None, tickerSymbol=None):
    # Print data types of the dataframe
    print('3.1) load final dataframe')
    print('')
    print('~~~~~~~~~~~~~')
    print(df.dtypes)
    print('~~~~~~~~~~~~~')
    current_directory = os.getcwd()

    # Initialize a Plotly figure
    fig = go.Figure()

    # Add traces for the stock close prices, buy signals, and sell signals
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=tickerSymbol))
    fig.add_trace(go.Scatter(x=df.index[df['pricebuy'].notnull()], y=df['pricebuy'].dropna(), mode='markers', name='Buy Signal', marker=dict(color='green', size=10, symbol='triangle-up')))
    fig.add_trace(go.Scatter(x=df.index[df['pricesell'].notnull()], y=df['pricesell'].dropna(), mode='markers', name='Sell Signal', marker=dict(color='red', size=10, symbol='triangle-down')))

    # Update layout with width, height, date range slider, and daily interval ticks
    fig.update_layout(title=f"{tickerSymbol} Stock Signals Chart",
                      xaxis_title='Date',
                      yaxis_title='Price USD ($)',
                      xaxis=dict(
                          rangeslider=dict(visible=False),
                          type='date',
                          tickmode='auto',  
                          tickformat='%Y-%m-%d', 
                          tick0=df.index.min(), 
                          dtick=86400000.0 
                      ),
                      width=1400, 
                      height=600) 

    # Show the figure
    return pio.to_html(fig, full_html=False)

def Last_record(df=None):
    # Validate if the input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The input is not a pandas DataFrame.")
    
    # Columns you are interested in
    cols = ['Open', 'High', 'Low', 'Close','Volume']
    
    # Check if all specified columns exist in the DataFrame
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in DataFrame: {', '.join(missing_cols)}")
    
    # Select the last row and filter by the specified columns
    last_record_filtered = df.iloc[-1][cols]
    
    # Format 'Open', 'High', 'Low' as US dollars and 'Volume' with commas
    formatted_last_record = {}
    formatted_last_record['Open'] = "${:,.2f}".format(last_record_filtered['Open'])
    formatted_last_record['High'] = "${:,.2f}".format(last_record_filtered['High'])
    formatted_last_record['Low'] = "${:,.2f}".format(last_record_filtered['Low'])
    formatted_last_record['Close'] = "${:,.2f}".format(last_record_filtered['Close'])
    formatted_last_record['Volume'] = "{:,}".format(int(last_record_filtered['Volume']))
    print(formatted_last_record)
    return formatted_last_record