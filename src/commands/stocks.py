
class StocksCommand:

    def __init__(self, chat, stockService):
        self.chat = chat
        self.stockService = stockService

    def execute(self, args, user_id):
        k = self.stockService.get_stocks(["AAPL"])
        
        print(k)
        self.chat.send(
            f"🤖 Responding \n{k}",
            user_id
        )