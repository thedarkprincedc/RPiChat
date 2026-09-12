import yfinance as yf

class StockService:
    def __init__(self):
        pass

    def stock_info_download(self, tickers, output_path):
        data = yf.download(
            tickers,
            start="2020-01-01",
            end="2026-01-01"
        )

        data.to_csv(output_path)