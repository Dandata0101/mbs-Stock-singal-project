import pandas as pd
import numpy as np
import os

def calculate_profit(df):
    initial_balance = 50000
    cumulative_profit = initial_balance
    position = 0  # Tracks the number of shares owned
    df['profit'] = 0.0
    df['shares_hold'] = 0
    df['cumulative_profit'] = initial_balance  # Renamed balance to cumulative_profit

    for i in range(len(df)):
        if df.loc[i, 'Buy_Signal'] == 1:
            shares_to_buy = cumulative_profit // df.loc[i, 'pricebuy']
            if shares_to_buy > 0:  # Proceed only if we can buy at least one share
                cost = shares_to_buy * df.loc[i, 'pricebuy']
                cumulative_profit -= cost
                position += shares_to_buy
                df.loc[i, 'profit'] = -cost  # Negative because it's a cost
                df.loc[i, 'cumulative_profit'] = cumulative_profit
                print(f"Bought {shares_to_buy} shares at {df.loc[i, 'pricebuy']} on index {i}")

        elif df.loc[i, 'Sell_Signal'] == 1 and position > 0:
            revenue = position * df.loc[i, 'pricesell']
            cumulative_profit += revenue
            print(f"Sold {position} shares at {df.loc[i, 'pricesell']} on index {i}")
            df.loc[i, 'profit'] = revenue
            position = 0  # Reset position after selling
            df.loc[i, 'cumulative_profit'] = cumulative_profit

        # Update shares_hold with current position after each transaction
        df.loc[i, 'shares_hold'] = position

    # If there are any remaining shares, sell them at the last available price
    if position > 0:
        revenue = position * df.iloc[-1]['Close']
        cumulative_profit += revenue
        print(f"Sold remaining {position} shares at {df.iloc[-1]['Close']} on the last index")
        df.iloc[-1, df.columns.get_loc('profit')] = revenue
        df.iloc[-1, df.columns.get_loc('cumulative_profit')] = cumulative_profit
        position = 0  # Reset position
    
    df.fillna(0, inplace=True)
    # Calculate profit for each row
    df['profit'] = df['cumulative_profit'] - initial_balance



    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    else:
        print("Warning: 'Date' column not found. Skipping date formatting.")

    # Save the DataFrame to a CSV file
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, '01-data', 'ml_test_signals_prices_w_profit.csv')
    df.to_csv(file_path, index=False)
    
    return df

# Example usage:
# Assuming you have a DataFrame named 'your_dataframe'
# df_with_profit = calculate_profit(your_dataframe)
# print(df_with_profit)