from datetime import datetime
from db import DataBase

db_instance = DataBase('coffeeshop.db', 'sales', 'warehouse', 'stock')

class Coffee:
    def __init__(self, name, selling_price, purchase_cost, count):
        self.name = name
        self.selling_price = selling_price
        self.purchase_cost = purchase_cost
        self.count = count

class CoffeeShop:
    CHECK_NUMBER = 1
    INVOICE = 1

    def __init__(self, name):
        self.name = name
        self.cash_register = 0
        self.coffee = {'Cappuccino': Coffee('Cappuccino', selling_price=350, purchase_cost=120, count=0), 
                       'Latte': Coffee('Latte', selling_price=380, purchase_cost=120, count=0), 
                       'Americano': Coffee('Americano', selling_price=250, purchase_cost=72, count=0),
                       'Espresso': Coffee('Espresso', selling_price=230, purchase_cost=70, count=0),
                       'Raf': Coffee('Raf', selling_price=420, purchase_cost=135, count=0)}
        self.load_last_data()

    def load_last_data(self):
        last_check = db_instance.get_last_check_number()
        last_invoice = db_instance.get_last_invoice_number()

        if last_check is not None:
            CoffeeShop.CHECK_NUMBER = last_check + 1
        if last_invoice is not None:
            CoffeeShop.INVOICE = last_invoice + 1

        for name in self.coffee:
            self.coffee[name].count = db_instance.get_current_stock(name)

    def order_coffee(self, **kwargs):
        total_sum = 0
        count_cups = 0
        drinks = []

        for drink, amount in kwargs.items():
            self.verification(drink)

            if amount > self.coffee[drink].count:
                raise Exception(f"К заказу доступно {self.coffee[drink].count} чашек {drink}")

            total_sum += self.coffee[drink].selling_price * amount
            count_cups += amount
            db_instance.update_stock(drink, amount, add=False)
            drinks.append(f"{drink}: {str(count_cups)} шт., {self.coffee[drink].selling_price} руб/шт")
            db_instance.add_entry_sales(CoffeeShop.CHECK_NUMBER, self.coffee[drink].name, amount, self.coffee[drink].selling_price)
            
        self.cash_register += total_sum
        self.print_a_check(coffee='\n'.join(drinks), total_price=total_sum)
        CoffeeShop.CHECK_NUMBER += 1

    def verification(self, drink):
        if drink not in self.coffee:
            raise Exception(f"{drink} нет в меню")
        
    def print_a_check(self, coffee, total_price):
        print(f"Чек {CoffeeShop.CHECK_NUMBER}\n{coffee}\n"
              f"Общая стоимость покупки: {total_price} руб.\n"
              f"{self.name}\n"
              f"{datetime.now().replace(microsecond=0)}")

    def replenish_warehouse(self, **kwargs):
        for drink, amount in kwargs.items():
            self.verification(drink)
            db_instance.update_stock(drink, amount, add=True)
            db_instance.add_entry_warehouse(invoice=CoffeeShop.INVOICE, type_coffee=drink, count_cups=amount, 
                                            purchase_cost=self.coffee[drink].purchase_cost)

        CoffeeShop.INVOICE += 1

    def show_table(self, table, select_col=None, to_sort = None, **kwargs):
        for line in db_instance.show_table(table, select_col, to_sort, **kwargs):
            print(*line)

    def update_table(self, table, col_name, new_val, **kwargs):
        db_instance.update_table(table, col_name, new_val, **kwargs)

    def delete_from_db(self, **kwargs):
        db_instance.delete_from_db(**kwargs)
        
    def sumchecks_and_countcups(self, dt_from, dt_before):
        return db_instance.sumchecks_and_countcups(dt_from, dt_before)

    def calculate_profit(self, dt_from=None, dt_before=None):
        for line in db_instance.calculate_profit(dt_from, dt_before):
            print(*line)

    def check_information(self):
        for line in db_instance.check_information():
            print(*line)

    def all_info(self):
        for line in db_instance.all_info():
            print(*line)