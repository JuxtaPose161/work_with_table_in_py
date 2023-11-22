import csv
import pickle


class GigaTable():
    def __init__(self):
        self.table = []

    #decorators for bug hunting (this part should be in another modul)
    def _dec_load_save_table(func):
        def check_errors(*arg):
            try:
                func(*arg)
            except:
                print('Путь до файла не введён или введён неправильно')
        return check_errors
    
    def _dec_get_func(func):
        def check_errors(*arg, **kwarg):
            try:
                result = func(*arg, **kwarg)
                return result
            except TypeError:
                print('Ошибка: Введены неправильные аргументы или их неправильное количество')
            except IndexError:
                print('Ошибка: Выбранная строка или столбец несуществует или не может быть передана')
            except ValueError:
                print('Ошибка: Один из переданных аргументов не существует')
            except:
                print('Ошибка: Что-то не так, что на тестах я не увидел)')
        return check_errors
    
    def _dec_set_func(func):
        def check_errors(*arg, **kwarg):
            try:
                func(*arg, **kwarg)
            except AttributeError:
                print('Ошибка: Передан аргумент неправильного типа')
            except ValueError:
                print('Ошибка: Невозможно установить одно или несколько переданных значений')
            except IndexError:
                print('Ошибка: Выбранная строка или столбец несуществует или не может быть передана')
            except TypeError:
                print('Ошибка: Введены неправильные аргументы или их неправильное количество')
            except: 
                print('Ошибка: Что-то не так, что на тестах я не увидел)')
        return check_errors
                         
    #main funcion's stack
    @_dec_load_save_table
    def load_table(self, path: str):
        format = path.split('.')[-1]

        if format == 'txt':
            with open(path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace(r'\t',' ').replace(',','.').split()
                    self.table.append(line)

        elif format == 'csv':
            with open(path, 'r') as f:
                reader = csv.reader(f,delimiter = ";")     
                for line in reader:
                    for value in line:
                        line[line.index(value)] = value.replace(',','.')
                    self.table.append(line)
        
        elif format == 'pickle':
            with open(path, 'rb') as f:
                self.table = pickle.load(f)  
        else:
            raise ValueError  
        
        column_types = []
        for value in self.table[1]:
            column_types.append(type(value))
        self.table.append(column_types)

    @_dec_load_save_table
    def save_table(self,path:str):
        format = path.split('.')[-1]
        output = self.table[:len(self.table)-1]

        if format == 'txt':
            with open(path, 'w+') as f:
                for line in output:
                    for i in line:
                        f.write(i)
                        f.write(' ')
                    f.write('\n')
        
        elif format == 'csv':
            with open(path, 'w+', newline='') as f:
                writer = csv.writer(f)
                for line in output:
                    writer.writerow(line)
        
        elif format == 'pickle':
            with open(path, 'wb') as f:
                pickle.dump(output, f)
        else:
            raise ValueError

    @_dec_get_func
    def get_rows_by_numbers(self, start:int, stop=None, copy_in_table=False):
        if start <=0:
            raise IndexError
        table_clone = self.table[start] if stop == None else self.table[start:stop+1]
        if copy_in_table == True:
            self.table = [self.table[0]] + table_clone + [self.table[-1]]
        elif type(copy_in_table)!=bool:
            raise TypeError
            
        return table_clone
    
    @_dec_get_func
    def get_rows_by_index(self,*val,copy_in_table=False):
        table_clone = []
        for value in val:
            for line in self.table[1:len(self.table)-1]:
                if value == line[0]:
                    table_clone.append(line)
                    break
            else:
                raise IndexError
        if copy_in_table == True:
            self.table = [self.table[0]] + table_clone + [self.table[-1]]
        elif type(copy_in_table)!=bool:
            raise TypeError
        
        return table_clone

    @_dec_get_func
    def get_column_types(self, by_number=True):
        column_types_dict = {}
        first_line = self.table[0]
        for column in range(len(first_line)):
            if by_number == False:
                column_types_dict[first_line[column]]=self.table[-1][column]
            elif type(by_number)!= bool:
                raise TypeError
            else:
                column_types_dict[column]=self.table[-1][column]
        return column_types_dict
    
    @_dec_set_func
    def set_column_types(self, types_dict: dict, by_number=True):
        for column, column_type in types_dict.items():
            if by_number==False:
                column = self.table[0].index(column)
            elif type(by_number)!= bool:
                raise IndexError
            self.table[-1][column] = column_type
        for column in range(len(self.table[0])):
            if self.table[-1][column] == bool and type(self.table[1][column])==str:
                for line in range(1,len(self.table)-1):
                    if self.table[line][column].lower() == 'false':
                        self.table[line][column] = ''

            for line in range(1,len(self.table)-1):
                self.table[line][column] = self.table[-1][column](self.table[line][column])

    @_dec_get_func
    def get_values(self, column=0):
        result_values = []
        if type(column)!=int:
            try:
                column = self.table[0].index(column)
            except:
                raise IndexError
        column_type = self.table[-1][column]
        for line in self.table[1:len(self.table)-1]:
            result_values.append(column_type(line[column]))
        
        return result_values
    
    @_dec_get_func  
    def get_value(self, column=0, line=1):
        if type(column)!=int:
            try:
                column = self.table[0].index(column)
            except:
                raise IndexError
        return self.table[line][column]
    
    @_dec_set_func
    def set_values(self, values:list, column=0):
        if type(values)!=list:
            raise AttributeError
        elif type(column)!=int:
            try:
                column = self.table[0].index(column)
            except:
                raise IndexError
        elif self.table[-1][column]!=type(values[0]):
            raise AttributeError
        for line in range(1,len(self.table)-1):
            self.table[line][column] = values[line-1]
        
    @_dec_set_func
    def set_value(self, value, column=0, line=1):
        if type(column)!=int:
            try:
                column = self.table[0].index(column)
            except:
                raise IndexError
        elif self.table[-1][column]!=type(value):
            raise AttributeError
        self.table[line][column] = value

    @_dec_get_func
    def print_table(self):
        column = [] 
        max_len_list = []       
        for column_index in range(len(self.table[0])):
            for line_index in range(len(self.table)-1):
                column.append(str(self.table[line_index][column_index]))
            max_len_list.append(len(max(column, key=len)))
            column = []
        
        for line in self.table[:len(self.table)-1]:
            row_on_print = ''
            for value_index in range(len(line)):
                column_width = max_len_list[value_index]
                row_on_print += f'|{str(line[value_index]):{column_width}}'
            row_on_print += '|'    
            print(row_on_print)   
    
    @_dec_get_func
    def function_with_columns(self, column_1, func:str, column_2, copy_in_table = False):
        result = []
        if type(column_1) != int:
            try:
                column_1 = self.table[0].index(column_1)
            except:
                raise IndexError
        if type(column_2) != int:
            try:
                column_2 = self.table[0].index(column_2)
            except:
                raise IndexError

        if func == '==':
            result.append(f'{self.table[0][column_1]}_equals_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(bool(self.table[line][column_1]==self.table[line][column_2]))  
        elif func == '>':
            result.append(f'{self.table[0][column_1]}_greater_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(bool(self.table[line][column_1]>self.table[line][column_2]))  
        elif func == '<':
            result.append(f'{self.table[0][column_1]}_less_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(bool(self.table[line][column_1]<self.table[line][column_2])) 
        elif func == '>=':
            result.append(f'{self.table[0][column_1]}_greater_or_equals_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(bool(self.table[line][column_1]>=self.table[line][column_2]))  
        elif func == '<=':
            result.append(f'{self.table[0][column_1]}_less_or_equals_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(bool(self.table[line][column_1]<=self.table[line][column_2]))
        elif func == '!=':
            result.append(f'{self.table[0][column_1]}_not_equals_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(bool(self.table[line][column_1]!=self.table[line][column_2]))
        elif func == '+':
            result.append(f'{self.table[0][column_1]}_add_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(self.table[line][column_1]+self.table[line][column_2])
        elif func == '-':
            result.append(f'{self.table[0][column_1]}_subtract_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(self.table[line][column_1]-self.table[line][column_2])
        elif func == '*':
            result.append(f'{self.table[0][column_1]}_multiply_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(self.table[line][column_1]-self.table[line][column_2])
        elif func == '/':
            result.append(f'{self.table[0][column_1]}_divide_{self.table[0][column_2]}')
            for line in range(1,len(self.table)-1):
                result.append(self.table[line][column_1]-self.table[line][column_2])
        else:
            raise ValueError

        if copy_in_table == True:
            for line in range(len(self.table)):
                self.table[line].append('')
            new_column = len(self.table[0])-1
            for line in range(len(self.table)-1):
                self.table[line][new_column]=result[line] 
            self.table[-1][new_column] = type(self.table[1][new_column])
        elif type(copy_in_table) != bool:
            raise TypeError
        return result
    

    def filter_row(self, bool_list, copy_in_table = False):
        table_clone = []
        if type(bool_list) != int:
            try:
                bool_list = self.table[0].index(bool_list)
            except:
                raise IndexError
        elif self.table[-1][bool_list]!=bool:
            print(self.table[-1][bool_list])
            raise TypeError
        for line in self.table[1:len(self.table)-1]:
            if line[bool_list] == True:
                table_clone.append(line)
        if copy_in_table == True:
            self.table = [self.table[0]] + table_clone + [self.table[-1]]
        return table_clone
        

def concat(*tables: GigaTable):
    try:
        result = []
        first_t, *next_t = tables
        if type(first_t) != GigaTable:
            raise TypeError
        for line in first_t.table[:len(first_t.table)-1]:
            result.append(line)
        column_type = first_t.table[-1]
        for t in next_t:
            if type(t) != GigaTable:
                raise TypeError
            if t.table[0] == result[0] and t.table[-1] == column_type:
                for line in t.table[1:len(t.table)-1]:
                    result.append(line)
            else:
                raise ValueError
        result.append(column_type)

        new_t = GigaTable()
        new_t.table = result

        return new_t
    except TypeError:
        print('Ошибка: Введен неправильный тип аргумента')
    except ValueError:
        print('Ошибка: Таблицы не совпадают содержанием')

def table_split(table_obj: GigaTable, row_number: int):
    try:
        if type(table_obj)!=GigaTable:
            raise TypeError
        elif type(row_number) != int:
            raise TypeError
        elif row_number >= len(table_obj.table)-2 or row_number < 1:
            raise ValueError
        header_row = table_obj.table[0]
        type_row = table_obj.table[-1]
        first_table = GigaTable()
        second_table = GigaTable()
        first_table.table.append(header_row)
        second_table.table.append(header_row)
        for line in table_obj.table[1:row_number+1]:
            first_table.table.append(line)
        for line in table_obj.table[row_number+1:len(table_obj.table)-1]:
            second_table.table.append(line)
        first_table.table.append(type_row)
        second_table.table.append(type_row)

        return first_table, second_table
    except TypeError:
        print('Ошибка: Введен неправильный тип аргумента')
    except ValueError:
        print('Ошибка: Передано неверное значение')
