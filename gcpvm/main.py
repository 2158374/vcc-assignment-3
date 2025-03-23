import functions_framework
import google.auth
from googleapiclient.discovery import build
from flask import Flask, request

app = Flask(__name__)

PROJECT_ID = "prime-ember-454418-t8"
INSTANCE_GROUP_NAME = "my-mig"
ZONE = "us-central1-a"

@functions_framework.http
def scale_trigger3(request):
    request_json = request.get_json()
    
    if request_json and "alerts" in request_json:
        for alert in request_json["alerts"]:
            if alert["status"] == "firing":
                increase_instances()

    return "Scaling triggered", 200

def increase_instances():
    credentials, _ = google.auth.default()
    compute = build("compute", "v1", credentials=credentials)

    instance_group = compute.instanceGroupManagers().get(
        project=PROJECT_ID,
        zone=ZONE,
        instanceGroupManager=INSTANCE_GROUP_NAME
    ).execute()

    current_size = instance_group["targetSize"]
    new_size = current_size + 1  # Scale up by 1

    compute.instanceGroupManagers().resize(
        project=PROJECT_ID,
        zone=ZONE,
        instanceGroupManager=INSTANCE_GROUP_NAME,
        size=new_size
    ).execute()
