from django.utils import timezone
import requests
from django.conf import settings
import json

def default_image_path(instance, file_name):
    now = timezone.now()
    path = f"images/{instance.__class__.__name__.lower()}/{str(now.date())}_{now.timestamp()}.{file_name.split('.')[-1]}"
    return path


base_azure_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0"

azure_headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': settings.AZURE_SUBSCRIPTION_KEY,
}


def assign_shelder_facegroup_id(shelter_id):
    from .models import Shelter
    shelter = Shelter.objects.get(id=shelter_id)
    url = f'{base_azure_url}/largefacelists/{shelter_id}'
    data = {
        "name": shelter.place,
        "recognitionModel": "recognition_02"
    }
    response = requests.put(url, data=json.dumps(data), headers=azure_headers)
    if response.status_code != 200:
        raise Exception()

    shelter.azure_on = True
    shelter.save(update_fields=['azure_on'])

def add_face_image(image_url, shelter_id, refugee_id):
    data = { "url": image_url }
    url = f'{base_azure_url}/largefacelists/{shelter_id}/persistedfaces?id={refugee_id}'
    response = requests.post(url, data=json.dumps(data), headers=azure_headers)
    return response

def run_image_finder(image_url):
    data = {
            "url": image_url,
            "recognitionModel": "recognition_02"
    }
    url = f"{base_azure_url}/detect?returnFaceId=true"
    response = requests.post(url, data=json.dumps(data), headers=azure_headers)
    face_id = json.loads(response.content)[0].get('faceId')
    result = find_face_image(face_id, 4)


def find_face_image(face_id, shelter_id):
    from .models import Shelter
    data = {
        "faceId": face_id,
        'largeFaceListId': shelter_id
    }
    url = f'{base_azure_url}/findsimilars'
    response = requests.post(url, data=json.dumps(data), headers=azure_headers)
    return response
