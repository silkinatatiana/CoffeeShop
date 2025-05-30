from datetime import datetime
from db import DataBase

BALANCE_IN_STOCK = {'Espresso': 10, 'Americano': 12, 'Cappuccino': 17, 'Latte': 35, 'Raf': 9}
db_instance = DataBase()


class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class CoffeeShop:
    def __init__(self, name, balance_in_stock=BALANCE_IN_STOCK):
        self.name = name
        self.cash_register = 0
        self.check_number = 0
        self.invoice = 0
        self.balance_in_stock = balance_in_stock
        self.coffee = {'Cappuccino': Coffee('Cappuccino', 350), 
                       'Latte': Coffee('Latte', 380), 
                       'Americano': Coffee('Americano', 250)}

    def order_coffee(self, **kwargs):
        total_price = 0
        drinks = []
        for drink, count in kwargs.items():
            self.verification(drink)
            if count > self.balance_in_stock[drink]:
                raise Exception(f"К заказу доступно {self.balance_in_stock[drink]} чашек {count}")

            total_price += self.coffee[drink].price * count
            self.balance_in_stock[drink] -= count
            drinks.append(f"{drink}: {count}, {self.coffee[drink].price}")

        self.cash_register += total_price
        self.print_a_check(coffee='\n'.join(drinks), total_price=total_price)
        db_instance.add_entry(check_number=self.check_number, operation='заказ кофе', type_coffee=', '.join(drinks), 
                              count_cups=count, total_sum=total_price)


    def verification(self, drink):
        if drink not in self.balance_in_stock:
            raise Exception(f"{drink} нет в меню")
        
    def print_a_check(self, coffee, total_price):
        self.check_number += 1

        print(f"Чек {self.check_number}\n{coffee}\n"
              f"Общая стоимость покупки: {total_price} руб.\n"
              f"{self.name}\n"
              f"{datetime.now().replace(microsecond=0)}")

    def replenish_warehouse(self, **kwargs): # пополнить склад
        drinks = []
        total_count = 0
        self.invoice += 1
        for drink, count in kwargs.items():
            self.verification(drink)
            self.balance_in_stock[drink] += count
            drinks.append(f"{drink}: {str(count)} шт.")
            total_count += count
        db_instance.add_entry(check_number=self.invoice, operation='пополнение склада', type_coffee=', '.join(drinks), 
                              count_cups=count)
        
    def show_table(self, select_col=None, to_sort = None, **kwargs):
        for line in db_instance.show_table(select_col, to_sort, **kwargs):
            print(*line)

    def sumchecks_and_countcups(self, dt_from, dt_before):
        print(db_instance.sumchecks_and_countcups(dt_from, dt_before))

    def update_table(self, col_name, new_val, **kwargs):
        db_instance.update_table(col_name, new_val, **kwargs)

    def delete_from_db(self, **kwargs):
        db_instance.delete_from_db(**kwargs)
        
       