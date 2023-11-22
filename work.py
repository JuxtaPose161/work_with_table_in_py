from table_class import GigaTable 
from table_class import concat
from table_class import table_split

# Создаём переменную-таблицу
table_1 = GigaTable()

# Загружаем в неё файл
table_1.load_table('Table1.csv')
print('\n Так выглядит таблица при выводе \n')

# Выводим значения
table_1.print_table()
print()
print('get_rows_by_number: выводит list, в котором все найденные по индексу строчки - \n', table_1.get_rows_by_numbers(1,3))
print()
print('get_rows_by_index: выводит list, в котором все найденные по начальному значению строчки - \n', table_1.get_rows_by_index('1','3','5'))
print()
print('get_values: выводит list значений столбца - \n', table_1.get_values('bmi'), table_1.get_values(1))
print()
print('get_value: выводит значение ячейки - \n', table_1.get_value(1,3))
print()

# Меняем тип колонок 2-мя способами
print('set_column_types: устанавливает тип колонки, меняя значения колонок на этот тип \n')
table_1.set_column_types({0:int, 2:int})
table_1.set_column_types({'bmi': float, 'driving_license': bool}, by_number=False)

# Выводим опять значения
print('get_column_types: выводит dict, в котором key - столбец, а value - тип переменных в столбце - \n', table_1.get_column_types(by_number=False))
print()


# Задаём значения существующим столбцам
print('set_values: принимает list и имя-номер столбца, задаёт значения из list в столбец \n')
table_1.set_values([True,False,True,False,True],4)
print('set_value: принимает значение, имя-номер номер столбца и номер строки, задаёт значения в ячейке \n')
table_1.set_value('Artur','name',1)
print('Так выглядит таблица после изменений \n ')
table_1.print_table()

# Сохраняем изменённые данные
table_1.save_table('result.pickle')

# ЗАДАНИЯ:

print('\n \n Реализация заданий \n')

#   4 - Определение типа столбцов

table_2 = GigaTable()
table_2.load_table('result.pickle')
print('4: \nтип новой импортированной таблицы pickle - \n',table_2.get_column_types())
# В формате pickle в переменных сохраняется их тип данных, в csv и txt данные импортируются изачально как str,
# поэтому все строчки из таблиц csv и txt будут в str

#   3 - Склеивание и разделение таблиц

table_first = GigaTable()
table_second = GigaTable()
table_first.load_table('Table1.csv')
table_second.load_table('Table2.txt')

print('\n 3:')
print('Первая таблица \n') 
table_first.print_table()
print('\nВторая таблица \n') 
table_second.print_table()
print('\nСклеенная таблица \n')
table_result = concat(table_first, table_second)
table_result.print_table()
print('\nРазделённая таблица \n')
tsplit1, tsplit2 = table_split(table_result,2)
tsplit1.print_table()
print()
tsplit2.print_table()

#   6 - 7  Функции суммы, разности, деления, умножения, вычитания и сравнения столбцов

print('\n6 - 7: Весь функционал объединён в одной функции function_with_columns \n')

table_1.print_table()
print('Сложение - ',table_1.function_with_columns(2,'+',3,True))
print('Вычитание - ',table_1.function_with_columns(2,'-',3))
print('Умножение - ',table_1.function_with_columns(2,'*',3))
print('Деление - ',table_1.function_with_columns(2,'/',3))
print('Равенство - ',table_1.function_with_columns(2,'==',3))
print('Неравенстов - ',table_1.function_with_columns(2,'!=',3))
print('Больше - ',table_1.function_with_columns(2,'>',3, True))
print('Меньше - ',table_1.function_with_columns(2,'<',3))
print('\n Если оставить значение copy_in_table = True, то создастся столбец со значениями')
table_1.print_table()
print('\nfilter_row: фильтрует таблицу по столбцу со значениями bool - \n', table_1.filter_row(4))

