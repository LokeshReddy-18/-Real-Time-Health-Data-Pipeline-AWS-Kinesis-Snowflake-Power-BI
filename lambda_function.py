import json
import base64
import boto3
from datetime import datetime


s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'health-data-raw-bucket'
    processed_records = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8')
        payload = payload.strip('[]')
    
        timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S-%f')
        file_name = f"record-{timestamp}.json"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=payload
        )
        
        processed_records.append({
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(payload.encode('utf-8')).decode('utf-8')  # Encode back for Firehose
        })

    return {'records': processed_records}