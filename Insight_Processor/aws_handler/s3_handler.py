import json
import boto3
from shared import S3_BUCKET_NAME

s3_client = boto3.client('s3')

## TODO: Can we store the bigger responses in string ?
def store_data_to_s3 (file_path : str, upload_data):
    if(upload_data.__len__() == 0):
        print("Empty News Data File, Not uploaded to S3 bucket --Skipping!")
        return

    print("Uploading to S3 bucket")

    bucket_name = S3_BUCKET_NAME 
    
    file_content = json.dumps(upload_data)
    
    try:
        # Upload the file to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key= file_path,
            Body=file_content
        )
        print( {
            "statusCode": 200,
            "body": json.dumps(f"File {file_path} successfully uploaded to bucket {bucket_name}")
        } )
    except Exception as e:
        raise Exception({
            "statusCode": 500,
            "body": json.dumps(f"Error uploading file: {str(e)}")
        })
    

