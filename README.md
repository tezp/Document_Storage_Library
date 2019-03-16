# Document_Storage_Library
This library is used to perform operation on file. Files can be on Local system, AWS S3, Sqlite or on azure blob storage. 

### Prerequisites
Packages/Libraries need to install to run the project.

* boto3
```bash
pip3 install boto3
```
* azure-storage-blob
```bash
pip3 install azure-storage-blob
```
* sqlite3
```bash
pip3 install sqlite3
```
## Steps to run the project: 
1. First step is to import the library.
```python
 import DocumentStoreLibrary
```
2. Select the engine (Engine is nothing but the storage utility like local storage, AWS S3, Azure or sqlite).
```python
  local_engine = DocumentStoreLibrary.LocalFileSystem.LocalFileSystem()
```
3. Then, we can start file operations. Save the file by providing name and content.
```python
  local_engine.save_file('sample1.txt',"This is my first library")
```
4. To open the file and print the data.
```python
  local_engine.open_file('sample1.txt')
```
5. To get the date of file creation.
```python
  local_engine.get_created_time('sample1.txt')
```
6. To get the date of file modification.
```python
  local_engine.get_modified_time('sample1.txt')
```
7. To get the size of file.
```python
  local_engine.get_file_size('sample1.txt')
```
8. To update the file content with append and overwrite mode [a|w].
```python
  local_engine.update_file('sample1.txt','This is updation testing','a')
```
9. To rename the file, rename_file(src_file_name,dst_file_name).
```python
  local_engine.rename_file('sample1.txt','sample2.txt')
```
10. To delete the file from storage engine.
```python
  local_engine.delete_file('sample1.txt')
```
## Change the storage engine:
1. For AWS S3, provide credentials like aws_access_key_id,aws_secret_access_key and bucket_name.
```python
aws_engine = DocumentStoreLibrary.AWS.AWS('aws_access_key_id','aws_secret_access_key','bucket_name')
```
2. For Azure storage blob, provide credentials like account_name,account_name and container_name.
```python
azure_engine = DocumentStoreLibrary.Azure.Azure('account_name','account_key','container_name')
```
3. For Sqlite, no need to prvide any arguments. By default it will create <b>test.db</b> database and <b>Files</b> table to store content
```python
sqlite_engine = DocumentStoreLibrary.Sqlite.Sqlite()
```
   
