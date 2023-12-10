import os
import json
import boto3
from botocore.exceptions import NoCredentialsError

BUCKET_NAME  = 'nice-exam-devops-student-s3' 
FUNCTION_NAME = 's3_list_all_objects'

output_directory = r'/home/dorbourshan/projects/NICE/files'


def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
    except FileNotFoundError:
        print(f"The file {local_file_path} was not found")
    except NoCredentialsError:
        print("Credentials not available")

def delete_all_objects(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.all():
        obj.delete()

def invoke_lambda_function(lambda_function_name, payload):
   
    lambda_client = boto3.client('lambda')

    response = lambda_client.invoke(
        FunctionName=lambda_function_name,
        InvocationType='RequestResponse',  # Us
        Payload=payload
    )

    #Lambda function returns JSON
    response_payload = response['Payload'].read().decode('utf-8')
    return response_payload

def main() : 
    delete_all_objects(BUCKET_NAME)
    os.makedirs(output_directory, exist_ok=True)

    # Loop to create 1001 text files
    for n in range(1, 1002):
        file_name = f'{output_directory}/{n}'
        
        # Create and write content to the file
        with open(file_name, 'w') as file:
            file.write(f'This is file number {n}')

        s3_file_path = os.path.basename(file_name)

        with open(file_name, 'r') as file:
            upload_to_s3(file_name, BUCKET_NAME, s3_file_path)
        print(f' {n} ')

        
    print(f'Files created successfully in the {output_directory} directory.')

    lambda_client = boto3.client('lambda')
    payload = {}
    payload_json = json.dumps(payload)

    try:
        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            InvocationType='RequestResponse', 
            Payload=payload_json
        )

        # Read the response from the Lambda function
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))

        files_name_list = response_payload['body']
        files_name_list = files_name_list.sort()
        order_list = [str(i) for i in range(1,1002)]
        order_list = order_list.sort()

        if order_list != files_name_list : 
            print('The test fail')
        else : 
            print('The test fail')


    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
    
if __name__ == '__main__' : 
    main()



