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

        #return boolean, so I was need to check if it return True or False 
    except FileNotFoundError:
        print(f"The file {local_file_path} was not found")
    except NoCredentialsError:
        print("Credentials not available")

def delete_all_objects(bucket_name):
    # Create an S3 client
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objects.all():
        obj.delete()

def invoke_lambda_function(lambda_function_name, payload):
   # Create an lambda client
    lambda_client = boto3.client('lambda')
    try : 
        response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse', 
            Payload=payload
        )
        #Lambda function returns JSON
        response_payload =  json.loads(response['Payload'].read().decode('utf-8'))
        return response_payload
    
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")



def main() : 
    delete_all_objects(BUCKET_NAME)
    os.makedirs(output_directory, exist_ok=True)

    # Loop to create 1001 text files
    for n in range(1, 10):
        file_name = f'{output_directory}/{n}'
        
        # Create and write content to the file
        with open(file_name, 'w') as file:
            file.write(f'This is file number {n}')

        s3_file_path = os.path.basename(file_name)


        # It can be remove 
        with open(file_name, 'r') as file:
            upload_to_s3(file_name, BUCKET_NAME, s3_file_path)


        
    print(f'Files created successfully in the {output_directory} directory.')

  
    response = invoke_lambda_function(FUNCTION_NAME, json.dumps({}))

    status_code = response['statusCode']
    
    if status_code == 200 : 
        files_name_list = response['body']
        files_name_list = sorted(files_name_list)
        order_list = [str(i) for i in range(1,10)]
        order_list = sorted(order_list)

    if status_code != 200 or order_list != files_name_list : 
        print('The test fail')
    else : 
        print('The test success')
        print(files_name_list)


    
if __name__ == '__main__' : 
    main()



