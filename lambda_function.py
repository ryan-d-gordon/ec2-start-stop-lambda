import json
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Check if query parameters are present
    if 'queryStringParameters' in event:
        instance_id = event['queryStringParameters'].get('instance_id')
        action = event['queryStringParameters'].get('action')
        
        if instance_id and action:
            if action == 'start':
                ec2.start_instances(InstanceIds=[instance_id])
                print('Started your instance: ' + instance_id)
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'message': 'Instance started successfully'})
                }
            elif action == 'stop':
                ec2.stop_instances(InstanceIds=[instance_id])
                print('Stopped your instance: ' + instance_id)
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'message': 'Instance stopped successfully'})
                }
            else:
                print('Invalid action specified')
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Invalid action specified'})
                }
    
    # If the instance_id is incorrect or missing query parameters
    print('Invalid instance ID or missing query parameters, instance not started/stopped')
    return {
        'statusCode': 401,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Invalid instance ID or missing query parameters'})
    }
