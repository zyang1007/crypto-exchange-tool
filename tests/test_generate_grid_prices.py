def test_generate_grid_prices(start_price, end_price, n):
    """e.g. 2627.06  2645.52  2664.11"""
    grid_prices = [start_price * (end_price / start_price) ** (i / (n - 1)) for i in
                   range(n)]

    # Round each price to 4 decimal places
    grid_prices = [round(price, 4) for price in grid_prices]

    return grid_prices


# Test the function and print the results
if __name__ == "__main__":
    left = 1800
    right = 3600
    num_grids = 100

    grids_v1 = test_generate_grid_prices(left, right, num_grids)

    # Output grid prices
    for i, price in enumerate(grids_v1):
        print(f"Grid {i + 1}: {price:.2f} USD")

    print("--- End of Testing---")
