import paramiko
import csv
import pysftp
from paramiko import SSHClient
import tkinter.filedialog
import pysftp as sftp
import pygsheets
import pandas as pd
import numpy as np
import zipfile
import boto3
import json
import os

# Create subdirectory if it doesn't exist
base_directory = '/home/KIPPNashvilleData'
subdirectory = 'accelerated_reader'
full_path = os.path.join(base_directory, subdirectory)
if not os.path.exists(full_path):
    os.makedirs(full_path)

host = "sftp.renaissance.com"
port = 22
transport = paramiko.Transport((host, port))
password = "hPMWyQ4k"
username = "3439022_Services@consult"

transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

localpath = os.path.join(full_path, 'ar.zip')
remotepath = '/KIPP Nashville.zip'
sftp.get(remotepath, localpath)

with zipfile.ZipFile(localpath, 'r') as zip_ref:
    zip_ref.extractall(full_path)

# Rename extracted CSV to lower case
extracted_csv_path = os.path.join(full_path, 'AR.csv')
new_csv_path = os.path.join(full_path, 'ar.csv')
if os.path.exists(extracted_csv_path):
    os.rename(extracted_csv_path, new_csv_path)

# Check if the final CSV is empty
if os.path.getsize(new_csv_path) == 0:
    os.remove(new_csv_path)
    print("CSV file was empty and has been deleted.")
else:
    # Pull in AWS credentials
    credentials_path = os.path.join(base_directory, "credentials_all.json")
    aws_config = json.load(open(credentials_path))["awss3"]
    access_key_id = aws_config["access_key_id"]
    access_secret_key = aws_config["access_secret_key"]
    bucket_name = aws_config["bucket_name"]

    s3 = boto3.resource('s3', aws_access_key_id=access_key_id,
                        aws_secret_access_key=access_secret_key,
                        )

    s3.meta.client.upload_file(new_csv_path, bucket_name, "ar/ar.csv")
    print("CSV file uploaded to S3.")

# print("all done")




# import paramiko
# import csv
# import pysftp
# from paramiko import SSHClient
# import tkinter.filedialog
# import pysftp as sftp
# # this module is new - you will need to pip install this
# import pygsheets
# import pandas as pd
# import numpy as np
# import zipfile
# import boto3
# import json
# import os

# # Create subdirectory if it doesn't exist
# base_directory = '/home/KIPPNashvilleData'
# subdirectory = 'accelerated_reader'
# full_path = os.path.join(base_directory, subdirectory)
# if not os.path.exists(full_path):
#     os.makedirs(full_path)

# host = "sftp.renaissance.com"
# port = 22
# transport = paramiko.Transport((host, port))
# password = "hPMWyQ4k"
# username = "3439022_Services@consult"

# transport.connect(username=username, password=password)
# sftp = paramiko.SFTPClient.from_transport(transport)

# localpath = os.path.join(full_path, 'ar.zip')
# remotepath = '/KIPP Nashville.zip'
# sftp.get(remotepath, localpath)

# with zipfile.ZipFile(localpath, 'r') as zip_ref:
#     zip_ref.extractall(full_path)

# # Rename extracted CSV to lower case
# extracted_csv_path = os.path.join(full_path, 'AR.csv')
# new_csv_path = os.path.join(full_path, 'ar.csv')
# if os.path.exists(extracted_csv_path):
#     os.rename(extracted_csv_path, new_csv_path)

# # Pull in AWS credentials
# credentials_path = os.path.join(base_directory, "credentials_all.json")
# aws_config = json.load(open(credentials_path))["awss3"]
# access_key_id = aws_config["access_key_id"]
# access_secret_key = aws_config["access_secret_key"]
# bucket_name = aws_config["bucket_name"]

# s3 = boto3.resource('s3', aws_access_key_id=access_key_id,
#                     aws_secret_access_key=access_secret_key,
#                     )

# s3.meta.client.upload_file(new_csv_path, bucket_name, "ar/ar.csv")

# print("all done")


#AR to google sheets chunk of code

#gc = pygsheets.authorize(client_secret = "/home/KIPPNashvilleData/credentials_bq.json")

#ar_file = gc.open("ar_data")
#ar_data = pd.read_csv("C:/Users/smccarron/OneDrive - Kipp Nashville/Documents/ar_data/AR_v2.csv")

#tab - 'PS Contact Info Export'
#ar = ar_file[0]
#ar.set_dataframe(ar_data,(1,1))