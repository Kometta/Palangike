from tincan import RemoteLRS, Statement
import requests
import os
import os.path
import json

def generate_xapi_statements(activity, file):
    raw_data = json.load(file)

    statements = []
    for student in raw_data['name']:
        statement = Statement(
            actor={'name': raw_data['name'][student], 'mbox': raw_data['email'][student]},
            verb={'id': 'http://adlnet.gov/expapi/verbs/completed', 'display': {'en-US': 'completed'}},
            object={'id': 'http://example.com/activities/kahoot-game', 'definition': {'name': {'en-US': 'Kahoot game'}}},
            result={"completion": "true","score": {"raw": raw_data[activity][student], "min": 0,"max": 10000} }
        )
        statements.append(statement)

    return statements

def send_statements_to_lrs(endpoint, username, password, file):

    # Disable SSL certificate verification
    requests.packages.urllib3.disable_warnings()

    # Configure SCORM Cloud LRS connection details
    lrs_config = {
        'endpoint': endpoint,
        'username': username,
        'password': password
    }

    # # Create RemoteLRS instance
    lrs = RemoteLRS(**lrs_config)

    # Disable SSL certificate verification for the LRS
    lrs.endpoint = lrs.endpoint.replace('https://', 'http://')

    activity = 'kahoot_score'
    statements = generate_xapi_statements(activity, file)

    # # # Send the statement to the LRS
    for statement in statements:
        lrs.save_statement(statement)
        
            
