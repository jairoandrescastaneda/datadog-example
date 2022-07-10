import json
import os
from logging import basicConfig, getLogger, INFO
import boto3
import uuid
from datadog_lambda.tracing import get_dd_trace_context

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()
logger = getLogger(__name__)
basicConfig(level=INFO, format='PID:%(process)d %(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)


def register(event, context):

    try:
        body = json.loads(event['body'])
        user_id = uuid.uuid4().hex
        user = {'id':user_id, 'name': body["name"], 'age': body["age"], 'email':body["email"], '_datadog':json.dumps(get_dd_trace_context())}
        table.put_item(Item=user)
        logger.info("User created")

        return {"statusCode": 200, "body": json.dumps(user)}

    except Exception as error:
        logger.exception(error)
        return {"statusCode":400, "body":json.dumps({"error":"error"})}


