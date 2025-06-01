from COFFEESHOP import CoffeeShop
from datetime import datetime


coffeeshop = CoffeeShop('Starbucks Coffee Company')

##################### ДОБАВЛЕНИЕ ДАННЫХ: #####################
# coffeeshop.replenish_warehouse(Cappuccino=1)
# coffeeshop.replenish_warehouse(Cappuccino=10, Latte=22, Americano=15)
# coffeeshop.replenish_warehouse(Cappuccino=27, Latte=13)
# coffeeshop.replenish_warehouse(Espresso=9, Raf=40)

# coffeeshop.order_coffee(Cappuccino=1, Latte=2, Americano=2)
# coffeeshop.order_coffee(Cappuccino=4)
# coffeeshop.order_coffee(Latte=1, Raf=1)
# coffeeshop.order_coffee(Cappuccino=1)
# coffeeshop.order_coffee(Espresso=1)
# coffeeshop.order_coffee(Espresso=3, Latte=2)

##################### КОМАНДЫ ДЛЯ ПРОСМОТРА БД: #####################

# coffeeshop.show_table(table='sales')
# coffeeshop.show_table(table='sales', select_col=('check_number', 'type_coffee', 'count_cups'), to_sort=('count_cups',))
# coffeeshop.show_table(table='sales', type_coffee=('Latte', 'Espresso'))
# coffeeshop.show_table(table='sales', to_sort=('count_cups', 'price'))
# coffeeshop.show_table(table='sales', select_col=("check_number", "type_coffee", "price"), 
#                       to_sort=("price",))

# coffeeshop.show_table(table='warehouse')
# coffeeshop.show_table(table='stock', to_sort=('count_cups', ))

##################### КОМАНДЫ ДЛЯ ОБНОВЛЕНИЯ БД: #####################

# coffeeshop.update_table(table='sales', col_name='check_number', new_val=77, count_cups=1)
# coffeeshop.update_table(table='sales', col_name='timestamp', new_val='2025-05-28 15:03:39', id=32)
# coffeeshop.update_table(table='sales', col_name='timestamp', new_val='2025-05-27 10:23:12', id=30)
# coffeeshop.update_table(table='sales', col_name='timestamp', new_val='2025-05-26 12:43:02', id=29)


##################### КОМАНДЫ ДЛЯ УДАЛЕНИЯ ИЗ БД: #####################

# coffeeshop.delete_from_db(table='sales', timestamp='2025-06-01 17:06:22')
# coffeeshop.delete_from_db(table='warehouse')
# coffeeshop.delete_from_db(table='sales')
# coffeeshop.delete_from_db(table='stock')
# coffeeshop.delete_from_db(table='sales', type_coffee='Cappuccino')

##################### ФИЛЬТРЫ: #####################

# print(coffeeshop.sumchecks_and_countcups(datetime(2025, 5, 26), datetime(2025, 5, 30)))
# coffeeshop.calculate_profit() # затраты на закупку - прибыль с продаж
# coffeeshop.calculate_profit(dt_from="2025-05-26", dt_before="2025-06-01")
# coffeeshop.check_information() # номер чека, тип кофе и общая сумма чека
# coffeeshop.all_info()