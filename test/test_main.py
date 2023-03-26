import glob
import json

import boto3
from moto import mock_sqs

from sqs_sample.main import *


@mock_sqs
def test_send_message():
    sqs = boto3.client("sqs")
    r = sqs.create_queue(QueueName="unittest-queue")
    queue_url = r["QueueUrl"]

    entries = []
    json_paths = glob.glob("./test/messages/*.json")
    for i, json_path in enumerate(json_paths):
        with open(json_path, "r") as json_f:
            json_data = json.load(json_f)
            json_payload = json.dumps(json_data)
            # boto3のsend_message_batchの仕様に合わせてIdは文字列にする
            entry_id = str(i)
            entry = {"Id": entry_id, "MessageBody": json_payload}
            entries.append(entry)
    _ = sqs.send_message_batch(QueueUrl=queue_url, Entries=entries)

    # テスト
    messages = get_messages(queue_url)

    # メッセージ内容
    message = json.loads(messages[0]["Body"])
    assert message["message"] == "test message 1"

    message = json.loads(messages[1]["Body"])
    assert message["message"] == "test message 3"

    message = json.loads(messages[2]["Body"])
    assert message["message"] == "test message 2"

    message = json.loads(messages[3]["Body"])
    assert message["message"] == "test message 5"

    message = json.loads(messages[4]["Body"])
    assert message["message"] == "test message 4"

    # メッセージ数
    assert len(messages) == 5
