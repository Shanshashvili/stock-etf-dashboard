# ----------------------------------------------------------
# stock_chart_advanced.py
#
# Advanced chart viewer for VOO & JEPI ETFs.
# Allows selection of stock, timeframe, and custom periods.
# Fetches historical price data using yfinance and displays charts.
# Usage:
#   1. Run: python stock_chart_advanced.py
#   2. Follow prompts to select stock, timeframe, and period.
#   3. Charts will be displayed for your selection.
# Requirements: yfinance, matplotlib (install via pip if needed).
# ----------------------------------------------------------

import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_choice():
    """Let user choose which stock(s) to view"""
    print("\n" + "=" * 50)
    print("   📈 STOCK SELECTION")
    print("=" * 50)
    print("\nWhich stock do you want to view?")
    print("-" * 30)
    print("  1. VOO    (S&P 500 ETF)")
    print("  2. JEPI   (JPMorgan Equity Premium Income)")
    print("  3. BOTH   (Compare VOO & JEPI)")
    print("  Q. QUIT   (Exit program)")
    print("-" * 30)
    print("💡 Tip: Enter 1, 2, 3, or Q")

    return input("\n👉 Your choice: ").strip().upper()

def get_period():
    """Let user choose the time period"""
    print("\n" + "=" * 50)
    print("   📅 TIME PERIOD")
    print("=" * 50)
    print("\nHow far back do you want to see?")
    print("-" * 30)
    print("  1. 1 day       (1d)")
    print("  2. 5 days      (5d)")
    print("  3. 1 month     (1mo)")
    print("  4. 3 months    (3mo)")
    print("  5. 6 months    (6mo)")
    print("  6. 1 year      (1y)")
    print("  7. 2 years     (2y)")
    print("  8. 5 years     (5y)")
    print("  9. 10 years    (10y)")
    print("  10. Max        (all available data)")
    print("-" * 30)
    print("💡 Tip: Press ENTER for default (1 year)")
    print("💡 Tip: Or type custom like: 3mo, 2y, 100d")

    choice = input("\n👉 Your choice (1-10 or custom): ").strip()

    period_map = {
        "1": "1d",
        "2": "5d",
        "3": "1mo",
        "4": "3mo",
        "5": "6mo",
        "6": "1y",
        "7": "2y",
        "8": "5y",
        "9": "10y",
        "10": "max",
        "": "1y"  # default
    }

    if choice in period_map:
        return period_map[choice]
    else:
        # User entered custom value like "3mo" or "100d"
        return choice

def get_interval(period):
    """Let user choose the interval (candle size)"""
    print("\n" + "=" * 50)
    print("   ⏰ INTERVAL (Candle/Bar Size)")
    print("=" * 50)
    print("\nHow detailed should each data point be?")
    print("-" * 30)
    print("  1. 1 minute    (1m)   ⚠️  Only works with period ≤ 7 days")
    print("  2. 5 minutes   (5m)   ⚠️  Only works with period ≤ 60 days")
    print("  3. 15 minutes  (15m)  ⚠️  Only works with period ≤ 60 days")
    print("  4. 30 minutes  (30m)  ⚠️  Only works with period ≤ 60 days")
    print("  5. 1 hour      (1h)   ⚠️  Only works with period ≤ 730 days")
    print("  6. 1 day       (1d)   ✅  Works with any period")
    print("  7. 1 week      (1wk)  ✅  Works with any period")
    print("  8. 1 month     (1mo)  ✅  Works with any period")
    print("-" * 30)
    print(f"💡 Your selected period: {period}")
    print("💡 Tip: Press ENTER for auto-select (best for your period)")
    print("💡 Tip: Shorter intervals = more detail but slower loading")

    choice = input("\n👉 Your choice (1-8 or custom): ").strip()

    interval_map = {
        "1": "1m",
        "2": "5m",
        "3": "15m",
        "4": "30m",
        "5": "1h",
        "6": "1d",
        "7": "1wk",
        "8": "1mo",
    }

    if choice == "":
        # Auto-select best interval based on period
        return auto_select_interval(period)
    elif choice in interval_map:
        return interval_map[choice]
    else:
        return choice

def auto_select_interval(period):
    """Automatically pick the best interval for the period"""
    if period in ["1d", "5d"]:
        return "1h"
    elif period in ["1mo", "3mo"]:
        return "1d"
    elif period in ["6mo", "1y", "2y"]:
        return "1d"
    elif period in ["5y", "10y", "max"]:
        return "1wk"
    else:
        # Custom period - try daily
        return "1d"

def get_chart_style():
    """Let user choose the chart appearance"""
    print("\n" + "=" * 50)
    print("   🎨 CHART STYLE")
    print("=" * 50)
    print("\nHow should the chart look?")
    print("-" * 30)
    print("  1. Line Chart      (simple line)")
    print("  2. Area Chart      (filled below line)")
    print("  3. Bar Chart       (vertical bars)")
    print("-" * 30)
    print("💡 Tip: Press ENTER for default (Line Chart)")

    choice = input("\n👉 Your choice (1-3): ").strip()

    style_map = {
        "1": "line",
        "2": "area",
        "3": "bar",
        "": "line"
    }

    return style_map.get(choice, "line")

def show_chart(ticker, period, interval, style):
    """Download data and display chart"""
    print(f"\n⏳ Downloading {ticker} data...")
    print(f"   Period: {period} | Interval: {interval}")

    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False)

        if data.empty:
            print(f"❌ No data found for {ticker}. Check your period/interval combination.")
            return

        plt.figure(figsize=(12, 6))

        if style == "line":
            plt.plot(data['Close'], label=ticker, linewidth=2, color='blue')
        elif style == "area":
            plt.fill_between(data.index, data['Close'].values.flatten(), alpha=0.3, color='blue')
            plt.plot(data['Close'], label=ticker, linewidth=2, color='blue')
        elif style == "bar":
            plt.bar(data.index, data['Close'].values.flatten(), label=ticker, color='blue', alpha=0.7)

        plt.title(f'{ticker} | Period: {period} | Interval: {interval}', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

        # Show summary stats
        print(f"\n📊 {ticker} Summary:")
        print(f"   Latest Price:  ${data['Close'].iloc[-1]:.2f}")
        print(f"   Highest:       ${data['High'].max():.2f}")
        print(f"   Lowest:        ${data['Low'].min():.2f}")
        print(f"   Data Points:   {len(data)}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try a different period/interval combination")

def show_comparison(period, interval, style):
    """Show both VOO and JEPI side by side"""
    print(f"\n⏳ Downloading VOO and JEPI data...")

    try:
        voo = yf.download("VOO", period=period, interval=interval, progress=False)
        jepi = yf.download("JEPI", period=period, interval=interval, progress=False)

        if voo.empty or jepi.empty:
            print("❌ Could not download data. Try different settings.")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f'VOO vs JEPI | Period: {period} | Interval: {interval}', 
                     fontsize=14, fontweight='bold')

        # VOO Chart
        if style == "line":
            ax1.plot(voo['Close'], color='blue', linewidth=2)
        elif style == "area":
            ax1.fill_between(voo.index, voo['Close'].values.flatten(), alpha=0.3, color='blue')
            ax1.plot(voo['Close'], color='blue', linewidth=2)
        elif style == "bar":
            ax1.bar(voo.index, voo['Close'].values.flatten(), color='blue', alpha=0.7)

        ax1.set_title('VOO - S&P 500 ETF')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, alpha=0.3)

        # JEPI Chart
        if style == "line":
            ax2.plot(jepi['Close'], color='green', linewidth=2)
        elif style == "area":
            ax2.fill_between(jepi.index, jepi['Close'].values.flatten(), alpha=0.3, color='green')
            ax2.plot(jepi['Close'], color='green', linewidth=2)
        elif style == "bar":
            ax2.bar(jepi.index, jepi['Close'].values.flatten(), color='green', alpha=0.7)

        ax2.set_title('JEPI - JPMorgan Equity Premium Income')
        ax2.set_ylabel('Price ($)')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        # Show summary
        print(f"\n📊 Summary:")
        print(f"   VOO  - Latest: ${voo['Close'].iloc[-1]:.2f}")
        print(f"   JEPI - Latest: ${jepi['Close'].iloc[-1]:.2f}")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main program loop"""
    print("\n" + "🟦" * 25)
    print("   STOCK CHART VIEWER")
    print("   VOO & JEPI Edition")
    print("🟦" * 25)

    while True:
        # Step 1: Choose stock
        stock_choice = get_stock_choice()

        if stock_choice == "Q":
            print("\n👋 Thanks for using Stock Chart Viewer! Goodbye!\n")
            break

        if stock_choice not in ["1", "2", "3"]:
            print("❌ Invalid choice. Please enter 1, 2, 3, or Q")
            continue

        # Step 2: Choose period
        period = get_period()

        # Step 3: Choose interval
        interval = get_interval(period)

        # Step 4: Choose style
        style = get_chart_style()

        # Step 5: Show confirmation
        print("\n" + "=" * 50)
        print("   ✅ YOUR SETTINGS")
        print("=" * 50)
        stock_name = {"1": "VOO", "2": "JEPI", "3": "VOO & JEPI"}.get(stock_choice)
        print(f"   Stock:    {stock_name}")
        print(f"   Period:   {period}")
        print(f"   Interval: {interval}")
        print(f"   Style:    {style}")
        print("=" * 50)

        confirm = input("\n👉 Proceed? (Y/n): ").strip().lower()

        if confirm in ["", "y", "yes"]:
            if stock_choice == "1":
                show_chart("VOO", period, interval, style)
            elif stock_choice == "2":
                show_chart("JEPI", period, interval, style)
            elif stock_choice == "3":
                show_comparison(period, interval, style)
        else:
            print("↩️  Going back to start...")

if __name__ == "__main__":
    main()
