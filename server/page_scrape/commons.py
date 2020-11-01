import logging
import mongoengine
import page_scrape
import boto3
from botocore.exceptions import NoCredentialsError
import urllib.request


def dataLogging(obj, prefix=''):
    obj = obj
    for key in obj:
        if isinstance(
                obj[key], mongoengine.base.datastructures.BaseList) and len(obj[key]) > 0:
            if isinstance(obj[key][0], page_scrape.models.ImageInfo):
                for k in range(len(obj[key])):
                    dataLogging(obj[key][k], ' '+key,)
            else:
                print(prefix, key, ':', obj[key])
        elif isinstance(obj[key], page_scrape.models.ImageInfo):
            dataLogging(obj[key], ' '+key)
        else:
            print(prefix, key, ':', obj[key])


def downloadAndSave(url, path):
    urllib.request.urlretrieve(
        url, "00000001.jpg")


# ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
# SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


# def upload_to_aws(local_file, bucket, s3_file):
#     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
#                       aws_secret_access_key=SECRET_KEY)

#     try:
#         s3.upload_file(local_file, bucket, s3_file)
#         print("Upload Successful")
#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False


# uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')
