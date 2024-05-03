import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/tz3hpt"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_messages():
    
    messages = []
    
    try:
        for _ in range(10): 
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                MessageAttributeNames=['All'],
                VisibilityTimeout=300  # 5 minutes timeout
            )

            if 'Messages' in response:
                message = response['Messages'][0]
                order = int(message['MessageAttributes']['order']['StringValue'])
                word = message['MessageAttributes']['word']['StringValue']
                handle = message['ReceiptHandle']
                
                messages.append({'order': order, 'word': word})
                
                #sqs.delete_message(QueueUrl=url, ReceiptHandle=handle)
            else:
                print("No more messages in the queue")
                break
    except Exception as e:
        print(f"An error occurred: {e}")

    # Reassemble
    messages.sort(key=lambda x: x['order'])
    sentence = ' '.join([msg['word'] for msg in messages])
    print(sentence)

    with open('phrase.txt', 'w') as file:
        file.write(sentence)

if __name__ == "__main__":
    get_messages()