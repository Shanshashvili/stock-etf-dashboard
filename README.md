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

## Requirements

- Python 3.7+
- [yfinance](https://pypi.org/project/yfinance/)
- [matplotlib](https://pypi.org/project/matplotlib/)

## Installation

1. **Clone or download this repository.**
2. **Install dependencies** using pip:

   ```sh
   pip install yfinance matplotlib
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

3. Follow the prompts in the terminal to select stocks, timeframes, periods, and chart styles.

## Features

- **Timeframe selection:** Choose from hourly, daily, weekly, or monthly data.
- **Stock selection:** View VOO, JEPI, or compare both.
- **Custom periods:** Advanced script allows custom date ranges.
- **Chart styles:** Line, area, and bar charts (advanced script).
- **Summary statistics:** Latest price, highest, lowest, and data points (advanced script).

## Troubleshooting

- If you encounter errors downloading data, check your internet connection and ensure the period/interval combination is valid.
- For issues with matplotlib display, ensure you are not running in a headless environment.

## License

This project is for educational and personal use.

---

**Enjoy visualizing VOO & JEPI ETF data!**
