from . import AWS
from . import Azure
from . import LocalFileSystem
from . import Sqlite


# @classmethod
# def select_engine(engine='', aws_access_key='', aws_bucket_name='', aws_secret_key='', azure_account_name='',
#                   azure_account_key='', aws_container_name=''):
#     if engine == 'local':
#         return LocalFileSystem()
#     elif engine == 'aws':
#         return AWS(aws_access_key, aws_secret_key, aws_bucket_name)
#     elif engine == 'azure':
#         return Azure(azure_account_key, azure_account_name, aws_container_name)
#     elif engine == 'sqlite':
#         return Sqlite()
#     raise Exception("Please select engine from this list -> [local,aws,azure,sqlite]")
