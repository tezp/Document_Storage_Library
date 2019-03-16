import boto3
import os

from .IDocumentOperation import IDocumentOperation


class AWS(IDocumentOperation):
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        try:
            self.__s3_client = boto3.client('s3',
                                            aws_access_key_id=aws_access_key_id,
                                            aws_secret_access_key=aws_secret_access_key)
            self.__s3_resource = boto3.resource('s3',
                                                aws_access_key_id=aws_access_key_id,
                                                aws_secret_access_key=aws_secret_access_key)
            self.__bucket_name = bucket_name
        except Exception as exception:
            print(str(exception))

    def save_file(self, file_name, text):
        '''
        Saves the file into bucket
        :param file_name:
        :param text:
        :return:
        '''
        try:
            self.__create_bucket(self.__bucket_name)
            with open(file_name, 'w') as file:
                file.write(text)
            self.__s3_client.upload_file(file_name, self.__bucket_name, file_name)
        except Exception as exception:
            print(str(exception))

    def open_file(self, file_name):
        '''
        Download the file from bucket and prints
        :param file_name:
        :return:
        '''
        try:
            self.__s3_resource.Bucket(self.__bucket_name).download_file(file_name, file_name)
            with open(file_name, 'r') as file:
                content = file.read()
                print(content)
        except Exception as exception:
            print(str(exception))

    def update_file(self, file_name, context, mode):
        '''
        Downloads the file from bucket, save on local system, then update content and again upload file in s3 bucket
        :param file_name:
        :param context:
        :param mode:
        :return:
        '''
        try:
            local_file = file_name + "_new"
            self.__s3_resource.Bucket(self.__bucket_name).download_file(file_name, local_file)
            with open(local_file, mode) as file:
                file.write(context)
            self.__s3_client.delete_object(Bucket=self.__bucket_name, Key=file_name)
            self.__s3_client.upload_file(local_file, self.__bucket_name, file_name)
            self.__delete_file_locally(local_file)
            print("Updated successfully")
        except Exception as exception:
            print(str(exception))

    def rename_file(self, src_file_name, dst_file_name):
        '''
        Download file on local system, rename it, delete original file from bucket and upload renamed file.
        :param src_file_name:
        :param dst_file_name:
        :return:
        '''
        try:
            self.__s3_resource.Bucket(self.__bucket_name).download_file(src_file_name, src_file_name)
            os.rename(src_file_name, dst_file_name)
            self.__s3_client.delete_object(Bucket=self.__bucket_name, Key=src_file_name)
            self.__s3_client.upload_file(dst_file_name, self.__bucket_name, dst_file_name)
            self.__delete_file_locally(dst_file_name)
            print("Renamed " + src_file_name + " --> " + dst_file_name)
        except Exception as exception:
            print(str(exception))

    def get_file_size(self, file_name):
        '''
        Returns file size
        :param file_name:
        :return:
        '''
        try:
            return str(self.__s3_resource.Bucket(self.__bucket_name).Object(file_name).content_length) + ' B'
        except Exception as exception:
            print(str(exception))

    def get_creation_time(self, file_name):
        '''
        Return time at which file is created in bucket
        :param file_name:
        :return:
        '''
        try:
            object = self.__s3_resource.Object(self.__bucket_name, file_name)
            return object.last_modified
        except Exception as exception:
            print(str(exception))

    def get_modified_time(self, file_name):
        '''
        Return time at which file is modified in bucket
        :param file_name:
        :return:
        '''
        try:
            object = self.__s3_resource.Object(self.__bucket_name, file_name)
            return object.last_modified
        except Exception as exception:
            print(str(exception))

    def delete_file(self, file_name):
        '''
        Deletes the file from bucket
        :param file_name:
        :return:
        '''
        try:
            self.__s3_client.delete_object(Bucket=self.__bucket_name, Key=file_name)
        except Exception as exception:
            print(str(exception))

    def __create_bucket(self, bucket_name):
        '''
        Creates the bucket. It already exist then dont create.
        :param bucket_name:
        :return:
        '''
        try:
            response = self.__s3_client.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            for bucket in buckets:
                if bucket == bucket_name:
                    return
            self.__s3_client.create_bucket(Bucket=bucket_name)
        except Exception as exception:
            print(str(exception))

    def __delete_file_locally(self, file_name):
        '''
        deletes file from local system created while renaming, updating.
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
