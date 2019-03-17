from azure.storage.blob import BlockBlobService
import os

from .IDocumentOperation import IDocumentOperation


class Azure(IDocumentOperation):

    def __init__(self, account_name, account_key, container_name):
        try:
            self.__block_blob_service = BlockBlobService(account_name=account_name,
                                                         account_key=account_key)
            self.__container_name = container_name
            self.__block_blob_service.create_container(self.__container_name)
            self.__block_blob_service.set_container_acl(self.__container_name)
        except Exception as exception:
            print(str(exception))

    def save_file(self, file_name, text):
        '''
        Saves file or blob in the provided container
        :param file_name:
        :param text:
        :return:
        '''
        try:
            # Write text to the file.
            with open(file_name, 'w') as file:
                file.write(text)
            # Upload the created file, use local_file_name for the blob name
            self.__block_blob_service.create_blob_from_path(self.__container_name, file_name, file_name)

        except Exception as exception:
            print(str(exception))

    def open_file(self, file_name):
        '''
        Download the blob or file from container and print the content in it.
        :param file_name:
        :return:
        '''
        try:
            self.__block_blob_service.get_blob_to_path(self.__container_name, file_name, file_name)
            with open(file_name, 'r') as file:
                content = file.read()
                print(content)
        except Exception as exception:
            print(str(exception))

    def update_file(self, file_name, context, mode):
        '''
        Download the file/blob from container, update the data, again upload into container
        :param file_name:
        :param context:
        :param mode:
        :return:
        '''
        try:
            local_file = file_name + "_new"
            self.__block_blob_service.get_blob_to_path(self.__container_name, file_name, local_file)
            with open(local_file, mode) as file:
                file.write(context)
            self.__block_blob_service.create_blob_from_path(self.__container_name, file_name, local_file)
            self.__delete_file_locally(local_file)
            print("Updated successfully")
        except Exception as exception:
            print(str(exception))

    def rename_file(self, src_file_name, dst_file_name):
        '''
        Download the file, rename it, delete orginal file from container and upload renamed file
        :param src_file_name:
        :param dst_file_name:
        :return:
        '''
        try:
            self.__block_blob_service.get_blob_to_path(self.__container_name, src_file_name, src_file_name)
            os.rename(src_file_name, dst_file_name)
            self.__block_blob_service.create_blob_from_path(self.__container_name, dst_file_name, dst_file_name)
            self.__block_blob_service.delete_blob(self.__container_name, src_file_name)
            self.__delete_file_locally(dst_file_name)
            print("Renamed " + src_file_name + " --> " + dst_file_name)
        except Exception as exception:
            print(str(exception))

    def get_file_size(self, file_name):
        '''
        Returns file/blob size
        :param file_name:
        :return:
        '''
        try:
            return str(BlockBlobService.get_blob_properties(self.__block_blob_service, self.__container_name,
                                                            file_name).properties.content_length) + " B"
        except Exception as exception:
            print(str(exception))

    def get_created_time(self, file_name):
        '''
        Returns time at which file/blob is created
        :param file_name:
        :return:
        '''
        try:
            return BlockBlobService.get_blob_properties(self.__block_blob_service, self.__container_name,
                                                        file_name).properties.creation_time
        except Exception as exception:
            print(str(exception))

    def get_modified_time(self, file_name):
        '''
        Returns time at which file/blob is modified
        :param file_name:
        :return:
        '''
        try:
            return BlockBlobService.get_blob_properties(self.__block_blob_service, self.__container_name,
                                                        file_name).properties.last_modified
        except Exception as exception:
            print(str(exception))

    def delete_file(self, file_name):
        '''
        Deletes file/blob from container
        :param file_name:
        :return:
        '''
        try:
            self.__block_blob_service.delete_blob(self.__container_name, file_name)
            print("Deleted " + file_name)
        except Exception as exception:
            print(str(exception))

    def __delete_file_locally(self, file_name):
        '''
        Deletes the file from local storage created while renaming, updating file.
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
