# ----------------------------------------------------------
# stock_chart_pro.py
#
# Professional Stock Chart Viewer for VOO & JEPI ETFs
# Features:
#   - Multiple chart styles (Line, Area, Bar, Candlestick)
#   - Technical indicators (SMA, EMA, Bollinger Bands)
#   - Dividend tracking
#   - Save charts as images
#   - Dark/Light theme
#   - Price alerts
#   - Portfolio summary
#
# Usage:
#   1. Run: python stock_chart_pro.py
#   2. Follow interactive prompts
#
# Requirements:
#   pip install yfinance matplotlib pandas mplfinance numpy
# ----------------------------------------------------------

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ==================== CONFIGURATION ====================

class Config:
    """Application configuration and themes"""

    THEMES = {
        "dark": {
            "bg_color": "#1a1a2e",
            "text_color": "#ffffff",
            "grid_color": "#333333",
            "up_color": "#00ff88",
            "down_color": "#ff4444",
            "line_color": "#00d4ff",
            "area_color": "#00d4ff",
            "accent_color": "#ff6b6b"
        },
        "light": {
            "bg_color": "#ffffff",
            "text_color": "#333333",
            "grid_color": "#cccccc",
            "up_color": "#26a65b",
            "down_color": "#e74c3c",
            "line_color": "#3498db",
            "area_color": "#3498db",
            "accent_color": "#e74c3c"
        }
    }

    VERSION = "2.0.0"
    APP_NAME = "Stock Chart Pro"

    DEFAULT_THEME = "dark"
    DEFAULT_PERIOD = "1y"
    DEFAULT_INTERVAL = "1d"
    DEFAULT_STYLE = "line"


# ==================== UTILITY FUNCTIONS ====================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + f"   📈 {Config.APP_NAME} v{Config.VERSION}".ljust(58) + "║")
    print("║" + "   Professional Stock Analysis Tool".ljust(58) + "║")
    print("║" + "   VOO & JEPI Edition".ljust(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")

def print_section(title, icon="📊"):
    """Print a section header"""
    print("\n" + "┌" + "─" * 56 + "┐")
    print(f"│  {icon} {title.upper()}" + " " * (53 - len(title)) + "│")
    print("└" + "─" * 56 + "┘")

def print_menu_item(key, label, description="", selected=False):
    """Print a formatted menu item"""
    prefix = "  ▸ " if selected else "    "
    if description:
        print(f"{prefix}{key}. {label:<20} ({description})")
    else:
        print(f"{prefix}{key}. {label}")

def print_divider():
    """Print a divider line"""
    print("  " + "─" * 50)

def print_tip(message):
    """Print a tip message"""
    print(f"\n  💡 Tip: {message}")

def print_error(message):
    """Print an error message"""
    print(f"\n  ❌ Error: {message}")

def print_success(message):
    """Print a success message"""
    print(f"\n  ✅ {message}")

def print_loading(message):
    """Print a loading message"""
    print(f"\n  ⏳ {message}")


# ==================== DATA FUNCTIONS ====================

def fix_dataframe_columns(df):
    """
    Fix yfinance multi-level column issue.
    Converts MultiIndex columns to simple column names.
    """
    if df is None or df.empty:
        return df

    # If columns are MultiIndex, flatten them
    if isinstance(df.columns, pd.MultiIndex):
        # Get the first level (Price type: Open, High, Low, Close, Volume)
        df.columns = df.columns.get_level_values(0)

    # Ensure we have the standard column names
    expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']

    # Check if all expected columns exist
    for col in expected_cols:
        if col not in df.columns:
            # Try to find similar column names (case-insensitive)
            for existing_col in df.columns:
                if existing_col.lower() == col.lower():
                    df = df.rename(columns={existing_col: col})
                    break

    return df

def download_stock_data(ticker, period, interval):
    """Download stock data with error handling and column fixing"""
    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False)
        if data.empty:
            return None, "No data available for this combination"

        # Fix the column structure
        data = fix_dataframe_columns(data)

        return data, None
    except Exception as e:
        return None, str(e)

def get_stock_info(ticker):
    """Get detailed stock information"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "name": info.get("longName", ticker),
            "price": info.get("regularMarketPrice", 0),
            "change": info.get("regularMarketChange", 0),
            "change_percent": info.get("regularMarketChangePercent", 0),
            "volume": info.get("regularMarketVolume", 0),
            "market_cap": info.get("marketCap", 0),
            "52w_high": info.get("fiftyTwoWeekHigh", 0),
            "52w_low": info.get("fiftyTwoWeekLow", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "pe_ratio": info.get("trailingPE", 0),
        }
    except:
        return None

def get_dividends(ticker, period="1y"):
    """Get dividend history"""
    try:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends
        if not dividends.empty:
            end_date = datetime.now()
            if period == "1y":
                start_date = end_date - timedelta(days=365)
            elif period == "2y":
                start_date = end_date - timedelta(days=730)
            elif period == "5y":
                start_date = end_date - timedelta(days=1825)
            else:
                start_date = end_date - timedelta(days=365)

            # Make start_date timezone-aware if dividends index is timezone-aware
            if dividends.index.tz is not None:
                start_date = pd.Timestamp(start_date).tz_localize(dividends.index.tz)

            dividends = dividends[dividends.index >= start_date]
        return dividends
    except:
        return pd.Series()


# ==================== TECHNICAL INDICATORS ====================

def calculate_sma(data, window):
    """Calculate Simple Moving Average"""
    close = data['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close.rolling(window=window).mean()

def calculate_ema(data, window):
    """Calculate Exponential Moving Average"""
    close = data['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close.ewm(span=window, adjust=False).mean()

def calculate_bollinger_bands(data, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = calculate_sma(data, window)
    close = data['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    std = close.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band

def calculate_rsi(data, window=14):
    """Calculate Relative Strength Index"""
    close = data['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    close = data['Close']
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


# ==================== HELPER FUNCTIONS FOR PLOTTING ====================

def get_column_values(data, column_name):
    """
    Safely extract column values from DataFrame.
    Handles both regular and MultiIndex columns.
    """
    col = data[column_name]
    if isinstance(col, pd.DataFrame):
        return col.iloc[:, 0].values.flatten()
    elif isinstance(col, pd.Series):
        return col.values.flatten()
    else:
        return np.array(col).flatten()

def get_scalar_value(value):
    """Convert any value to a Python scalar"""
    if hasattr(value, 'item'):
        return value.item()
    elif isinstance(value, (pd.Series, pd.DataFrame)):
        return float(value.iloc[0])
    elif isinstance(value, np.ndarray):
        return float(value.flatten()[0])
    else:
        return float(value)


# ==================== CHART FUNCTIONS ====================

def apply_theme(fig, ax, theme_name):
    """Apply theme to matplotlib figure"""
    theme = Config.THEMES.get(theme_name, Config.THEMES["dark"])

    fig.patch.set_facecolor(theme["bg_color"])
    ax.set_facecolor(theme["bg_color"])
    ax.tick_params(colors=theme["text_color"])
    ax.xaxis.label.set_color(theme["text_color"])
    ax.yaxis.label.set_color(theme["text_color"])
    ax.title.set_color(theme["text_color"])
    ax.spines['bottom'].set_color(theme["grid_color"])
    ax.spines['top'].set_color(theme["grid_color"])
    ax.spines['left'].set_color(theme["grid_color"])
    ax.spines['right'].set_color(theme["grid_color"])
    ax.grid(True, alpha=0.3, color=theme["grid_color"])

    return theme

def plot_line_chart(ax, data, theme, label="Price"):
    """Plot line chart"""
    close_values = get_column_values(data, 'Close')
    ax.plot(data.index, close_values,
            color=theme["line_color"],
            linewidth=2,
            label=label)

def plot_area_chart(ax, data, theme, label="Price"):
    """Plot area chart"""
    close_values = get_column_values(data, 'Close')
    ax.fill_between(data.index, close_values,
                    alpha=0.3,
                    color=theme["area_color"])
    ax.plot(data.index, close_values,
            color=theme["line_color"],
            linewidth=2,
            label=label)

def plot_bar_chart(ax, data, theme, label="Price"):
    """Plot bar chart"""
    close_values = get_column_values(data, 'Close')
    open_values = get_column_values(data, 'Open')

    colors = [theme["up_color"] if close_values[i] >= open_values[i]
              else theme["down_color"] for i in range(len(data))]
    ax.bar(data.index, close_values,
           color=colors,
           alpha=0.7,
           label=label)

def plot_candlestick(ax, data, theme):
    """Plot candlestick chart"""
    # Get values as flat arrays
    open_vals = get_column_values(data, 'Open')
    high_vals = get_column_values(data, 'High')
    low_vals = get_column_values(data, 'Low')
    close_vals = get_column_values(data, 'Close')

    # Determine candle width based on data frequency
    if len(data) > 1:
        time_diff = (data.index[1] - data.index[0]).total_seconds()
        if time_diff < 3600:  # Less than 1 hour
            width = timedelta(minutes=1)
        elif time_diff < 86400:  # Less than 1 day
            width = timedelta(hours=0.5)
        elif time_diff < 604800:  # Less than 1 week
            width = timedelta(days=0.6)
        else:
            width = timedelta(days=4)
    else:
        width = timedelta(days=0.6)

    width2 = width / 5

    for i in range(len(data)):
        if close_vals[i] >= open_vals[i]:
            color = theme["up_color"]
            body_bottom = open_vals[i]
            body_height = close_vals[i] - open_vals[i]
        else:
            color = theme["down_color"]
            body_bottom = close_vals[i]
            body_height = open_vals[i] - close_vals[i]

        # Draw body
        ax.bar(data.index[i], body_height, width, bottom=body_bottom,
               color=color, edgecolor=color)

        # Draw upper wick
        ax.bar(data.index[i], high_vals[i] - max(open_vals[i], close_vals[i]),
               width2, bottom=max(open_vals[i], close_vals[i]), color=color)

        # Draw lower wick
        ax.bar(data.index[i], min(open_vals[i], close_vals[i]) - low_vals[i],
               width2, bottom=low_vals[i], color=color)

def add_indicators(ax, data, indicators, theme):
    """Add technical indicators to chart"""
    colors = ['#ff9f43', '#ee5a24', '#5f27cd', '#10ac84']
    color_idx = 0

    for indicator in indicators:
        if indicator == "sma20":
            sma = calculate_sma(data, 20)
            ax.plot(data.index, sma.values.flatten(), color=colors[color_idx % len(colors)],
                    linewidth=1.5, label='SMA 20', linestyle='--')
            color_idx += 1
        elif indicator == "sma50":
            sma = calculate_sma(data, 50)
            ax.plot(data.index, sma.values.flatten(), color=colors[color_idx % len(colors)],
                    linewidth=1.5, label='SMA 50', linestyle='--')
            color_idx += 1
        elif indicator == "ema20":
            ema = calculate_ema(data, 20)
            ax.plot(data.index, ema.values.flatten(), color=colors[color_idx % len(colors)],
                    linewidth=1.5, label='EMA 20', linestyle='-.')
            color_idx += 1
        elif indicator == "bb":
            upper, middle, lower = calculate_bollinger_bands(data)
            ax.plot(data.index, upper.values.flatten(), color=theme["accent_color"],
                    linewidth=1, label='BB Upper', linestyle=':')
            ax.plot(data.index, lower.values.flatten(), color=theme["accent_color"],
                    linewidth=1, label='BB Lower', linestyle=':')
            ax.fill_between(data.index, upper.values.flatten(), lower.values.flatten(),
                           alpha=0.1, color=theme["accent_color"])


# ==================== MAIN CHART DISPLAY ====================

def show_professional_chart(ticker, period, interval, style, theme_name,
                           indicators=None, show_volume=True, save_path=None):
    """Display professional chart with all features"""

    print_loading(f"Downloading {ticker} data...")
    data, error = download_stock_data(ticker, period, interval)

    if error:
        print_error(error)
        return

    # Get stock info
    info = get_stock_info(ticker)

    # Setup figure
    if show_volume:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10),
                                        gridspec_kw={'height_ratios': [3, 1]})
    else:
        fig, ax1 = plt.subplots(figsize=(14, 8))

    # Apply theme
    theme = apply_theme(fig, ax1, theme_name)
    if show_volume:
        apply_theme(fig, ax2, theme_name)

    # Plot main chart based on style
    if style == "line":
        plot_line_chart(ax1, data, theme, ticker)
    elif style == "area":
        plot_area_chart(ax1, data, theme, ticker)
    elif style == "bar":
        plot_bar_chart(ax1, data, theme, ticker)
    elif style == "candlestick":
        plot_candlestick(ax1, data, theme)

    # Add indicators
    if indicators:
        add_indicators(ax1, data, indicators, theme)

    # Title and labels
    title = f"{ticker}"
    if info and info.get("price"):
        price_change = "+" if info["change"] >= 0 else ""
        title += f" | ${info['price']:.2f} ({price_change}{info['change']:.2f}, {price_change}{info['change_percent']:.2f}%)"
    title += f" | {period.upper()} | {interval}"

    ax1.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax1.set_ylabel('Price ($)', fontsize=11)
    ax1.legend(loc='upper left', framealpha=0.9)

    # Format x-axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Volume subplot
    if show_volume:
        close_values = get_column_values(data, 'Close')
        open_values = get_column_values(data, 'Open')
        volume_values = get_column_values(data, 'Volume')

        colors = [theme["up_color"] if close_values[i] >= open_values[i]
                  else theme["down_color"] for i in range(len(data))]
        ax2.bar(data.index, volume_values, color=colors, alpha=0.7)
        ax2.set_ylabel('Volume', fontsize=11)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight',
                    facecolor=theme["bg_color"])
        print_success(f"Chart saved to: {save_path}")

    plt.show()

    # Print summary
    print_summary(ticker, data, info)

def show_comparison_chart(period, interval, style, theme_name,
                         indicators=None, save_path=None):
    """Show VOO vs JEPI comparison chart"""

    print_loading("Downloading VOO and JEPI data...")

    voo_data, voo_error = download_stock_data("VOO", period, interval)
    jepi_data, jepi_error = download_stock_data("JEPI", period, interval)

    if voo_error or jepi_error:
        print_error("Could not download data")
        return

    # Setup figure
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    theme = apply_theme(fig, ax1, theme_name)
    apply_theme(fig, ax2, theme_name)
    apply_theme(fig, ax3, theme_name)
    apply_theme(fig, ax4, theme_name)

    # VOO Price
    if style == "candlestick":
        plot_candlestick(ax1, voo_data, theme)
    else:
        plot_line_chart(ax1, voo_data, theme, "VOO")
    if indicators:
        add_indicators(ax1, voo_data, indicators, theme)
    ax1.set_title('VOO - S&P 500 ETF', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.legend(loc='upper left')

    # JEPI Price
    theme_jepi = theme.copy()
    theme_jepi["line_color"] = "#00ff88"
    if style == "candlestick":
        plot_candlestick(ax2, jepi_data, theme)
    else:
        plot_line_chart(ax2, jepi_data, theme_jepi, "JEPI")
    if indicators:
        add_indicators(ax2, jepi_data, indicators, theme)
    ax2.set_title('JEPI - JPMorgan Equity Premium Income', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Price ($)')
    ax2.legend(loc='upper left')

    # Normalized comparison
    voo_close = get_column_values(voo_data, 'Close')
    jepi_close = get_column_values(jepi_data, 'Close')

    voo_norm = (voo_close / voo_close[0] - 1) * 100
    jepi_norm = (jepi_close / jepi_close[0] - 1) * 100

    ax3.plot(voo_data.index, voo_norm, color=theme["line_color"],
             linewidth=2, label='VOO')
    ax3.plot(jepi_data.index, jepi_norm, color='#00ff88',
             linewidth=2, label='JEPI')
    ax3.axhline(y=0, color=theme["grid_color"], linestyle='--', alpha=0.5)
    ax3.set_title('Performance Comparison (%)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Return (%)')
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)

    # Volume comparison
    voo_volume = get_column_values(voo_data, 'Volume')
    jepi_volume = get_column_values(jepi_data, 'Volume')

    ax4.bar(voo_data.index, voo_volume, alpha=0.5,
            label='VOO Volume', color=theme["line_color"])
    ax4.bar(jepi_data.index, jepi_volume, alpha=0.5,
            label='JEPI Volume', color='#00ff88')
    ax4.set_title('Volume Comparison', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Volume')
    ax4.legend(loc='upper left')

    # Format dates
    for ax in [ax1, ax2, ax3, ax4]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    fig.suptitle(f'VOO vs JEPI Comparison | {period.upper()} | {interval}',
                 fontsize=14, fontweight='bold', color=theme["text_color"])

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight',
                    facecolor=theme["bg_color"])
        print_success(f"Chart saved to: {save_path}")

    plt.show()

    # Print comparison summary
    print_comparison_summary(voo_data, jepi_data)

def print_summary(ticker, data, info):
    """Print detailed summary statistics"""
    print_section("SUMMARY", "📊")

    print(f"\n  {'─' * 40}")
    print(f"  │ {'Metric':<20} │ {'Value':>15} │")
    print(f"  {'─' * 40}")

    close_values = get_column_values(data, 'Close')
    high_values = get_column_values(data, 'High')
    low_values = get_column_values(data, 'Low')

    latest = close_values[-1]
    print(f"  │ {'Latest Price':<20} │ ${latest:>14.2f} │")

    high = np.max(high_values)
    print(f"  │ {'Period High':<20} │ ${high:>14.2f} │")

    low = np.min(low_values)
    print(f"  │ {'Period Low':<20} │ ${low:>14.2f} │")

    first_price = close_values[0]
    returns = ((latest - first_price) / first_price) * 100

    print(f"  │ {'Period Return':<20} │ {returns:>14.2f}% │")
    print(f"  │ {'Data Points':<20} │ {len(data):>15} │")

    if info:
        if info.get('dividend_yield'):
            div_yield = info['dividend_yield'] * 100
            print(f"  │ {'Dividend Yield':<20} │ {div_yield:>14.2f}% │")
        if info.get('pe_ratio'):
            print(f"  │ {'P/E Ratio':<20} │ {info['pe_ratio']:>15.2f} │")

    print(f"  {'─' * 40}")

def print_comparison_summary(voo_data, jepi_data):
    """Print comparison summary for VOO vs JEPI"""
    print_section("COMPARISON SUMMARY", "📈")

    voo_close = get_column_values(voo_data, 'Close')
    jepi_close = get_column_values(jepi_data, 'Close')

    voo_return = ((voo_close[-1] - voo_close[0]) / voo_close[0]) * 100
    jepi_return = ((jepi_close[-1] - jepi_close[0]) / jepi_close[0]) * 100

    print(f"\n  {'─' * 50}")
    print(f"  │ {'Metric':<20} │ {'VOO':>12} │ {'JEPI':>12} │")
    print(f"  {'─' * 50}")

    print(f"  │ {'Latest Price':<20} │ ${voo_close[-1]:>11.2f} │ ${jepi_close[-1]:>11.2f} │")
    print(f"  │ {'Period Return':<20} │ {voo_return:>11.2f}% │ {jepi_return:>11.2f}% │")
    print(f"  {'─' * 50}")

    if voo_return > jepi_return:
        print(f"\n  🏆 VOO outperformed JEPI by {voo_return - jepi_return:.2f}%")
    else:
        print(f"\n  🏆 JEPI outperformed VOO by {jepi_return - voo_return:.2f}%")


# ==================== MENU FUNCTIONS ====================

def get_stock_choice():
    """Let user choose which stock(s) to view"""
    print_section("STOCK SELECTION", "📈")

    print("\n  Which stock do you want to analyze?\n")
    print_menu_item("1", "VOO", "S&P 500 ETF - Tracks the S&P 500 index")
    print_menu_item("2", "JEPI", "JPMorgan Equity Premium Income ETF")
    print_menu_item("3", "COMPARE", "Side-by-side VOO vs JEPI analysis")
    print_divider()
    print_menu_item("S", "SETTINGS", "Change theme, save preferences")
    print_menu_item("Q", "QUIT", "Exit application")

    print_tip("Enter 1, 2, 3, S, or Q")

    return input("\n  👉 Your choice: ").strip().upper()

def get_period():
    """Let user choose the time period"""
    print_section("TIME PERIOD", "📅")

    print("\n  How far back do you want to analyze?\n")

    print("  Short Term:")
    print_menu_item("1", "1 Day", "Intraday movements")
    print_menu_item("2", "5 Days", "Trading week")
    print_menu_item("3", "1 Month", "Recent performance")

    print("\n  Medium Term:")
    print_menu_item("4", "3 Months", "Quarterly view")
    print_menu_item("5", "6 Months", "Half-year trend")
    print_menu_item("6", "1 Year", "Annual performance")

    print("\n  Long Term:")
    print_menu_item("7", "2 Years", "Medium-term trend")
    print_menu_item("8", "5 Years", "Long-term growth")
    print_menu_item("9", "10 Years", "Historical perspective")
    print_menu_item("10", "Max", "All available data")

    print_divider()
    print_tip("Press ENTER for default (1 year)")
    print_tip("Or type custom period: 3mo, 2y, 100d")

    choice = input("\n  👉 Your choice (1-10 or custom): ").strip()

    period_map = {
        "1": "1d", "2": "5d", "3": "1mo", "4": "3mo", "5": "6mo",
        "6": "1y", "7": "2y", "8": "5y", "9": "10y", "10": "max",
        "": "1y"
    }

    return period_map.get(choice, choice)

def get_interval(period):
    """Let user choose the interval"""
    print_section("DATA INTERVAL", "⏰")

    print("\n  How granular should the data be?\n")

    print("  High Frequency (requires shorter periods):")
    print_menu_item("1", "1 Minute", "⚠️ Max 7 days")
    print_menu_item("2", "5 Minutes", "⚠️ Max 60 days")
    print_menu_item("3", "15 Minutes", "⚠️ Max 60 days")
    print_menu_item("4", "1 Hour", "⚠️ Max 730 days")

    print("\n  Standard:")
    print_menu_item("5", "1 Day", "✅ Most common, works with any period")
    print_menu_item("6", "1 Week", "✅ Good for long-term trends")
    print_menu_item("7", "1 Month", "✅ Best for multi-year analysis")

    print_divider()
    print(f"  📌 Your selected period: {period}")
    print_tip("Press ENTER for auto-select (recommended)")

    choice = input("\n  👉 Your choice (1-7): ").strip()

    interval_map = {
        "1": "1m", "2": "5m", "3": "15m", "4": "1h",
        "5": "1d", "6": "1wk", "7": "1mo"
    }

    if choice == "":
        return auto_select_interval(period)

    return interval_map.get(choice, "1d")

def auto_select_interval(period):
    """Auto-select best interval for period"""
    if period in ["1d"]:
        return "5m"
    elif period in ["5d"]:
        return "1h"
    elif period in ["1mo", "3mo"]:
        return "1d"
    elif period in ["6mo", "1y", "2y"]:
        return "1d"
    else:
        return "1wk"

def get_chart_style():
    """Let user choose the chart style"""
    print_section("CHART STYLE", "🎨")

    print("\n  How should the chart be displayed?\n")
    print_menu_item("1", "Line Chart", "Clean, simple trend line")
    print_menu_item("2", "Area Chart", "Filled area under the line")
    print_menu_item("3", "Bar Chart", "Vertical bars for each period")
    print_menu_item("4", "Candlestick", "Professional trading view (OHLC)")

    print_divider()
    print_tip("Candlestick shows Open, High, Low, Close prices")
    print_tip("Press ENTER for default (Line Chart)")

    choice = input("\n  👉 Your choice (1-4): ").strip()

    style_map = {"1": "line", "2": "area", "3": "bar", "4": "candlestick", "": "line"}
    return style_map.get(choice, "line")

def get_indicators():
    """Let user choose technical indicators"""
    print_section("TECHNICAL INDICATORS", "📐")

    print("\n  Add technical analysis overlays?\n")
    print_menu_item("1", "SMA 20", "20-day Simple Moving Average")
    print_menu_item("2", "SMA 50", "50-day Simple Moving Average")
    print_menu_item("3", "EMA 20", "20-day Exponential Moving Average")
    print_menu_item("4", "Bollinger Bands", "Volatility bands (20-day)")
    print_menu_item("5", "All Above", "Add all indicators")
    print_menu_item("0", "None", "No indicators (clean chart)")

    print_divider()
    print_tip("Enter multiple numbers separated by comma: 1,2,4")
    print_tip("Press ENTER to skip (no indicators)")

    choice = input("\n  👉 Your choice: ").strip()

    if choice == "" or choice == "0":
        return []

    indicator_map = {
        "1": "sma20", "2": "sma50", "3": "ema20", "4": "bb"
    }

    if choice == "5":
        return ["sma20", "sma50", "ema20", "bb"]

    indicators = []
    for c in choice.split(","):
        c = c.strip()
        if c in indicator_map:
            indicators.append(indicator_map[c])

    return indicators

def get_theme():
    """Let user choose color theme"""
    print_section("COLOR THEME", "🌓")

    print("\n  Choose your preferred theme:\n")
    print_menu_item("1", "Dark Mode", "Easy on the eyes, professional look")
    print_menu_item("2", "Light Mode", "Classic white background")

    print_divider()
    print_tip("Press ENTER for default (Dark Mode)")

    choice = input("\n  👉 Your choice (1-2): ").strip()

    return "light" if choice == "2" else "dark"

def get_save_option():
    """Ask if user wants to save chart"""
    print_section("SAVE OPTIONS", "💾")

    print("\n  Would you like to save the chart as an image?\n")
    print_menu_item("1", "Yes", "Save as PNG file")
    print_menu_item("2", "No", "Just display on screen")

    choice = input("\n  👉 Your choice (1-2): ").strip()

    if choice == "1":
        filename = input("  📁 Filename (without extension): ").strip()
        if not filename:
            filename = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return f"{filename}.png"

    return None

def show_settings_menu(current_theme):
    """Show settings menu"""
    print_section("SETTINGS", "⚙️")

    print(f"\n  Current theme: {current_theme}")
    print("\n  What would you like to change?\n")
    print_menu_item("1", "Change Theme", "Switch between dark/light mode")
    print_menu_item("2", "View Dividends", "Show dividend history")
    print_menu_item("3", "Portfolio Summary", "Quick overview of VOO & JEPI")
    print_menu_item("B", "Back", "Return to main menu")

    return input("\n  👉 Your choice: ").strip().upper()

def show_dividends(ticker):
    """Display dividend information"""
    print_section(f"{ticker} DIVIDENDS", "💰")

    dividends = get_dividends(ticker)

    if dividends.empty:
        print("\n  No dividend data available.")
        return

    print(f"\n  Last 10 dividend payments:\n")
    print(f"  {'─' * 35}")
    print(f"  │ {'Date':<15} │ {'Amount':>15} │")
    print(f"  {'─' * 35}")

    for date, amount in dividends.tail(10).items():
        date_str = date.strftime('%Y-%m-%d')
        print(f"  │ {date_str:<15} │ ${amount:>14.4f} │")

    print(f"  {'─' * 35}")

    total = dividends.sum()
    avg = dividends.mean()
    print(f"\n  📊 Total (shown): ${total:.4f}")
    print(f"  📊 Average: ${avg:.4f}")

def show_portfolio_summary():
    """Show quick portfolio summary"""
    print_section("PORTFOLIO SUMMARY", "💼")

    print_loading("Fetching latest data...")

    voo_info = get_stock_info("VOO")
    jepi_info = get_stock_info("JEPI")

    if not voo_info or not jepi_info:
        print_error("Could not fetch stock information")
        return

    print(f"\n  {'═' * 55}")
    print(f"  ║ {'Stock':<8} │ {'Price':>10} │ {'Change':>12} │ {'Div Yield':>10} ║")
    print(f"  {'═' * 55}")

    voo_change = f"{'+' if voo_info['change'] >= 0 else ''}{voo_info['change']:.2f}"
    jepi_change = f"{'+' if jepi_info['change'] >= 0 else ''}{jepi_info['change']:.2f}"

    voo_div = f"{voo_info['dividend_yield']*100:.2f}%" if voo_info['dividend_yield'] else "N/A"
    jepi_div = f"{jepi_info['dividend_yield']*100:.2f}%" if jepi_info['dividend_yield'] else "N/A"

    print(f"  ║ {'VOO':<8} │ ${voo_info['price']:>9.2f} │ {voo_change:>12} │ {voo_div:>10} ║")
    print(f"  ║ {'JEPI':<8} │ ${jepi_info['price']:>9.2f} │ {jepi_change:>12} │ {jepi_div:>10} ║")
    print(f"  {'═' * 55}")

def confirm_settings(stock, period, interval, style, theme, indicators):
    """Display confirmation of all settings"""
    print_section("CONFIRM YOUR SETTINGS", "✅")

    stock_name = {"1": "VOO", "2": "JEPI", "3": "VOO vs JEPI"}.get(stock, stock)
    indicators_str = ", ".join(indicators) if indicators else "None"

    print(f"""
  ┌────────────────────────────────────────┐
  │  Stock:      {stock_name:<25} │
  │  Period:     {period:<25} │
  │  Interval:   {interval:<25} │
  │  Style:      {style:<25} │
  │  Theme:      {theme:<25} │
  │  Indicators: {indicators_str:<25} │
  └────────────────────────────────────────┘
    """)

    choice = input("  👉 Proceed with these settings? (Y/n): ").strip().lower()
    return choice in ["", "y", "yes"]


# ==================== MAIN FUNCTION ====================

def main():
    """Main application loop"""
    current_theme = Config.DEFAULT_THEME

    while True:
        clear_screen()
        print_header()

        # Step 1: Stock selection
        stock_choice = get_stock_choice()

        if stock_choice == "Q":
            print("\n  👋 Thank you for using Stock Chart Pro!")
            print("  📈 Happy investing!\n")
            break

        if stock_choice == "S":
            # Settings menu
            while True:
                settings_choice = show_settings_menu(current_theme)

                if settings_choice == "1":
                    current_theme = get_theme()
                    print_success(f"Theme changed to {current_theme}")
                elif settings_choice == "2":
                    ticker = input("  Enter ticker (VOO/JEPI): ").strip().upper()
                    if ticker in ["VOO", "JEPI"]:
                        show_dividends(ticker)
                    input("\n  Press ENTER to continue...")
                elif settings_choice == "3":
                    show_portfolio_summary()
                    input("\n  Press ENTER to continue...")
                elif settings_choice == "B":
                    break
            continue

        if stock_choice not in ["1", "2", "3"]:
            print_error("Invalid choice")
            input("  Press ENTER to continue...")
            continue

        # Step 2: Period
        period = get_period()

        # Step 3: Interval
        interval = get_interval(period)

        # Step 4: Chart style
        style = get_chart_style()

        # Step 5: Indicators
        indicators = get_indicators()

        # Step 6: Save option
        save_path = get_save_option()

        # Confirmation
        if confirm_settings(stock_choice, period, interval, style, current_theme, indicators):
            if stock_choice == "1":
                show_professional_chart("VOO", period, interval, style,
                                       current_theme, indicators, save_path=save_path)
            elif stock_choice == "2":
                show_professional_chart("JEPI", period, interval, style,
                                       current_theme, indicators, save_path=save_path)
            elif stock_choice == "3":
                show_comparison_chart(period, interval, style, current_theme,
                                     indicators, save_path=save_path)

        input("\n  Press ENTER to continue...")


if __name__ == "__main__":
    main()
