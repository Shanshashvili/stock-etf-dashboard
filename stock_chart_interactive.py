# ----------------------------------------------------------
# stock_chart_interactive.py
#
# Interactive chart viewer for VOO & JEPI ETFs.
# Allows you to select a stock (VOO, JEPI, or both) and a timeframe.
# Fetches historical price data using yfinance and displays charts.
# Usage:
#   1. Run: python stock_chart_interactive.py
#   2. Follow prompts to select stock and timeframe.
#   3. Charts will be displayed for your selection.
# Requirements: yfinance, matplotlib (install via pip if needed).
# ----------------------------------------------------------

import yfinance as yf
import matplotlib.pyplot as plt

def show_chart(ticker, period, interval, title):
    data = yf.download(ticker, period=period, interval=interval, progress=False)

    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label=ticker, linewidth=2)
    plt.title(f'{ticker} - {title}')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    timeframes = {
        "1": ("5d", "1h", "Hourly - Last 5 Days"),
        "2": ("1mo", "1d", "Daily - Last 1 Month"),
        "3": ("3mo", "1d", "Daily - Last 3 Months"),
        "4": ("1y", "1wk", "Weekly - Last 1 Year"),
        "5": ("5y", "1mo", "Monthly - Last 5 Years"),
    }

    while True:
        print("\n" + "=" * 40)
        print("   VOO & JEPI Chart Viewer")
        print("=" * 40)
        print("\n📈 Select Stock:")
        print("1. VOO")
        print("2. JEPI")
        print("3. Both (Comparison)")
        print("Q. Quit")

        stock_choice = input("\nStock choice: ").upper()

        if stock_choice == "Q":
            print("Goodbye! 👋")
            break

        print("\n⏰ Select Timeframe:")
        print("1. Hourly (5 days)")
        print("2. Daily (1 month)")
        print("3. Daily (3 months)")
        print("4. Weekly (1 year)")
        print("5. Monthly (5 years)")

        tf_choice = input("\nTimeframe choice: ")

        if tf_choice not in timeframes:
            print("Invalid choice, using default (1 year)")
            tf_choice = "4"

        period, interval, title = timeframes[tf_choice]

        if stock_choice == "1":
            show_chart("VOO", period, interval, title)
        elif stock_choice == "2":
            show_chart("JEPI", period, interval, title)
        elif stock_choice == "3":
            # Comparison chart
            voo = yf.download("VOO", period=period, interval=interval, progress=False)
            jepi = yf.download("JEPI", period=period, interval=interval, progress=False)

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

            ax1.plot(voo['Close'], color='blue', linewidth=2)
            ax1.set_title(f'VOO - {title}')
            ax1.set_ylabel('Price ($)')
            ax1.grid(True, alpha=0.3)

            ax2.plot(jepi['Close'], color='green', linewidth=2)
            ax2.set_title(f'JEPI - {title}')
            ax2.set_ylabel('Price ($)')
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    main()
