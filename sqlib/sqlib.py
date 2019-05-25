import sys
import sqlite3

DATA_TYPES = ['NULL', 'INTEGER', 'TEXT']
FLAG_COL = [None, 'NOT NULL']


def check_str(strn):
    somestr = 'str'
    if type(strn) == type(somestr):
        return True
    else:
        return False


def check_int(intn):
    someint = 1
    if type(intn) == type(someint):
        return True
    else:
        return False


def entry_check(strn,list_str):
    entering = False
    for item in list_str:
        if strn == item:
            entering = True
    return entering


def del_item(item, list_item):
    for i, it in enumerate(list_item):
        if it == item:
            del list_item[i]

def check_name_col(listname):
    check_flag = True
    for name in listname:
        if not check_str(name):
            check_flag = False
    return check_flag


def check_entry_list(listname, chklist):
    check_flag = True
    for item in listname:
        if entry_check(item, chklist):
            pass
        else:
            check_flag = False
            break
    return check_flag


def sqlreq_create_tab(name_t,name_col, type_data, flag_col):
    sql_str = 'CREATE TABLE '
    if check_str(name_t):
        sql_str += name_t
    else:
        print('invalid argumets')
        sys.exit()
    sql_str += ' (id INTEGER PRIMARY KEY AUTOINCREMENT, '

    if len(name_col) == len(type_data) == len(flag_col):
        pass
    else:
        print('invalid argumets')
        sys.exit()

    if check_name_col(name_col):
        pass
    else:
        print('invalid argumets')
        sys.exit()

    if check_entry_list(type_data, DATA_TYPES):
        pass
    else:
        print('invalid argumets')
        sys.exit()

    if check_entry_list(flag_col, FLAG_COL):
        pass
    else:
        print('invalid argumets')
        sys.exit()

    for i, cols in enumerate(name_col):
        sql_str += cols + ' '+ type_data[i] + ' '
        if flag_col[i]:
            sql_str += flag_col[i] + ' '
        if i < len(name_col) - 1:
            sql_str += ','
        else:
            sql_str += ');'
    return sql_str


def sqlreq_create_tab_fk(name_t, name_col, type_data, flag_col, fkey, fkid):
    sql_str = sqlreq_create_tab(name_t,name_col, type_data, flag_col)
    sql_str = sql_str[:-2] + ', ' + 'FOREIGN KEY ('
    sql_str += fkey + ')' + ' REFERENCES ' + fkid + ');'
    return sql_str


def drop_tab(name_t):
    sql_str = 'DROP TABLE IF EXISTS ' + name_t
    return sql_str


def sqlreq_insert(name_t, str_col, list_values):
    sql_str = 'INSERT INTO '
    sql_str += name_t
    sql_str += str_col
    sql_str += ' VALUES ('
    for i, cols in enumerate(list_values):
        if check_str(list_values[i]):
            sql_str += "'" + list_values[i] + "'"
        if check_int(list_values[i]):
            sql_str += str(list_values[i])
        if i < len(list_values) - 1:
            sql_str += ', '
        else:
            sql_str += ');'
    return sql_str


def sql_updt(name_t, col_name, old_value, new_value):
    sql_str = 'UPDATE '
    sql_str += name_t
    sql_str += ' SET '
    sql_str += col_name + ' = ' + "'" + new_value + "'" + ' WHERE '\
        + col_name + ' = ' + "'" + old_value + "'"
    return sql_str


if __name__ == '__main__':
    conn = sqlite3.connect("my_lite.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    # cursor.execute(sqlreq_create_tab(name_t,name_col, type_data, flag_col))
    print('fk', cursor.execute( "PRAGMA foreign_keys" ))
    conn.commit()
