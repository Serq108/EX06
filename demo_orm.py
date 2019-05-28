import sqlite3
import os
from sqlib import sqlib


class Base:
    def __init__(self):
        self.conn = sqlite3.connect('my.db')
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()
        # print('commit')

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

    def create_tab(self, name_t, name_col, type_data, flag_col):
        # print(name_t,name_col, type_data, flag_col)
        if sqlib.entry_check(name_t, Table.tablist):
            print('tab already exist')
            return 1
        if self.name_t:
            print('one obj one tab not ALLOWED!!!')
            return 1
        self.name_t = name_t
        self.name_col = name_col
        self.type_data = type_data
        self.flag_col = flag_col
        sql_str = sqlib.sqlreq_create_tab(self.name_t, self.name_col, 
                                          self.type_data, self.flag_col
        )
        self.cursor.execute(sql_str)
        Table.tablist.append(self.name_t)
        self.commit()
        return 0

    def create_tab_fk(self, name_t, name_col, type_data, flag_col, fkey, fkid):
        Table.fk_on(self)
        # print(name_t,name_col, type_data, flag_col)
        if sqlib.entry_check(name_t, Table.tablist):
            print('tab already exist')
            return 1
        if self.name_t:
            print('one obj one tab not ALLOWED!!!')
            return 1
        # check_entry_list(listname, chklist):
        self.name_t = name_t
        self.name_col = name_col
        self.type_data = type_data
        self.flag_col = flag_col
        self.fkey = fkey
        self.fkid = fkid
        sql_str = sqlib.sqlreq_create_tab_fk(self.name_t, self.name_col, self.type_data, self.flag_col, self.fkey, self.fkid)
        # print(sql_str)
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
        if len(list_values) != len(self.name_col)-1:
            print('invalid args')
            return 1
        n_col = self.name_col[1:]
        str_col = '('
        for i, item in enumerate(n_col):
            str_col += "'" + item + "'"
            if i < len(n_col) - 1:
                str_col += ', '
            else:
                str_col += ')'
        sql_str = sqlib.sqlreq_insert(self.name_t, str_col, list_values)
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


class Select(Base):
    def sel_from_tab(self, name_t, list_col):
        if sqlib.entry_check(name_t, Table.tablist):
            pass
        else:
            print('no table')
        sql_str = 'SELECT * FROM ' + name_t
        self.cursor.execute(sql_str)
        names_col = [description[0] for description in self.cursor.description]
        if sqlib.check_entry_list(list_col, names_col):
            pass
        else:
            print('invalid col names')
        sql_str = sqlib.sql_sel_fr_tab(name_t, list_col)
        # print('selc_str', sql_str)
        self.cursor.execute(sql_str)
        self.commit()
        rows = self.cursor.fetchall()
        list_respns = [row for row in rows]
        return list_respns

    def sel_all_with_jn(self, obj_tab_fk, obj_tab):
        if obj_tab_fk.fkey:
            pass
        else:
            print('NO frgn key')
            return 1
        list_col = obj_tab_fk.name_col[:-1] + obj_tab.name_col[1:]
        sql_str = sqlib.sql_join(obj_tab_fk.name_t, obj_tab.name_t, list_col, obj_tab_fk.fkid[:-1], obj_tab_fk.fkey)
        self.cursor.execute(sql_str)
        self.commit()
        rows = self.cursor.fetchall()
        list_respns = [row for row in rows]
        return list_respns


if __name__ == '__main__':
    # удаление файла базы данных для демнтрации
    try:
        os.remove('my.db')
    except FileNotFoundError:
        print(u'нет  файл')
    # данные для ввода в базу
    name_t = 'contac'
    name_col = ['prsn_id', 'first_name', 'last_name', 'job', 'touwn_id']
    type_data = ['INTEGER PRIMARY KEY AUTOINCREMENT', 
                'TEXT', 'TEXT', 'TEXT', 'INTEGER'
    ]
    flag_col = ['NOT NULL', 'NOT NULL', 'NOT NULL', None, 'NOT NULL']
    list_values = ['Ivan', 'Ivanov', 'dev', 1]
    Table1 = Table()  # создаем объект класса таблица
    Table1.create_tab(name_t, name_col, type_data, flag_col)  # создаем таблицу
        # передаем в метод имя таблицы, списки названий столбцов, типов и флагов (типа 'NOT NULL')
    Table1.create_tab('nontallowed', name_col, type_data, flag_col)  # один объект
        # может создать только одну таблицу 
    Table2 = Table()
    Table2.create_tab('Towns', ['twn_id', 'Town', 'Street'], 
                     ['INTEGER PRIMARY KEY AUTOINCREMENT', 'TEXT', 'TEXT'],
                     ['NOT NULL', 'NOT NULL', 'NOT NULL']
    )
    Table3 = Table() 
    Table3.create_tab_fk('person_fk', name_col, type_data, flag_col, 'touwn_id', 'Towns(twn_id)')
        # создание таблицы с внешним ключем
    Table4 = Table()
    Table4.create_tab('ssdf', name_col, type_data, flag_col)
    Table1.insert_into(list_values)  # значения вводятся одним списком кроме ключевого поля
        # есть проверка на корректность
    Table1.insert_into(['Bob', 'Spanch', 'webdev', 2])
    Table1.insert_into(['Ivan', 'Ivanenko', 'программист', 3])
    Table1.insert_into(['Ivan', 'Иваныч', 'сисадмин', 2])
    Table2.insert_into(['Moscow', 'Арбат'])
    Table2.insert_into(['London', 'Beach'])
    Table2.insert_into(['Berlin', 'Street'])
    Table3.insert_into(list_values)
    Table3.insert_into(['Bob', 'Spanch', 'webdev', 2])
    Table3.insert_into(['Ivan', 'Ivanenko', 'программист', 3])
    Table3.insert_into(['Ivan', 'Иваныч', 'сисадмин', 2])
    Table3.insert_into(['Вофан', 'Иваныч', 'сисадмин', 3])
    Table3.insert_into(['Вофан', 'Фофаныч', 'сисадмин', 3])
    Table4.delete_tab()  # удаляет таблицу из базы и объект 
        # получает возможность создать табицу т.к. атрибуты обнуляются
    Table1.update_tab('job', 'dev', 'повар')  # реализует апдейт 
        # передается имя столбца , старое значение, новое значение
    sel1 = Select()  # создаем объект класса cелект
    print(sel1.sel_from_tab('contac', ['first_name', 'last_name']))
    # реализует селект столбцов по выбору из таблицы столбцы передаются ввиде списка
        # реализована проверка на наличие аблицы и столбцов
    print(sel1.sel_all_with_jn(Table3, Table2))  # реализует джойн таблицы 
        # принимат 2 аргумента объектов типа таблицы и присоединяет 2ю таблицу
        # по внешнему ключу если ключ есть в первой
