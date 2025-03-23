import time

import typer

from src.util import set_up_stock_market


def interactive_menu() -> None:
    """
    Displays the interactive menu and processes user selections.
    """

    market = set_up_stock_market()

    while True:
        typer.echo("\nSuper Simple Stock Market Menu:")
        typer.echo("1. Calculate Dividend Yield")
        typer.echo("2. Calculate P/E Ratio")
        typer.echo("3. Record a Trade")
        typer.echo("4. Calculate Volume Weighted Stock Price (VWSP)")
        typer.echo("5. Calculate GBCE All Share Index")
        typer.echo("6. Exit")
        try:
            choice = typer.prompt("Select an option (1-6)").strip()
        except (EOFError, KeyboardInterrupt):
            typer.echo("\nExiting application.")
            raise typer.Exit()

        match choice:
            case "1":
                symbol = typer.prompt("Enter stock symbol").upper().strip()
                price = float(typer.prompt("Enter price"))
                if symbol in market.stocks:
                    try:
                        result = market.stocks[symbol].dividend_yield(price)
                        typer.echo(
                            f"Dividend Yield for {symbol} at price {price} is: {result:.4f}")
                    except Exception as e:
                        typer.echo(f"Error: {e}")
                else:
                    typer.echo("Stock not found.")
            case "2":
                symbol = typer.prompt("Enter stock symbol").upper().strip()
                price = float(typer.prompt("Enter price"))
                if symbol in market.stocks:
                    try:
                        result = market.stocks[symbol].pe_ratio(price)
                        if result is None:
                            typer.echo(
                                f"P/E Ratio for {symbol} at price {price} is undefined (dividend is zero).")
                        else:
                            typer.echo(
                                f"P/E Ratio for {symbol} at price {price} is: {result:.4f}")
                    except Exception as e:
                        typer.echo(f"Error: {e}")
                else:
                    typer.echo("Stock not found.")
            case "3":
                symbol = typer.prompt("Enter stock symbol").upper().strip()
                try:
                    quantity = int(typer.prompt("Enter quantity"))
                    trade_side = typer.prompt(
                        "Enter trade side (buy/sell)").strip().upper()
                    trade_price = float(typer.prompt("Enter trade price"))

                    market.record_trade(symbol, quantity, trade_price, trade_side)
                    typer.echo(f"Trade recorded for {symbol}.")
                except Exception as e:
                    typer.echo(f"Error recording trade: {e}")
            case "4":
                symbol = typer.prompt("Enter stock symbol").upper().strip()
                if symbol in market.stocks:
                    result = market.stocks[symbol].volume_weighted_stock_price()
                    if result is None:
                        typer.echo(f"No trades in the past 15 minutes for {symbol}.")
                    else:
                        typer.echo(
                            f"Volume Weighted Stock Price for {symbol} is: {result:.4f}")
                else:
                    typer.echo("Stock not found.")
            case "5":
                result = market.all_share_index()
                if result is None:
                    typer.echo("No trades available to calculate GBCE All Share Index.")
                else:
                    typer.echo(f"GBCE All Share Index is: {result:.4f}")
            case "6":
                typer.echo("Exiting application.")
                break
            case _:
                typer.echo("Invalid option. Please choose a number between 1 and 6.")

        time.sleep(2)
