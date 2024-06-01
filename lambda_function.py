import json
import boto3

# Create an EC2 client using Boto3
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Check if query parameters are present in the event
    if 'queryStringParameters' in event:
        # Retrieve the instance ID and action from the query parameters
        instance_id = event['queryStringParameters'].get('instance_id')
        action = event['queryStringParameters'].get('action')
        
        # Check if both instance_id and action are provided
        if instance_id and action:
            # Handle the 'start' action
            if action == 'start':
                # Start the specified EC2 instance
                ec2.start_instances(InstanceIds=[instance_id])
                print('Started your instance: ' + instance_id)
                return {
                    'statusCode': 200,  # HTTP status code for success
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'message': 'Instance started successfully'})
                }
            # Handle the 'stop' action
            elif action == 'stop':
                # Stop the specified EC2 instance
                ec2.stop_instances(InstanceIds=[instance_id])
                print('Stopped your instance: ' + instance_id)
                return {
                    'statusCode': 200,  # HTTP status code for success
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'message': 'Instance stopped successfully'})
                }
            else:
                # Invalid action specified
                print('Invalid action specified')
                return {
                    'statusCode': 400,  # HTTP status code for bad request
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Invalid action specified'})
                }
    
    # If the instance_id is incorrect or missing query parameters
    print('Invalid instance ID or missing query parameters, instance not started/stopped')
    return {
        'statusCode': 401,  # HTTP status code for unauthorized
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Invalid instance ID or missing query parameters'})
    }
