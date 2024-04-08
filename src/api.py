import json
import boto3
import logging
import os
import typing as t

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', "")

sqs = boto3.resource('sqs')
queue = sqs.Queue(SQS_QUEUE_URL)


def prepare_message_for_queue(event_body) -> dict[str, t.Any]:
    base_message = {
        "message": {
            "message_id": event_body["message"]["message_id"],
            "chat": {
                "id": event_body["message"]["chat"]["id"],
                "type": event_body["message"]["chat"]["type"],
            },
            "text": event_body["message"]["text"],
            "date": event_body["message"]["date"]
        },
        "update_id": event_body["update_id"],
    }
    if "entities" in event_body["message"]:
        base_message["message"]["entities"] = event_body["message"]["entities"]
    return base_message


def lambda_handler(event, context):
    logger.info("event: {}".format(json.dumps(event)))
    try:
        message = prepare_message_for_queue(event_body=event["body"])
        queue.send_message(MessageBody=json.dumps(message))
        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as exc:
        logger.error(f"Exception: {exc}")
        return {
            'statusCode': 500,
            'body': 'Failure'
        }
