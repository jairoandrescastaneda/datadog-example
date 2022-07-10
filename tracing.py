import base64
import json


def get_data_dynamodb_stream(event_record):
    return base64.b64decode(event_record['records'])


def get_first_event_record(dynamo_records):
    return dynamo_records[0]["dynamodb"]["NewImage"]


def get_data_contex_trace(data_inserted):
    data_trace = json.loads(data_inserted["_datadog"]["S"])
    trace_id = data_trace["x-datadog-trace-id"]
    parent_id = data_trace["x-datadog-parent-id"]
    sampling_priority = data_trace.get("x-datadog-sampling-priority", None)
    return trace_id, parent_id, sampling_priority

def extract_context_tracing(payload, context):
    try:
        records = payload['Records']
        event_record = get_first_event_record(records)
        return get_data_contex_trace(event_record)
    except Exception as error:
        return None, None, None
