class Competitor:
    def __init__(self, size=10):
        self.size = size
        self.cash = 1000
        self.products = 0
        self.expenses = self.size * 10
        self.production = self.size

        self.step = 0
        self.cash_hist = [self.cash]
        self.income_hist = []
        self.expenses_hist = []
        self.profit_hist = []
        self.products_hist = []

    def run(self):
        self.decide_action()

    def update_state(self):
        self.cash -= self.expenses
        self.cash_hist.append(self.cash)
        self.income_hist.append(self.cash_hist[-1] - self.cash_hist[-2] + self.expenses)
        self.expenses_hist.append(self.expenses)
        self.profit_hist.append(self.cash_hist[-1] - self.cash_hist[-2])
        self.products_hist.append(self.products)

        # next step
        self.products += self.production
        self.step += 1

    def decide_action(self):
        # simple action: always selling for the same price
        self.action = 150

