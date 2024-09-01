import json
import urllib3  
import boto3
import os

s3_client = boto3.client('s3')
http = urllib3.PoolManager()
object_key = 'very_important_text_file.txt'

def lambda_handler(event, context):
    get_file_from_bucket()
    
    response = file_scan_request()
                        
    return {
        'statusCode': response.status,
        'body': json.loads(response.data.decode('utf-8'))
    }
    
def file_scan_request():
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': os.getenv('apikey')}
    
    with open('/tmp/' + object_key, 'rb') as f:
        files = {'file': (object_key, f.read())}

    return http.request(
        'POST',
        url + '?' + urllib3.request.urlencode(params),
        fields = files
        )
    
def get_file_from_bucket():
    s3_client.download_file('explore-apis-files', object_key, '/tmp/' + object_key)