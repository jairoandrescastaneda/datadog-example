import json
import os
from logging import basicConfig, getLogger, INFO
import requests
import boto3
import uuid

logger = getLogger(__name__)
basicConfig(level=INFO, format='PID:%(process)d %(asctime)s %(name)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

ses_client = boto3.client('ses')

html_data = """Subject: Subscription
MIME-Version: 1.0
Content-Type: text/HTML

<!DOCTYPE html>
    <html>
    <head>
        <style>
            h1   {color: #333;}
            p    {color: #555;}
        </style>
    </head>
    <body>
        <h1>Welcome</h1>
     
    </body>
</html>
"""

def register(event, context):
    try:
        records = event["Records"]
        for record in records:
            data = record["dynamodb"]
            body = data.get("NewImage", None)
            if body:
                logger.info("User created")
                user_id = uuid.uuid4().hex
                user = {"id": body["id"]["S"] ,"name": body["name"]["S"], "age": body["age"]["N"], "email": body["email"]["S"]}
                response = ses_client.send_raw_email(
                    Source='andresbbx@gmail.com',
                    Destinations=[
                        user["email"],
                    ],
                    RawMessage={
                        'Data': html_data
                    }
                )

        return {"statusCode": 200, "body": json.dumps(user)}

    except Exception as error:
        logger.exception(error)
        return {"statusCode": 400, "body": json.dumps({"error": "error"})}


