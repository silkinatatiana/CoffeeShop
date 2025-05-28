from COFFEESHOP import *
from datetime import datetime


coffeeshop = CoffeeShop('Starbucks Coffee Company')

##################### ДОБАВЛЕНИЕ ДАННЫХ: #####################

# coffeeshop.order_coffee(Cappuccino=1, Latte=2, Americano=7)
# coffeeshop.order_coffee(Cappuccino=4)
# coffeeshop.order_coffee(Latte=1, Americano=1)
# coffeeshop.order_coffee(Cappuccino=1)
# coffeeshop.order_coffee(Latte=4)
# coffeeshop.order_coffee(Americano=3, Latte=2)

# coffeeshop.replenish_warehouse(Cappuccino=10, Latte=22, Americano=4)


##################### КОМАНДЫ ДЛЯ ПРОСМОТРА БД: #####################

# coffeeshop.show_table()
# coffeeshop.show_table('пополнение склада')  
# coffeeshop.show_table(3, 5)
# coffeeshop.show_table(datetime(2025, 5, 26, 16, 00, 00), datetime(2025, 5, 26, 16, 43, 30))
# coffeeshop.show_table(datetime(2025, 5, 26, 16, 00, 00), datetime(2025, 5, 26, 16, 43, 30), show_all=False)


##################### КОМАНДЫ ДЛЯ СОРТИРОВКИ БД: #####################

# coffeeshop.sort_table()
# coffeeshop.sort_table(by_sum=False)


##################### КОМАНДЫ ДЛЯ УДАЛЕНИЯ ИЗ БД: #####################

# coffeeshop.del_from_table(datetime(2025, 5, 26, 23, 46, 00))
# coffeeshop.del_from_table('заказ кофе')
# coffeeshop.del_from_table('Latte')
