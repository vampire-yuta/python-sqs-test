import boto3


def get_messages(queue_url):
    sqs = boto3.client("sqs")
    wait_time_seconds = 5
    messages = []

    r = sqs.receive_message(
        QueueUrl=queue_url, WaitTimeSeconds=wait_time_seconds, MaxNumberOfMessages=10
    )

    received_messages = r.get("Messages")
    if received_messages:
        messages += received_messages

    return messages
