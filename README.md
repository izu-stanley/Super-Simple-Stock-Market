
# Super Simple Stock Market

The application simulates basic stock market operations including dividend yield and P/E ratio calculations, trade recording, volume-weighted stock price computations, and an overall GBCE All Share Index calculation.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Code Details](#code-details)
  - [Interactive Menu](#interactive-menu)
  - [Stock Operations](#stock-operations)
  - [Trade Recording](#trade-recording)
  - [Calculations](#calculations)
- [Logging and Error Handling](#logging-and-error-handling)
- [License](#license)

## Overview

The Simple Stock Market application provides an interactive CLI to perform several stock market calculations and operations. 
Users can:

- Calculate the dividend yield for both common and preferred stocks.
- Compute the P/E Ratio.
- Record buy or sell trades.
- Determine the Volume Weighted Stock Price (VWSP) for a stock based on recent trades.
- Calculate the GBCE All Share Index using the geometric mean of available stock prices.

This tool demonstrates practical use of Python's modern libraries, such as [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation and [Typer](https://typer.tiangolo.com/) for building a command-line interface.

## Features

- **Dividend Yield Calculation**: Computes dividend yield differently for common stocks (`last_dividend / price`) and preferred stocks (`(fixed_dividend * par_value) / price`).
- **P/E Ratio Calculation**: Determines the price-to-earnings ratio as `price / dividend`. If the dividend is zero, the ratio is considered undefined.
- **Trade Recording**: Enables users to record buy/sell trades with timestamp, quantity, and trade price.
- **Volume Weighted Stock Price (VWSP)**: Calculates VWSP based on trades recorded in the last 15 minutes.
- **GBCE All Share Index**: Computes the GBCE All Share Index as the geometric mean of all valid VWSPs.

## Project Structure

```
super-simple-stock-market/
├── pyproject.toml           # Poetry configuration with project metadata and dependencies.
├── README.md                # The README file.
│── tests                    # Containing multiple unit tests
└── src/
    ├── cli/
    │   └── application.py   # Contains the interactive_menu function and CLI logic.
    ├── models/
    │   ├── stock.py         # Stock model and methods for calculations.
    │   ├── trade.py         # Trade model with validation and unique ID generation.
    │   ├── stock_type.py    # Enum for stock types: COMMON and PREFERRED.
    │   └── side.py          # Enum for trade sides: BUY and SELL.
    └── util/
        └── __init__.py      # Utility functions such as set_up_stock_market() to initialize the market.
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/izu-stanley/Super-Simple-Stock-Market.git
   cd super-simple-stock-market
   ```

2. **Install Dependencies**

   The project uses [Poetry](https://python-poetry.org/) for dependency management. Install Poetry if you haven’t already, then run:

   ```bash
   poetry install
   ```

   This command will create a virtual environment and install the required packages:
   - Python 3.12
   - Pydantic (^2.10.6)
   - Typer (^0.15.2)
   - pytz (^2025.1)
   - pytest (^8.3.5)

## Usage

To run the interactive command-line application, use the following command inside 
the project's root directory:

```bash
python main.py
```

When executed, the application will display a menu with options:

```
Simple Stock Market Menu:
1. Calculate Dividend Yield
2. Calculate P/E Ratio
3. Record a Trade
4. Calculate Volume Weighted Stock Price (VWSP)
5. Calculate GBCE All Share Index
6. Exit
```

Select the desired option by entering the corresponding number. For example:
- Enter **1** to calculate the dividend yield for a specific stock by providing its symbol and price.
- Enter **3** to record a trade by specifying the stock symbol, quantity, trade side (`BUY` or `SELL`), and trade price.

## Code Details

### Interactive Menu

The interactive menu is defined in the `interactive_menu()` function. It 
continuously asks the user for input until the "Exit" option is selected.

### Stock Operations
- **Dividend Yield Calculation**: Uses a match-case to differentiate between common and preferred stocks.
- **P/E Ratio Calculation**: Relies on the dividend yield and accounts for cases where the dividend is zero.

### Trade Recording

Trades are recorded via the `record_trade()` method in both the `Stock` and `StockMarket` classes. The `Trade` model uses Pydantic to validate input data and auto-generate a unique trade ID. It ensures the trade side is either `BUY` or `SELL`.

### Calculations

- **Volume Weighted Stock Price (VWSP)**: Calculated by filtering trades that occurred 
 within the last 15 minutes and calculating a weighted average price.
- **GBCE All Share Index**: Calculated as the geometric mean of the VWSPs for all stocks that have trades in the specified time window.

## Logging and Error Handling

- **Logging**: The application leverages Python’s built-in `logging` module to log key actions (e.g., calculating ratios, recording trades, and adding stocks). Logs are set to the INFO level
- **Error Handling**: Input validation and try-except blocks are used throughout to handle errors gracefully. This ensures that if invalid data is provided (e.g., a negative price), an appropriate error message is shown.

