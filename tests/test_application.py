from datetime import datetime

import pytest

from src.cli.application import interactive_menu


class DummyStock:
    """
    Dummy implementations for stocks and market to be used in application tests
    """

    def __init__(self):
        self.trade_recorded = False

    def dividend_yield(self, price: float) -> float:
        """
        Returns a fixed dividend yield for testing
        """

        return 0.1

    def pe_ratio(self, price: float) -> float:
        """
        Returns a fixed P/E ratio for testing
        """

        return 10.0

    def record_trade(self, trade) -> None:
        """
        Set default value when recording a trade
        """

        self.trade_recorded = True

    def volume_weighted_stock_price(self, now: datetime = None) -> float:
        """
        Return a fixed VWSP value for testing
        """

        return 80.0

class DummyMarket:
    """
    Dummy implementation for market to be used in application tests
    """

    def __init__(self):
        """
        Set up "ABC" stock; used to test the "stock not found" scenario too.
        """

        self.stocks = {"ABC": DummyStock()}

    def record_trade(self, symbol: str, quantity: int, trade_price: float, side) -> None:
        """
        Set default value when recording a trade
        """

        if symbol in self.stocks:
            self.stocks[symbol].trade_recorded = True

    def all_share_index(self) -> float:
        """
        Return a fixed GBCE All Share Index value for testing
        """
        return 100.0


def dummy_set_up_stock_market() -> DummyMarket:
    """
    Dummy set_up_stock_market function that returns dummy market
    """
    return DummyMarket()


# Patch the set_up_stock_market function inside the interactive menu function
@pytest.fixture(autouse=True)
def patch_set_up_stock_market(monkeypatch) -> None:
    monkeypatch.setattr("src.cli.application.set_up_stock_market", dummy_set_up_stock_market)


def run_interactive_menu(monkeypatch, inputs) -> None:
    """
    Helper function to simulate interactive_menu input responses.
    """

    input_iter = iter(inputs)
    monkeypatch.setattr("typer.prompt", lambda prompt_text: next(input_iter))
    # Run the interactive_menu. Since our dummy responses eventually include "6", the loop exits.
    interactive_menu()


def test_interactive_menu_calculate_dividend_yield(monkeypatch, capsys) -> None:
    """
    Test Interactive Calculate Dividend Yield.
    Control Flow: "1" -> option; "ABC" -> valid symbol; "80" -> price; then "6" to exit.
    """

    inputs = ["1", "ABC", "80", "6"]
    run_interactive_menu(monkeypatch, inputs)
    output = capsys.readouterr().out

    # Expect the dividend yield message for ABC to be printed.
    assert "Dividend Yield for ABC" in output, f"Output was:\n{output}"

def test_interactive_menu_calculate_pe_ratio(monkeypatch, capsys) -> None:
    """
    Test Interactive Calculate P/E Ratio.
    Control Flow: "2" -> option; "ABC" -> valid symbol; "80" -> price; then "6" to exit.
    """

    inputs = ["2", "ABC", "80", "6"]
    run_interactive_menu(monkeypatch, inputs)
    output = capsys.readouterr().out
    assert "P/E Ratio for ABC" in output, f"Output was:\n{output}"

def test_interactive_menu_record_trade(monkeypatch, capsys) -> None:
    """
    Test Interactive Record Trade.
    Control Flow: "3" -> option; "ABC" -> valid symbol; "100" -> price; BUY -> Side;
    80 -> quantity; then "6" to exit.
    """

    inputs = ["3", "ABC", "100", "BUY", "80", "6"]
    run_interactive_menu(monkeypatch, inputs)
    output = capsys.readouterr().out
    assert "Trade recorded for ABC" in output, f"Output was:\n{output}"

def test_interactive_menu_vwsp(monkeypatch, capsys) -> None:
    """
    Test Interactive VWSP.
    Control Flow: "4" -> option; "ABC" -> valid symbol; then "6" to exit.
    """
    inputs = ["4", "ABC", "6"]
    run_interactive_menu(monkeypatch, inputs)
    output = capsys.readouterr().out
    assert "Volume Weighted Stock Price for ABC" in output, f"Output was:\n{output}"

def test_interactive_menu_gbce(monkeypatch, capsys) -> None:
    """
    Test the GBCE interactive menu.
    Control Flow: "5" -> option; then "6" to exit.
    """
    inputs = ["5", "6"]
    run_interactive_menu(monkeypatch, inputs)
    output = capsys.readouterr().out
    assert "GBCE All Share Index" in output, f"Output was:\n{output}"

def test_interactive_menu_invalid_option(monkeypatch, capsys) -> None:
    """
    Test "Invalid Option" by providing an invalid option to the menu.
    Control Flow: "9" -> invalid option; then "6" to exit.
    """

    inputs = ["9", "6"]
    run_interactive_menu(monkeypatch, inputs)
    output = capsys.readouterr().out
    assert "Invalid option" in output, f"Output was:\n{output}"

def test_interactive_menu_stock_not_found(monkeypatch, capsys) -> None:
    """
    Test "stock not found" by providing a symbol that doesn't exist in the dummy market.
    Control Flow: "1" -> option; "ZZZ" -> invalid symbol; "80" -> price; then "6" to
    exit.
    """

    inputs = ["1", "ZZZ", "80", "6"]
    run_interactive_menu(monkeypatch, inputs)
    output = capsys.readouterr().out
    assert "Stock not found." in output, f"Output was:\n{output}"
