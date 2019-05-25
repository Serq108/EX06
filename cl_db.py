import sqlite3
import os
from sqlib import sqlib


class Base:
    def __init__(self):
        self.conn = sqlite3.connect('my.db')
        self.cursor = self.conn.cursor()


    def commit(self):
        self.conn.commit()
        print('commit')


    def fk_on(self):
        self.cursor.execute('PRAGMA foreign_keys = ON;')
        self.commit()


class Table(Base):
    tablist = []
    def __init__(self):
        super(Table, self).__init__()
        self.name_t = ''
        self.name_col = []
        self.type_data = []
        self.flag_col = []
        self.fkey = ''
        self.fkid = ''


    def create_tab(self, name_t,name_col, type_data, flag_col):
        # print(name_t,name_col, type_data, flag_col)
        if sqlib.entry_check(name_t,Table.tablist):
            print('tab already exist')
            return 1
        if self.name_t:
            print('one obj one tab not ALLOWED!!!')
            return 1
        self.name_t = name_t
        self.name_col = name_col
        self.type_data = type_data
        self.flag_col = flag_col
        sql_str = sqlib.sqlreq_create_tab(self.name_t, self.name_col, self.type_data, self.flag_col)
        self.cursor.execute(sql_str)
        Table.tablist.append(self.name_t)
        print(sql_str)
        self.commit()
        return 0


    def create_tab_fk(self, name_t,name_col, type_data, flag_col, fkey, fkid):
        Table.fk_on(self)
        # print(name_t,name_col, type_data, flag_col)
        if sqlib.entry_check(name_t,Table.tablist):
            print('tab already exist')
            return 1
        if self.name_t:
            print('one obj one tab not ALLOWED!!!')
            return 1
        self.name_t = name_t
        self.name_col = name_col
        self.type_data = type_data
        self.flag_col = flag_col
        self.fkey = fkey
        self.fkid = fkid
        sql_str = sqlib.sqlreq_create_tab_fk(self.name_t, self.name_col, \
            self.type_data, self.flag_col, self.fkey, self.fkid)
        print(sql_str)
        self.cursor.execute(sql_str)
        Table.tablist.append(self.name_t)
        self.commit()
        return 0


    def delete_tab(self):
        sql_str = sqlib.drop_tab(self.name_t)
        self.cursor.execute(sql_str)
        self.commit()
        sqlib.del_item(self.name_t, Table.tablist)
        self.name_t = ''
        self.name_col = []
        self.type_data = []
        self.flag_col = []
        self.fkey = ''
        self.fkid = ''
        return 0


    def insert_into(self, list_values):
        if len(list_values) != len(self.name_col):
            print('invalid args')
            return 1

        # print(self.name_col)
        str_col = '('
        for i, item in enumerate(self.name_col):
            str_col += "'" + item + "'"
            if i < len(self.name_col) - 1:
                str_col += ', '
            else:
                str_col += ')'

        sql_str = sqlib.sqlreq_insert(self.name_t, str_col, list_values)
        #~ print(sql_str)
        self.cursor.execute(sql_str)
        self.commit()
        return 0


    def update_tab(self, col_name, old_value, new_value):
        if sqlib.entry_check(col_name, self.name_col):
            pass
        else:
            print('col not exist')
            return 1
        sql_str = sqlib.sql_updt(self.name_t, col_name, old_value, new_value)
        # print(sql_str)
        self.cursor.execute(sql_str)
        self.commit()
        return 0



if __name__ == '__main__':
    try:
        os.remove('my.db')
    except:
        print(u'нет  файл')
    name_t = 'contac'
    name_col = ['first_name', 'last_name', 'job', 'touwn_id']
    type_data = ['TEXT', 'TEXT', 'TEXT', 'INTEGER']
    flag_col = ['NOT NULL', 'NOT NULL', None, 'NOT NULL']
    list_values = ['Ivan', 'Ivanov', 'dev', 1]

    Table2 = Table()
    Table2.create_tab('Towns', ['Town', 'Street'], ['TEXT', 'TEXT'], ['NOT NULL', 'NOT NULL'])
    Table1 = Table()
    Table1.create_tab(name_t, name_col, type_data, flag_col)
    Table1.create_tab('nontallowed', name_col, type_data, flag_col)
    Table3 = Table()
    Table3.create_tab_fk('person_fk', name_col, type_data, flag_col, 'touwn_id', 'Towns(id)')
    Table4 = Table()
    Table4.create_tab('ssdf',name_col, type_data, flag_col)
    print('list tab',Table1.tablist)

    Table2.insert_into(['Moscow', 'Арбат'])
    Table2.insert_into(['London', 'Beach'])
    Table2.insert_into(['Berlin', 'Street'])
    Table1.insert_into(list_values)
    Table1.insert_into(['Bob', 'Spanch', 'webdev', 2])
    Table1.insert_into(['Ivan', 'Ivanenko', 'программист', 3])
    Table1.insert_into(['Ivan', 'Иваныч', 'сисадмин', 2])

    Table3.insert_into(list_values)
    Table3.insert_into(['Bob', 'Spanch', 'webdev', 2])
    Table3.insert_into(['Ivan', 'Ivanenko', 'программист', 3])
    Table3.insert_into(['Ivan', 'Иваныч', 'сисадмин', 2])
    Table3.insert_into(['Вофан', 'Иваныч', 'сисадмин', 3])

    Table4.delete_tab()
    print('list tab',Table1.tablist)
    Table1.update_tab('job', 'dev', 'повар')

