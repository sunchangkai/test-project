#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import time

from django.db import connection

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")


class SQLSearch(object):
    @staticmethod
    def search(str_sql=""):
        """
        Directly execute SQL statements to query multiple pieces of data. If no data is found,
        return an empty dict. If an error occurs, return False;
        :param str_sql: SQL statement，type(str)
        :return: res
        """

        if str_sql == "":
            return {}

        with connection.cursor() as cursor:
            try:
                cursor.execute(str_sql)
            except Exception as e:
                print(e.__str__())

            res = dictfetchall(cursor)

        return res

    @staticmethod
    def update(str_sql=""):
        """
        Directly execute SQL statements to update data. If an error occurs, return False;
        :param str_sql: SQL statement，type(str)
        :return: res or False
        """

        if str_sql == "":
            return False
        with connection.cursor() as cursor:
            try:
                res = cursor.execute(str_sql)
            except Exception as e:
                print(e.__str__())
                res = False

        return res

    @staticmethod
    def insert(str_sql=""):
        """
        Directly execute SQL statements to insert data. If an error occurs, return False;
        :param str_sql: SQL statement，type(str)
        :return: res or False
        """
        if str_sql == "":
            return False
        res = False
        with connection.cursor() as cursor:
            try:
                cursor.execute(str_sql)
                res = cursor.lastrowid
                # connection.commit()

            except Exception as e:
                print(e.__str__())

        return res

    @staticmethod
    def insertmany(str_sql="", values=()):
        """
        Directly execute inserting data by sql.

        Parameters
        -----------
        str_sql: sql string for insertting data, type(str);
        values: values for inserting data

        Return
        --------
        result: res or False
        """
        if str_sql == "":
            return False

        with connection.cursor() as cursor:
            try:
                res = cursor.executemany(str_sql, values)

            except Exception as e:
                print(e.__str__())
                res = False
        return res

    @staticmethod
    def delete(str_sql=""):
        """
        Directly execute SQL statements to delete data，If success, return True，if an error occurs, return False;
        :param str_sql:  SQL statement，type(str)
        :return: res or False
        """
        if str_sql == "":
            return False

        with connection.cursor() as cursor:
            try:
                res = cursor.execute(str_sql)
                if res == 1 or res == 0:
                    res = True
            except Exception as e:
                print(e.__str__())
                res = False

            return res

    # load a file to database
    @staticmethod
    def sql_load_bool(
        file_path, table_name, fields_terminated="*&*", lines_terminated_by="\n"
    ):
        """
        函数说明：Directly load a file to database
        :param file_path: ，type(str)
        :param table_name:，type(str)
        :param fields_terminated: default “*&*"，type(str)
        :param lines_terminated_by: default ”\n",type(str)
        :return: True or False
        """
        loadSQL = """LOAD DATA LOCAL INFILE '{0}' INTO TABLE {1}
                FIELDS TERMINATED BY '{2}' LINES TERMINATED BY '{3}';"""

        str_sql = loadSQL.format(
            file_path, table_name, fields_terminated, lines_terminated_by
        )
        is_load = False
        print(file_path)
        if os.path.isfile(file_path):
            print("filePath correct")
            with connection.cursor() as cursor:
                try:
                    cursor.execute(str_sql)
                    is_load = True
                except Exception as e:
                    print(e.__str__())
                    is_load = False
        else:
            print("FilePath Incorrect")

        return is_load

    @staticmethod
    def rollback():
        connection.rollback()


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
