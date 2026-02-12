# ----------------------------------------------------------
# stock_chart_simple.py
#
# Simple chart viewer for VOO & JEPI ETFs.
# Lets you select a timeframe and view price charts for both funds.
# Fetches historical price data using yfinance and displays two charts.
# Usage:
#   1. Run: python stock_chart_simple.py
#   2. Choose a timeframe when prompted.
#   3. Charts for VOO and JEPI will be shown.
# Requirements: yfinance, matplotlib (install via pip if needed).
# ----------------------------------------------------------

import yfinance as yf
import matplotlib.pyplot as plt

def get_timeframe():
    print("\n📊 Select Timeframe:")
    print("1. Hourly (Last 5 days)")
    print("2. Daily (Last 1 month)")
    print("3. Daily (Last 3 months)")
    print("4. Weekly (Last 1 year)")
    print("5. Monthly (Last 5 years)")

    choice = input("\nEnter choice (1-5): ")

    timeframes = {
        "1": ("5d", "1h", "Hourly - Last 5 Days"),
        "2": ("1mo", "1d", "Daily - Last 1 Month"),
        "3": ("3mo", "1d", "Daily - Last 3 Months"),
        "4": ("1y", "1wk", "Weekly - Last 1 Year"),
        "5": ("5y", "1mo", "Monthly - Last 5 Years"),
    }

    return timeframes.get(choice, ("1y", "1d", "Daily - Last 1 Year"))

def plot_charts(period, interval, title):
    # Download data
    print(f"\n⏳ Downloading VOO and JEPI data...")
    voo = yf.download("VOO", period=period, interval=interval)
    jepi = yf.download("JEPI", period=period, interval=interval)

    # Create charts
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # VOO Chart
    ax1.plot(voo['Close'], label='VOO', color='blue')
    ax1.set_title(f'VOO - S&P 500 ETF ({title})')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True)

    # JEPI Chart
    ax2.plot(jepi['Close'], label='JEPI', color='green')
    ax2.set_title(f'JEPI - Equity Premium Income ({title})')
    ax2.set_ylabel('Price ($)')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

# Run the program
if __name__ == "__main__":
    print("=" * 40)
    print("   VOO & JEPI Stock Chart Viewer")
    print("=" * 40)

    period, interval, title = get_timeframe()
    plot_charts(period, interval, title)
