from abc import abstractmethod


class IDocumentOperation:
    @abstractmethod
    def save_file(self, file_name, content):
        '''
        Saves the file.
        :param file_name:
        :param text to save:
        :return:
        '''
        pass

    @abstractmethod
    def open_file(self, file_name):
        '''
        Opens the file and print content
        :param file_name:
        :return:
        '''
        pass

    @abstractmethod
    def update_file(self, file_name, content, mode):
        '''
        Update the file.
        :param file_name:
        :param content:
        :return:
        '''
        pass

    @abstractmethod
    def rename_file(self, src_file_name, dst_file_name):
        '''
        Renames the file
        :param src_file_name:
        :param dst_file_name:
        :return:
        '''
        pass

    @abstractmethod
    def delete_file(self, file_name):
        '''
        Deletes the file
        :param file_name:
        :return:
        '''
        pass

    @abstractmethod
    def get_file_size(self, file_name):
        '''
        Returns the file size
        :param file_name:
        :return:
        '''
        pass

    @abstractmethod
    def get_created_time(self, file_name):
        '''
        Returns the date time of file creation
        :param file_name:
        :return:
        '''
        pass

    @abstractmethod
    def get_modified_time(self, file_name):
        '''
        Returns the date time of modified file
        :param file_name:
        :return:
        '''
        pass
