# EC2 Stop/Start Lambda Function

This repository contains a Python-based AWS Lambda function that will enable you to easily start or stop EC2 instances using HTTPS GET or POST requests. This tool is particularly useful for managing development instances. You can bookmark the URLs in your browser for quick access to turn your instances on or off.

## How It Works
- **AWS Lambda Function with Function URL:** While you can use an AWS API Gateway endpoint to invoke the Lambda function, the simplest way is to use Lambda's built-in "Function URL" feature which provides you a simple endpoint URL you can send GET or POST requests to invoke the function's code.
- **Query Parameters:** The Lambda function code accepts `instance_id` and `action` as query parameters on the GET or POST request.
- **Action Execution:** Based on the `action` parameter (either `start` or `stop`), the function starts or stops the specified EC2 instance.
- **Responses:** The function returns appropriate responses for successful operations, invalid actions, or missing parameters.

## Setup Instructions

1. **Create Lambda Function:**
    - Go to the AWS Lambda console and create a new function.
    - Choose Python 3.12 Runtime, and leave other settings as default.
    - Under Advanced Settings, select `Enable function URL` and Auth type `NONE` to make the URL public for ease of use.
    **_IMPORTANT: The Lambda Function URL will be completely public with these settings meaning anyone can invoke it and start/stop your instances if they know the URL. Use with caution and see Security Considerations section below._**
  
2. **Configure Lambda Function:**
    - Copy the provided Python code in this repo's lambda_function.py file into the Lambda function's editor.
    - `Save` the lambda_function.py file, and `Deploy` the function.

3. **Create and Attach IAM Policy:**
    - Ensure the Lambda function has the necessary permissions to start and stop EC2 instances by creating and attaching an appropriate IAM policy.
        1. **Navigate to the IAM Console:**
            - Go to the IAM console.
        2. **Create a Policy:**
            - In the left sidebar, click on `Policies`.
            - Click `Create policy`.
            - Go to the `JSON` tab and paste the following policy document. This will provide full access to start/stop any EC2 instance in your entire AWS account. Change this policy to narrow the scope and limit to specific instances, regions, etc.
            ```json
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "ec2:StartInstances",
                            "ec2:StopInstances"
                        ],
                        "Resource": "arn:aws:ec2:*:<account-id>:instance/*"
                    }
                ]
            }
            ```
            - Replace `<account-id>` with your AWS account ID. 
            - Click `Next`.
            - Give the policy a name, e.g., `EC2StartStopPolicy`, and click `Create policy`.
        3. **Attach the Policy to the Lambda Execution Role:**
            - In the left sidebar, click on `Roles`.
            - Search for the role created for your Lambda function. It typically starts with `<function-name>-role`.
            - Click on the role name to open its details.
            - Under the `Permissions` tab, click `Add permissions` and select `Attach policies`.
            - Search for the `EC2StartStopPolicy` you created and attach it to the role.
  
4. **Function URL**
    - Back in the Lambda console, copy the `Function URL` that was generated when we created the function.
    - In the EC2 console, copy a full EC2 instance ID, including the "i-" in the beginning.
    - To test starting or stopping the instance, see below. 

## Usage

- Open your browser and paste the URL with the required query parameters. Examples below.

### Start an EC2 Instance
```
https://<your-lambda-function-url>?instance_id=<your-instance-id>&action=start
```

### Stop an EC2 Instance
```
https://<your-lambda-function-url>?instance_id=<your-instance-id>&action=stop
```



## Security Considerations

- **Access Control**: This guide outlines making the Lambda Function URL publicly accessible, which is NOT recommended security practice. If someone has your instance ID and URL, they could easily stop/start your instances. "Security through obscurity" is not best practice. Both Lambda Function URLs and AWS API Gateway offer different forms of authentication. Learn more about [Lambda Function URLs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html) and [securing Lambda Function URLs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls-auth.html).

- **AWS API Gateway**: An AWS API Gateway REST endpoint can also be used to invoke the function. API Gateways offer more robust authentication options including Amazon Cognito. Learn more [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html).

- **HTTPS**: Always use HTTPS to encrypt data in transit. This ensures that any data sent between the client and the server is encrypted and secure from eavesdropping or tampering.

- **IAM Roles and Policies**: Implement least privilege principle by creating and attaching IAM policies that only allow necessary actions, on limited resources, such as only starting and stopping specific EC2 instances, rather than broader permissions.

- **CORS Configuration**: If your function URL will be accessed from web applications on different domains, configure Cross-Origin Resource Sharing (CORS) settings appropriately to restrict which domains can make requests to your function URL.

