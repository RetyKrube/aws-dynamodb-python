# Load the AWS SDK for Python
import boto3

# Load the exceptions for error handling
from botocore.exceptions import ClientError, ParamValidationError

# JSON handling
import json

# Create AWS service client and set region
db = boto3.client('dynamodb', region_name='us-east-1')

# Get a list of tables in region
def get_tables():
    try:
        data = db.list_tables()
        return data['TableNames']
    # An error occurred
    except ParamValidationError as e:
        print("Parameter validation error: %s" % e)
    except ClientError as e:
        print("Client error: %s" % e)
        
# Download JSON data from S3
s3 = boto3.client('s3', region_name='us-east-1')
def download_data():
    try:
        data_object = s3.get_object(
            Bucket='YOUR_BUCKET_NAME',
            Key='lab-data/test-table-items.json'
        )
        data_string = data_object['Body'].read().decode('utf-8')
        print('Downloaded from S3:')
        print(data_string)
        data = json.loads(data_string)
        return data
    # An error occured
    except ParamValidationError as e:
        print("Parameter validation error: %s" % e)
    except ClientError as e:
        print("Client error %s" % e)
        
def write_dynamo_db(json_data):
    try:
        data = db.batch_write_item(
            RequestItems = json_data
        )
        print('UnprocessedItems: ')
        print(data['UnprocessedItems'])
        return data
    # An error occured
    except ParamValidationError as e:
        print("Parameter validation error: %s" % e)
    except ClientError as e:
        print("Client error %s" % e)
        
def query_dynamo_db():
    try:
        data = db.query(
            TableName='test-table',
            IndexName='ProductCategory-Price-index',
            KeyConditionExpression='ProductCategory = :c AND Price <= :p',
            ExpressionAttributeValues={
                ':c': {'S': 'Bike'},
                ':p': {'N': '300'}
                }
        )
        print('Matching Items')
        for x in data['Items']:
            print(x)
    # An error occurred
    except ParamValidationError as e:
        print('Parameter validation error: %s' % e)
    except ClientError as e:
        print('Client error %s' % e)
        
        
# Main program
def main():
    table_names = get_tables()
    if (len(table_names)) == 0:
        print('No tables in region.')
    else:
        for x in table_names:
            print('Table name: '+ x )
        y = download_data()
        write_dynamo_db(y)
        query_dyanamo_db()
            
if __name__ == '__main__':
    main()
