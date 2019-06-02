from model_utils.models import TimeStampedModel
from django.db import models
from .utils import default_image_path


class Model(TimeStampedModel):
    class Meta:
        abstract = True


class Shelter(models.Model):
    place = models.CharField('장소', max_length=250)
    azure_on = models.BooleanField('에저그룹생성', default=False)

    def __str__(self, *args, **kwargs):
        return f'{self.place}(id:{self.id})'


class Refugee(Model):
    ALIVE = 'alive'
    DEATH = 'death'
    MOVEOUT = 'moveout'

    STATUS = [
        (ALIVE, 'alive'),
        (DEATH, 'death'),
        (MOVEOUT, 'moveout'),
    ]
    shelter = models.ForeignKey('Shelter', verbose_name='피난처', on_delete=models.CASCADE)
    image = models.ImageField('이미지', upload_to=default_image_path)
    status = models.CharField('상태', choices=STATUS, max_length=250)


class RefugeeFaceAddResult(Model):
    refugee = models.ForeignKey('Refugee', verbose_name='등록결과', on_delete=models.CASCADE)
    is_recognized = models.BooleanField('인식여부')
    persisted_face_id = models.CharField("인식아이디", max_length=250, blank=True, null=True)


class FindRequest(Model):
    READY = 'ready'
    FAIL = 'fail'
    SUCCESS = 'success'

    STATUS = [
        (READY, 'ready'),
        (FAIL, 'fail'),
        (SUCCESS, 'success')
    ]
    image = models.ImageField('이미지', upload_to=default_image_path)
    contact = models.CharField('연락처', max_length=250)
    status = models.CharField('상태', choices=STATUS, max_length=250, default=READY)


class FindResult(Model):
    find_request = models.ForeignKey('FindRequest', verbose_name='찾기요청', on_delete=models.CASCADE, related_name='find_results',)
    refugee = models.ForeignKey('Refugee', verbose_name='실종자', on_delete=models.CASCADE, related_name='+',)
    percent = models.CharField('일치도', max_length=250)

