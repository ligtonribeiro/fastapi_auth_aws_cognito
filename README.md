## Links úteis

* [AWS Cognito Docs](https://docs.aws.amazon.com/pt_br/cognito/latest/developerguide/example_cognito-identity-provider_AdminInitiateAuth_section.html)

## Deploy AWS Lambda / API Gateway

1. Build Image
   ```sh
   # $IMAGE is the image name, and $TAG image tag version
   docker build -t $IMAGE:$TAG -f lambda.Dockerfile .
   ```

2. Push the Image to ECR (Deployment using the AWS CLI )
   ```sh
   # Get AWS_ACCOUNT and AWS_REGION
   AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
   AWS_REGION=$(aws ec2 describe-availability-zones --query 'AvailabilityZones[0].RegionName' --output text)

   # login AWS ECR
   aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com

   # create repository
   aws ecr create-repository --repository-name $IMAGE \ 
       --image-scanning-configuration scanOnPush=true \ 
       --image-tag-mutability MUTABLE

   # Create a timestamp tag
   TAG=$(date +%Y%m%d_%H%M%S)

   # Tag the image
   docker tag $IMAGE:latest $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE:$TAG

   # Push image
   docker push $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE:$TAG
   ```

3. Create a Lambda Execution Role
   ```sh
    # Give the Lambda execution role a name in AWS_LAMBDA_ROLE_NAME
    aws iam create-role --role-name $AWS_LAMBDA_ROLE_NAME \ 
        --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

    aws iam attach-role-policy --role-name $AWS_LAMBDA_ROLE_NAME \ 
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    aws iam attach-role-policy --role-name $AWS_LAMBDA_ROLE_NAME \ 
        --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess
   ```

4. Create Lambda Function
   ```sh
   ENV=stage
   AWS_LAMBDA_FUNC_NAME="$IMAGE-$ENV"

   aws lambda create-function \
       --function-name $AWS_LAMBDA_FUNC_NAME \
       --package-type Image \
       --code ImageUri=$AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE:$TAG \
       --role $(aws iam get-role --role-name $AWS_LAMBDA_ROLE_NAME --query 'Role.Arn' --output text)
   ```

5. Update Environments Variables
   ```sh
   # Upload the current ENV to Lambda
    aws lambda update-function-configuration \
        --function-name $AWS_LAMBDA_FUNC_NAME \
        --environment "Variables={ENV=$ENV}"
   ```

6. Create API Gateway
   ```sh
   API_GATEWAY_NAME=$IMAGE

   # Create API Gateway
   aws apigateway create-rest-api --name $API_GATEWAY_NAME --region $AWS_REGION

   # Get the API Gateway ID.
   API_GATEWAY_ID=$(aws apigateway get-rest-apis --query "items[?name=='$API_GATEWAY_NAME'].id" --output text)
   ```

7. Create proxy resource
   ```sh
   # Obtain parent ID the created API Gateway
   PARENT_ID=$(aws apigateway get-resources --rest-api-id $API_GATEWAY_ID --region $AWS_REGION --query 'items[0].id' --output text)

   aws apigateway create-resource --rest-api-id $API_GATEWAY_ID --region $AWS_REGION --parent-id $PARENT_ID --path-part {proxy+}
   ```

8. Add ANY method on the proxy resource
   ```sh
   # Obtain ID of the proxy resource
   RESOURCE_ID=$(aws apigateway get-resources --rest-api-id $API_GATEWAY_ID --query "items[?parentId=='$PARENT_ID'].id" --output text)

   # Add ANY method to the resource
   aws apigateway put-method --rest-api-id $API_GATEWAY_ID \
       --region $AWS_REGION \ 
       --resource-id $RESOURCE_ID \ 
       --http-method ANY \ 
       --authorization-type "NONE"
   ```

9. Add Lambda integration to the ANY method
   ```sh
   LAMBDA_ARN=$(aws lambda get-function --function-name $AWS_LAMBDA_FUNC_NAME --query 'Configuration.FunctionArn' --output text)

   aws apigateway put-integration \
       --region $AWS_REGION \
       --rest-api-id $API_GATEWAY_ID \
       --resource-id $RESOURCE_ID \
       --http-method ANY \
       --type AWS_PROXY \
       --integration-http-method POST \
       --uri arn:aws:apigateway:${AWS_REGION}:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations
   ```

10. Grant permission for API Gateway to invoke Lambda
    ```sh
    aws lambda add-permission 
        --function-name $LAMBDA_ARN 
        --source-arn "arn:aws:execute-api:$AWS_REGION:$AWS_ACCOUNT:$API_GATEWAY_ID/*/*/{proxy+}" 
        --principal apigateway.amazonaws.com 
        --statement-id apigateway-access 
        --action lambda:InvokeFunction
    ```

11. Deploy API Gateway
    ```sh
    aws apigateway create-deployment --rest-api-id $API_GATEWAY_ID --stage-name $ENV --variables env=$ENV
    ```

12. Update Lambda with new version image
    ```sh
    aws lambda update-function-code \
        --function-name $AWS_LAMBDA_FUNC_NAME \
        --image-uri $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE:$TAG
    ```

## Reference
- [API Service with FastAPI + AWS Lambda + API Gateway and Make It Work](https://fanchenbao.medium.com/api-service-with-fastapi-aws-lambda-api-gateway-and-make-it-work-c20edcf77bff)