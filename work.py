from table_class import GigaTable 
from table_class import concat
from table_class import table_split

table_1 = GigaTable()
table_1.load_table('Table1.csv')
table_1.print_table()
print(table_1.get_rows_by_numbers(1,3))
print(table_1.get_rows_by_index('1','3','5'))
table_1.set_column_types({0:int, 4:bool})
table_1.set_column_types({'bmi': float, 'driving_license': bool}, by_number=False)
table_1.print_table()
print(table_1.get_column_types(by_number=False))
print(table_1.get_values('bmi'), table_1.get_values(1))
table_1.set_values([True,False,False,False,True],4)
table_1.set_value(22,'age',5)
table_1.print_table()