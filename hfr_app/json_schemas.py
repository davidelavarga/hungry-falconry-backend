publish_schedule_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "timestamp": {
            "type": "string"
        },
        "done": {
            "type": "boolean"
        },
        "feeder": {
            "type": "integer"
        },
        "auth_token": {
            "type": "string"
        }
    },
    "required": [
        "id",
        "timestamp",
        "done",
        "feeder",
        "auth_token"
    ]
}
