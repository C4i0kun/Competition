from environment import Environment

import matplotlib.pyplot as plt

env = Environment()
env.run_simulation()

competitor = env.competitors[0]

plt.plot(competitor.cash_hist)
plt.title("Cash over time")
plt.xlabel("Time step")
plt.show()

plt.plot(competitor.income_hist, label="Production")
plt.plot(competitor.expenses_hist, label="Expenses")
plt.plot(competitor.profit_hist, label="Profit")
plt.title("Income and Cost over time")
plt.xlabel("Time step")
plt.legend()
plt.show()

plt.plot(competitor.products_hist)
plt.show()