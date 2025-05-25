from datetime import datetime
from functools import wraps
from db import DataBase

BALANCE_IN_STOCK = {'Espresso': 10, 'Americano': 12, 'Cappuccino': 17, 'Latte': 35, 'Raf': 9}
db_instance = DataBase()

# class DBdecorator:
#     db_instance = DataBase()

#     def __init__(self, methods_to_log):
#         self.methods_to_log = methods_to_log

#     def __call__(self, cls):
#         for method_name in self.methods_to_log:
#             if hasattr(cls, method_name):
#                 original_method = getattr(cls, method_name)

#             @wraps(original_method)
#             def wrapper(*args, **kwargs):
#                 DBdecorator.db_instance.add_entry(
#                     operation=method_name.__name__,
#                     count=kwargs.get('count'),
#                     timestamp=datetime.now().replace(microsecond=0),
#                     summa=kwargs.get('summa')
#                     )
#                 return original_method(*args, **kwargs)
#             setattr(cls, method_name, wrapper)
        
#         return cls


class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# @DBdecorator(['order_coffee', 'replenish_warehouse'])
class CoffeeShop:
    def __init__(self, name, balance_in_stock=BALANCE_IN_STOCK):
        self.name = name
        self.cash_register = 0
        self.check_number = 0
        self.balance_in_stock = balance_in_stock
        self.coffee = {'Cappuccino': Coffee('Cappuccino', 350), 
                       'Latte': Coffee('Latte', 380), 
                       'Americano': Coffee('Americano', 250)}

    def order_coffee(self, *args, **kwargs):
        total_price = 0
        drinks = []
        for drink, count in kwargs.items():
            self.verification(drink)
            if count > self.balance_in_stock[drink]:
                raise Exception(f"К заказу доступно {self.balance_in_stock[drink]} чашек {count}")

            total_price += self.coffee[drink].price * count
            self.balance_in_stock[drink] -= count
            drinks.append(f"{drink}: {str(count)} шт., {self.coffee[drink].price} руб/шт")

        self.cash_register += total_price
        self.print_a_check(coffee='\n'.join(drinks), total_price=total_price)
        db_instance.add_entry(operation='заказ кофе', type_coffee=', '.join(drinks), 
                              count=count, timestamp=datetime.now().replace(microsecond=0), summa=total_price)

    def verification(self, drink):
        if drink not in self.balance_in_stock:
            raise Exception(f"{drink} нет в меню")
        
    def print_a_check(self, coffee, total_price):
        self.check_number += 1

        print(f"Чек {self.check_number}\n{coffee}\n"
              f"Общая стоимость покупки: {total_price} руб.\n"
              f"{self.name}\n"
              f"{datetime.now().replace(microsecond=0)}")

    def replenish_warehouse(self, *args, **kwargs): # пополнить склад
        drinks = []
        total_count = 0
        for drink, count in kwargs.items():
            self.verification(drink)
            self.balance_in_stock[drink] += count
            drinks.append(f"{drink}: {str(count)} шт.")
            total_count += count
        db_instance.add_entry(operation='пополнение склада', type_coffee=', '.join(drinks), 
                              count=total_count, timestamp=datetime.now().replace(microsecond=0))