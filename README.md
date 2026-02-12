# VOO & JEPI Stock Chart Viewer

## Overview

This project provides three Python scripts for visualizing historical price data for the VOO (S&P 500 ETF) and JEPI (JPMorgan Equity Premium Income ETF). Each script offers a different level of interactivity and customization, allowing users to select timeframes, compare funds, and adjust chart styles.

## Project Structure

- [`stock_chart_basic.py`](stock_chart_basic.py):
  Simple chart viewer. Lets you select a timeframe and displays price charts for both VOO and JEPI.

- [`stock_chart_interactive.py`](stock_chart_interactive.py):
  Interactive chart viewer. Allows selection of stock (VOO, JEPI, or both) and timeframe. Supports comparison charts.

- [`stock_chart_advanced.py`](stock_chart_advanced.py):
  Advanced chart viewer. Enables selection of stock, timeframe, custom periods, and chart style (line, area, bar). Provides summary statistics.

- [`stock_chart_pro.py`](stock_chart_pro.py):
  Professional chart viewer with multiple chart styles (Line, Area, Bar, Candlestick), technical indicators (SMA, EMA, Bollinger Bands), dividend tracking, image saving, dark/light theme, price alerts, and portfolio summary.

## Requirements

- Python 3.7+
- [yfinance](https://pypi.org/project/yfinance/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [pandas](https://pypi.org/project/pandas/) (for pro version)
- [mplfinance](https://pypi.org/project/mplfinance/) (for pro version)
- [numpy](https://pypi.org/project/numpy/) (for pro version)

## Installation

1. **Clone or download this repository.**
2. **Install dependencies** using pip:

  ```sh
  pip install yfinance matplotlib pandas mplfinance numpy
  ```

## Usage

1. Open a terminal in the project directory.
2. Run the desired script:
   - Basic viewer:

     ```sh
     python stock_chart_basic.py
     ```

   - Interactive viewer:

     ```sh
     python stock_chart_interactive.py
     ```

   - Advanced viewer:

     ```sh
     python stock_chart_advanced.py
     ```

   - Professional viewer:

     ```sh
     python stock_chart_pro.py
     ```

3. Follow the prompts in the terminal to select stocks, timeframes, periods, chart styles, indicators, and other options.

## Features

- **Timeframe selection:** Choose from hourly, daily, weekly, or monthly data.
- **Stock selection:** View VOO, JEPI, or compare both.
- **Custom periods:** Advanced and pro scripts allow custom date ranges.
- **Chart styles:** Line, area, bar, and candlestick charts (pro script).
- **Technical indicators:** SMA, EMA, Bollinger Bands (pro script).
- **Dividend tracking:** View dividend history (pro script).
- **Portfolio summary:** Quick overview of VOO & JEPI (pro script).
- **Theme selection:** Dark and light modes (pro script).
- **Image saving:** Save charts as PNG files (pro script).
- **Summary statistics:** Latest price, highest, lowest, and data points.

## Troubleshooting

- If you encounter errors downloading data, check your internet connection and ensure the period/interval combination is valid.
- For issues with matplotlib display, ensure you are not running in a headless environment.
- If you see errors about missing columns, try updating yfinance and pandas to the latest versions.

## License

This project is for educational and personal use.

---

**Enjoy visualizing VOO & JEPI ETF data!**
