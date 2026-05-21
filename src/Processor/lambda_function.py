import json
import boto3
import urllib.parse
import uuid
from decimal import Decimal 

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']
    
    object_key = urllib.parse.unquote_plus(raw_key)
    
    try:
        response = s3.get_object(Bucket=bucket, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')
        
      
        data = json.loads(file_content, parse_float=Decimal) 
        
        table = dynamodb.Table('IoT-telemetry-data-cmps465')
        
        record_id = data.get('record_id', str(uuid.uuid4()))
        client_name = data.get('client_name', 'Unknown-User')
        amount = data.get('amount', Decimal('0'))   
        status = data.get('status', 'Normal') 
        
        table.put_item(
            Item={
                'record_id': record_id,
                'file_source': object_key,
                'client_name': client_name,
                'amount': amount,
                'status': status
            }
        )
        
        if status.lower() != 'normal':
            sns.publish(
                TopicArn='arn:aws:sns:eu-central-1:696817466596:Pipeline-Alerts-cmps465',
                Message=f"Alert! IoT Device registered an unusual status: {status}. Reading: {amount}.",
                Subject="IoT Telemetry System Alert"
            )
            
        return {
            'statusCode': 200,
            'body': json.dumps('Telemetry data processed successfully!')
        }
        
    except Exception as e:
        print(f"Error processing object {object_key} from bucket {bucket}: {str(e)}")
        raise e