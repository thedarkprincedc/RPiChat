import yfinance as yf

class StockService:
    def __init__(self):
        pass

    def get_stocks(self, tickers):
        return yf.download(
            tickers,
            start="2020-01-01",
            end="2026-01-01"
        )