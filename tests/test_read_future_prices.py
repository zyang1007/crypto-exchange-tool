import csv
import os

import pandas as pd

from src.service.exchange import Exchange
from src.strategy.grid_strategy import GridStrategy


def read_original_data_and_filter():
    price_file_path = '~/Documents/data_futures_sorted.csv'
    df = pd.read_csv(price_file_path, low_memory=False)  # low_memory=False helps prevent DtypeWarning
    df = df[(df['timestamp'] >= '2024-08-13 16:09:12') & (df['timestamp'] <= '2024-09-21 08:50:12')]

    df.to_csv('~/Documents/data_futures_sorted_filtered.csv', index=False)


def read_prices():
    temp_exchange = Exchange()
    grid_instance = GridStrategy(temp_exchange)

    price_file_path = '/Users/yang/Documents/data_futures_sorted_filtered.csv'
    if not os.path.exists(price_file_path):
        raise FileNotFoundError(f"Target file '{price_file_path}' not found.")
    with open(price_file_path, 'r') as file:
        for i, line in enumerate(file):
            if i != 0:  # first line is the header
                data = line.strip().split(',')  # Strip whitespace and split by comma
                # print(f"date_time: {data[0]} , price: {data[1]}")

                # Convert price to float and handle potential ValueError
                try:
                    date_time = data[0]
                    price = data[1]
                    float_price = float(price)
                    grid_instance.compare_history_prices_and_trade(float_price, date_time)
                    # print(f"price data type: {type(float_price)}: {float_price}")
                except ValueError:
                    print(f"Could not convert price '{price}' to float.")

        print("\n---- Buy Orders----")
        for buy_order in grid_instance.buy_orders:
            print(buy_order)

        print("\n---- Sell Orders----")
        for sell_order in grid_instance.sell_orders:
            print(sell_order)

    # export buy_orders and sell_orders
    buy_orders_file_path = os.path.expanduser('~/Documents/buy_orders.csv')
    sell_orders_file_path = os.path.expanduser('~/Documents/sell_orders.csv')
    export_data(buy_orders_file_path, grid_instance)
    export_data(sell_orders_file_path, grid_instance)

    print("\n\n---- Test Completed----")


def export_data(file_path, grid_instance: GridStrategy):
    # Writing to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        fieldnames = ['side', 'amount', 'price', 'date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Writing headers
        writer.writeheader()

        # Write each dictionary in sell_orders to the CSV file
        for order in grid_instance.sell_orders:
            writer.writerow(order)


if __name__ == '__main__':
    # read_original_data_and_filter()
    read_prices()
