# aws_module.py
import boto3
import os
from dotenv import load_dotenv

# 加載 .env 文件中的環境變數
load_dotenv()

def get_files_from_s3(bucket_name):
    # 從環境變數中獲取 AWS 憑證
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # 初始化 S3 客戶端，使用從環境變數中讀取的憑證
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # 列出 S3 bucket 中的文件
    response = s3.list_objects_v2(Bucket=bucket_name)
    files = [item['Key'] for item in response.get('Contents', [])]
    return files

def download_file_from_s3(bucket_name, file_key, download_path):
    # 從環境變數中獲取 AWS 憑證
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # 初始化 S3 客戶端
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # 下載指定的文件
    s3.download_file(bucket_name, file_key, download_path)
