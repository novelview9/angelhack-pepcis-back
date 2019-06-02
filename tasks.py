from apps.models import Refugee, RefugeeFaceAddResult
from apps.utils import add_face_image
import json
from zappa.asynchronous import task

@task
def assign_image_to_azure(refugee_id):
    refugee = Refugee.objects.get(id=refugee_id)
    response = add_face_image(refugee.image.url, refugee.shelter_id, refugee.id)
    persisted_face_id = json.loads(response.content).get('persistedFaceId')
    RefugeeFaceAddResult.objects.create(
        persisted_face_id=persisted_face_id,
        refugee=refugee,
        is_recognized=True
    )
