import numpy as np

class Stock():
    def __init__(self, inital_price:float=100):
        self.price = inital_price
    def fluctuate_from_current_normal(self, percentage:float):
        change = round( np.random.normal() * (percentage/100 * self.price) , 2)
        self.price += change
    def fluctuate_from_current_random(self, percentage:float):
        change = round( np.random.random() * (percentage/100 * self.price) , 2)
        sign = np.random.choice(np.array([-1,1]))
        self.price += change*sign
    def fluctuate_with_direction(self, price_aimed:float, percentage:float):
        price_taken_as_mean = (self.price + price_aimed)/2
        change = round( np.random.random() * (percentage/100 * price_taken_as_mean) , 2)
        sign = np.random.choice(np.array([-1,1]))
        self.price = price_taken_as_mean + change*sign

class Player():
    def __init__(self):
        self.net_position = 0
        self.net_cashflow = 0
        #Cashflow is considered to be positive when sold and -ve otherwise
    def show_PnL(self, current_price:float):
        return round(self.net_position*current_price + self.net_cashflow,2)
    def buy(self, current_price:float):
        self.net_position+=1
        self.net_cashflow -= current_price
    def sell(self, current_price:float):
        self.net_position-=1
        self.net_cashflow += current_price

""" stk = Stock()
print(stk.price)
for i in range(10):
    stk.fluctuate_from_current_random(2)
    print(round(stk.price,2)) """