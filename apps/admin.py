from django.contrib import admin
from .models import Refugee, Shelter, FindRequest, FindResult, RefugeeFaceAddResult
from django.db.models.fields.reverse_related import ForeignObjectRel
from django.db.models.fields.reverse_related import OneToOneRel
from django.db.models.fields.reverse_related import ManyToOneRel
from django_object_actions import DjangoObjectActions


class ModelAdmin(DjangoObjectActions, admin.ModelAdmin):
    @staticmethod
    def check_related_field(field):
        if type(field) in [ForeignObjectRel, ManyToOneRel, OneToOneRel]:
            return True

    def get_list_display(self, request):
        if self.list_display == ('__str__',):
            list_display = [field.name for field in self.model._meta.get_fields() if not self.check_related_field(field)]
        else:
            list_display = self.list_display

        return list_display

@admin.register(Refugee)
class RefugeeAdmin(ModelAdmin):
    change_actions = ('assign_azure_face_id', )

    def assign_azure_face_id(self, request, obj):
        from tasks import assign_image_to_azure
        assign_image_to_azure(obj.id)



@admin.register(Shelter)
class ShelterAdmin(ModelAdmin):
    change_actions = ('assign_azure_largefacelists', )

    def assign_azure_largefacelists(self, request, obj):
        from .utils import assign_shelder_facegroup_id
        assign_shelder_facegroup_id(obj.id)

@admin.register(FindRequest)
class FindRequestAdmin(ModelAdmin):
    pass

@admin.register(FindResult)
class FindResultAdmin(ModelAdmin):
    pass

@admin.register(RefugeeFaceAddResult)
class RefugeeFaceAddResultAdmin(ModelAdmin):
    pass
