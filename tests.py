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
# coffeeshop.replenish_warehouse(Latte=22, Americano=6)
# coffeeshop.replenish_warehouse(Cappuccino=16, Americano=10)



##################### КОМАНДЫ ДЛЯ ПРОСМОТРА БД: #####################

# coffeeshop.show_table(select_col=('operation', 'count_cups', 'total_sum'), to_sort=('total_sum', ))
# coffeeshop.show_table(select_col=('operation', 'count_cups', 'total_sum'), to_sort=('count_cups', ))
# coffeeshop.show_table(operation='пополнение склада')
# coffeeshop.show_table(timestamp=(datetime(2025, 5, 30, 17, 10, 23), ))


# TODO не работает
# coffeeshop.sumchecks_and_countcups(datetime(2025, 5, 26, 16, 00, 00), datetime(2025, 5, 30, 17, 10, 23))
# coffeeshop.show_table(datetime(2025, 5, 26, 16, 00, 00), datetime(2025, 5, 26, 16, 43, 30))

##################### КОМАНДЫ ДЛЯ ОБНОВЛЕНИЯ БД: #####################

# coffeeshop.update_table(col_name='check_number', new_val=10, count_cups=1)
# coffeeshop.update_table(col_name='total_sum', new_val=580, id=139)


##################### КОМАНДЫ ДЛЯ УДАЛЕНИЯ ИЗ БД: #####################

# coffeeshop.del_from_table(datetime(2025, 5, 26, 23, 46, 00))
# coffeeshop.delete_from_db(check_number=(1, ))
# coffeeshop.delete_from_db()
