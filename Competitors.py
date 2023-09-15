class Competitor:
    def __init__(self, size=1):
        self.size = size
        self.cash = 1000
        self.products = 0
        self.base_expenses = self.size * 50
        self.production = 5 * self.size 

        self.step = 0
        self.cash_hist = [self.cash]
        self.income_hist = []
        self.expenses_hist = []
        self.profit_hist = []
        self.products_hist = []

    def run(self):
        self.decide_action()

    def update_state(self):
        expenses = self.base_expenses + (1 / self.size) * (self.products ** 1.5)
        self.cash -= expenses
        self.cash_hist.append(self.cash)
        self.income_hist.append(self.cash_hist[-1] - self.cash_hist[-2] + expenses)
        self.expenses_hist.append(expenses)
        self.profit_hist.append(self.cash_hist[-1] - self.cash_hist[-2])
        self.products_hist.append(self.products)

        # next step
        self.products += self.production
        self.step += 1

    def decide_action(self):
        # simple action: always selling for the same price
        self.action = 50

