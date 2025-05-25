from COFFEESHOP import *
from db import DataBase



coffeeshop = CoffeeShop('Starbucks Coffee Company')
database = DataBase()

# print("изначально:")
# print(coffeeshop.balance_in_stock)
# print()

# coffeeshop.order_coffee(Cappuccino=1, Latte=2, Americano=7)


# print("после покупки cappuccino: 1, latte: 2, americano: 7:")
# print(coffeeshop.balance_in_stock)
# print()
coffeeshop.replenish_warehouse(Cappuccino=10, Latte=22, Americano=4)
# print("после пополнения склада cappuccino: 10, latte: 22, americano: 4:")
# print(coffeeshop.balance_in_stock)
# print()

