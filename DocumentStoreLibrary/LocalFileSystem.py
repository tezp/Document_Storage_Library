import os
from datetime import datetime

from .IDocumentOperation import IDocumentOperation


class LocalFileSystem(IDocumentOperation):
    '''
    This is Local file storage engine.
    '''

    def __init__(self):
        pass

    def save_file(self, file_name, context):
        '''
        Saves the given context into file_name
        :param file_name:
        :param context:
        :return:
        '''
        try:
            with open(file_name, 'w') as file:
                file.write(context)
        except Exception as exception:
            print(str(exception))

    def open_file(self, file_name):
        '''
        Open the given file and prints content from it
        :param file_name:
        :return:
        '''
        try:
            with open(file_name, 'r') as file:
                content = file.read()
                print(content)
        except Exception as exception:
            print(str(exception))

    def update_file(self, file_name, context, mode):
        '''
        Updates the file according to mode (append or overwrite)
        :param file_name:
        :param context:
        :param mode:
        :return:
        '''

        try:
            if os.path.exists(file_name):
                with open(file_name, mode) as file:
                    file.write(context)
                print("Updated successfully")
            else:
                print("File not found")

        except Exception as exception:
            print(str(exception))

    def rename_file(self, src_file_name, dst_file_name):
        '''
        Renames the file
        :param src_file_name:
        :param dst_file_name:
        :return:
        '''
        try:
            if os.path.exists(src_file_name) or os.path.exists(dst_file_name):
                os.rename(src_file_name, dst_file_name)
                print("Renamed " + src_file_name + " --> " + dst_file_name)
            else:
                print("one of the file not found")
        except Exception as exception:
            print(str(exception))

    def get_file_size(self, file_name):
        '''
        Return the file size
        :param file_name:
        :return:
        '''
        try:
            if os.path.exists(file_name):
                return str(os.path.getsize(file_name)) + " B"
            else:
                return "File not found"
        except Exception as exception:
            print(str(exception))

    def get_created_time(self, file_name):
        '''
        Returns the time ata which file is created
        :param file_name:
        :return:
        '''
        try:
            if os.path.exists(file_name):
                return str(datetime.fromtimestamp(os.path.getctime(file_name)))
            else:
                return "File not found"

        except Exception as exception:
            print(str(exception))

    def get_modified_time(self, file_name):
        '''
        Returns the time ata which file is modified
        :param file_name:
        :return:
        '''
        try:
            if os.path.exists(file_name):
                return str(datetime.fromtimestamp(os.path.getmtime(file_name)))
            else:
                return "File not found"
        except Exception as exception:
            print(str(exception))

    def delete_file(self, file_name):
        '''
        Deletes the file from local file system
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
