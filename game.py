import random
import asyncio
from typing import Any, Dict, Union

import numpy as np
import spade
from spade_game import Player, Server

# class representing the consumer consumers in the environment
class Consumer:
    def __init__(self, mean, std):
        self.money = max(np.random.normal(mean, std), 0.1)
        self.max_buying_price = self.money / 2
        self.steps_to_max = 100

    def update_max_buying_price(self):
        if self.steps_to_max > 0:
            y_0 = self.max_buying_price / self.money
            x_0 = 2 * np.arcsin(y_0) / np.pi
            dx = (1 - x_0) / self.steps_to_max
            x = x_0 + dx
            y = np.sin(np.pi * x / 2)
            self.max_buying_price = self.money * y
            self.steps_to_max -= 1

    def can_buy(self, price):
        return True if self.money > price else False

    def will_buy(self, price):
        return True if self.max_buying_price > price else False

# Here we define the server's update step
class Environment(Server):
    def step(self):
        # new buyers arrive
        for i in range(self.world_model["new_buyers_per_step"]):
            self.world_model["buyers"].append(
                Consumer(self.world_model["buyers_mean_money"], self.world_model["buyers_std_dev_money"])
            )

        # sort competitors by price
        valid_competitors = []
        for competitor in self.world_model["players"]:
            if (
                competitor["action"] is not None
                and competitor["products"] > 0
            ):
                valid_competitors.append(competitor)

        competitors_ordered = sorted(valid_competitors, key=lambda x: x["action"])

        # randomly sort buyers
        buyers_randomized = self.world_model["buyers"].copy()
        random.shuffle(self.world_model["buyers"])

        # buyers prefer lower prices
        while len(buyers_randomized) > 0 and len(competitors_ordered) > 0:
            buyer = buyers_randomized.pop(0)
            competitor = competitors_ordered.pop(0)

            if buyer.can_buy(competitor["action"]) and buyer.will_buy(competitor["action"]):
                self.world_model["buyers"].remove(buyer)
                competitor["cash"] += competitor["action"]
                competitor["products"] -= 1

            if competitor["products"] > 0:
                competitors_ordered.insert(0, competitor)

        # update max buying price
        for buyer in self.world_model["buyers"]:
            buyer.update_max_buying_price()

        # update competitors cash 
        for competitor in self.world_model["players"]:
            size = competitor["size"]
            products = competitor["products"]
            expenses = 50 * size + (1 / size) * (products ** 1.5)
            competitor["cash"] -= expenses
            competitor["products"] += 5 * size
            competitor["step"] += 1

# Player's action function
class Competitor(Player):
    def decide_action(self) -> None:
        print(self.world_model)
        self.action = 150

# Now, we define the initial conditions of the game
game_attributes = {
    "new_buyers_per_step": 10,
    "buyers_mean_money": 100,
    "buyers_std_dev_money": 250,
    "buyers": []
}

player_attributes = {
    "cash": 1000,
    "products": 0,
    "step": 0,
    "size": None # variable value: must be set in connection
}

# Main
async def main():
    server = Environment("exec_0@localhost", "caio123", game_attributes, player_attributes, frequency=1)
    await server.start()

    competitor_1 = Competitor("exec_1@localhost", "caio123", "exec_0@localhost", {"size": 1})
    await competitor_1.start()

    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    spade.run(main())