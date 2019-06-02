from rest_framework import generics
from .serializers import RefugeeSerializer, FindRequestSerializer
from .models import Refugee, FindRequest, FindResult
from rest_framework.exceptions import ValidationError
from tasks import assign_image_to_azure
from rest_framework.response import Response


class CreateRefugeeView(generics.CreateAPIView):
    queryset = Refugee.objects.all()
    serializer_class = RefugeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        from IPython import embed;embed()
        serializer.is_valid(raise_exception=True)
        refugee = serializer.save()
        assign_image_to_azure(refugee.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class FindRequestView(generics.ListCreateAPIView):
    queryset = FindRequest.objects.all()
    serializer_class = FindRequestSerializer

    def get_queryset(self, *args, **kwargs):
        contact = self.request.GET.get('contact')
        if not contact:
            raise ValidationError('올바른 contact url prarameter가 필요합니다.')
        return FindRequest.objects.filter(contact=contact)
