import json
import os
from logging import basicConfig, getLogger, INFO
import requests
import boto3
import uuid


logger = getLogger(__name__)
basicConfig(level=INFO, format='PID:%(process)d %(asctime)s %(name)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME_EVENT"]
table = dynamodb.Table(TABLE_NAME)


def register(event, context):

    try:
        records = event["Records"]
        for record in records:
            data = record["dynamodb"]
            body = data.get("NewImage", None)
            if body:

                logger.info("User created")
                user = {"id": body["id"]["S"] ,"name": body["name"]["S"], "age": body["age"]["N"], "email": body["email"]["S"]}
                table.put_item(Item=user)

        return {"statusCode": 200, "body": json.dumps(user)}

    except Exception as error:
        logger.exception(error)
        return {"statusCode":400, "body":json.dumps({"error":"error"})}


