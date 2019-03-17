import os
import sqlite3
from .IDocumentOperation import IDocumentOperation


class DBConnection:
    '''
    This class is used for database connection.
     '''
    __instance = None
    connection = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        '''
        Used to get database instance
        :return:
        '''
        if not cls.__instance:
            cls.__instance = DBConnection()
        return cls.__instance

    def get_cursor(self):
        '''
        return the connection cursor
        :return:
        '''
        if self.connection is None:
            self.connection = sqlite3.connect('test.db')
            self.cursor = self.connection.cursor()
        return self.cursor


class Sqlite(IDocumentOperation):
    '''
    This is Sqlite engine, used to perform operation on file which are in db
    '''

    def __init__(self):
        self.__create_table('Files')

    def __create_table(self, table_name):
        '''
        Creates table Files. It used DBConnection class to create db connection.
        :param table_name:
        :return:
        '''
        cursor = DBConnection.getInstance().get_cursor()
        query = "CREATE TABLE " + table_name + "(name TEXT, content TEXT, d1 TEXT, d2 TEXT)"
        try:
            cursor.execute(query)
            print('table ' + table_name + ' created successfully')
        except Exception as exception:
            print('Table ' + table_name + ' already created in database.')
            pass

    def save_file(self, file_name, context):
        '''
        Saves the file name and content in db
        :param file_name:
        :param context:
        :return:
        '''
        try:
            with open(file_name, 'w') as file:
                file.write(context)
            query = "INSERT INTO Files(name,content,d1,d2) values ('{}','{}',datetime('now'),datetime('now'))".format(
                file_name, context)
            cursor = DBConnection.getInstance().get_cursor()
            cursor.execute(query)
            DBConnection.getInstance().connection.commit()
        except Exception as exception:
            print(str(exception))

    def open_file(self, file_name):
        '''
        opens the file (here content column) and shows content
        :param file_name:
        :return:
        '''

        try:
            query = "SELECT content from Files where name='{}'".format(file_name)
            cursor = DBConnection.getInstance().get_cursor()
            cursor.execute(query)
            row = cursor.fetchone()[0]
            print(row)
        except Exception as exception:
            print(str(exception))

    def update_file(self, file_name, context, mode):
        '''
        first fetch the file from db and then append or overwrite context in it
        :param file_name:
        :param context:
        :param mode:
        :return:
        '''
        try:
            query = "SELECT content from Files where name='{}'".format(file_name)
            local_file = file_name + "_for_size"
            cursor = DBConnection.getInstance().get_cursor()
            cursor.execute(query)
            row = cursor.fetchone()[0]
            # read data from db
            with open(local_file, 'w') as file:
                file.write(row)
            # append or overwrite context
            with open(local_file, mode) as file:
                file.write(context)
            # Write updated data in db
            content = ''
            with open(local_file, 'r') as file:
                content = file.read()
            query = "UPDATE Files set content='{}',d2 = datetime('now') where name='{}'".format(content, file_name)
            cursor.execute(query)
            DBConnection.getInstance().connection.commit()
            print("Updated successfully")
        except Exception as exception:
            print(str(exception))

    def rename_file(self, src_file_name, dst_file_name):
        '''
        Rename the column name in db table.
        :param src_file_name:
        :param dst_file_name:
        :return:
        '''
        query = "UPDATE Files set name='{}' where name='{}'".format(dst_file_name, src_file_name)
        cursor = DBConnection.getInstance().get_cursor()
        try:
            cursor.execute(query)
            DBConnection.getInstance().connection.commit()
            print("Renamed " + src_file_name + " --> " + dst_file_name)
        except Exception as exception:
            print(str(exception))

    def get_file_size(self, file_name):
        '''
        Fetch the data from db. Write it in file and save locally, then find file size from local file
        :param file_name:
        :return:
        '''
        try:
            query = "SELECT content from Files where name='{}'".format(file_name)
            local_file = file_name + "_for_size"
            cursor = DBConnection.getInstance().get_cursor()
            cursor.execute(query)
            row = cursor.fetchone()[0]
            with open(local_file, 'w') as file:
                file.write(row)
            size = os.path.getsize(local_file)
            self.__delete_file_locally(local_file)
            return str(size) + " B"
        except Exception as exception:
            print(str(exception))

    def get_created_time(self, file_name):
        '''
        Get created file time from db table
        :param file_name:
        :return:
        '''
        query = "SELECT d1 from Files where name='{}'".format(file_name)
        cursor = DBConnection.getInstance().get_cursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()[0]
            return row
        except Exception as exception:
            print(str(exception))
            DBConnection.getInstance().connection.close()

    def get_modified_time(self, file_name):
        '''
        Get modified file time from db table. While updating content, modified time column also gets updated
        :param file_name:
        :return:
        '''
        query = "SELECT d2 from Files where name='{}'".format(file_name)
        cursor = DBConnection.getInstance().get_cursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()[0]
            return row
        except Exception as exception:
            print(str(exception))

    def delete_file(self, file_name):
        '''
        Delete the row from table.
        :param file_name:
        :return:
        '''
        query = "DELETE FROM Files where name='{}'".format(file_name)
        cursor = DBConnection.getInstance().get_cursor()
        try:
            cursor.execute(query)
            DBConnection.getInstance().connection.commit()
        except Exception as exception:
            print(str(exception))

    def __delete_file_locally(self, file_name):
        '''
        Delete the file which is created while getting size of file.
        :param file_name:
        :return:
        '''
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
            else:
                print("File not found")
        except Exception as exception:
            print(str(exception))
