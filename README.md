# DevOps Student Position Exam Documentation

## Testing

To thoroughly test the implemented solution, I created a comprehensive test scenario. This involved creating a user specifically for testing purposes, granting permissions for read, write, and delete operations on the S3 bucket, as well as invoking the Lambda function.

### User Setup for Testing

I created a dedicated user with the necessary permissions to perform testing operations. The user was granted the following permissions:
- `s3:GetObject`, `s3:ListBucket`, `s3:PutObject`, `s3:DeleteObject` on the S3 bucket.
- `lambda:InvokeFunction` on the Lambda function.

### Local Environment Configuration

To interact with AWS services locally, we configured our local development environment. This involved setting up AWS credentials, including the access key and secret key, to authenticate API requests. I used the AWS CLI to configure these credentials.

### Test Execution

created a script in Python to automate the testing process. The script performed the following steps:
1. Created 1001 files locally.
2. Uploaded the files to the S3 bucket.
3. Invoked the Lambda function.
4. Checked if all 1001 files were returned as a list.

### Test Results

After executing the test script, I verified that the Lambda function correctly listed all objects in the S3 bucket. The test was considered successful as all 1001 files were returned as expected.

