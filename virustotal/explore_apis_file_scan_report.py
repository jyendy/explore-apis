import json
import urllib3
import os

http = urllib3.PoolManager()

def lambda_handler(event, context):
    response = file_scan_report(event['resource'])
    
    body_response = json.loads(response.data.decode('utf-8'))
        
    return {
        'statusCode': response.status,
        'statusDescription': 'ALERT!' if body_response['positives'] > 0 else 'No problem!',
        'body': body_response
    }
    
def file_scan_report(resource):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {
        'apikey': os.getenv('apikey'),
        'resource': resource
    }

    encoded_params = urllib3.request.urlencode(params)
    
    return http.request(
        'GET',
        url + '?' + encoded_params
        )