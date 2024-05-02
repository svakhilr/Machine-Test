from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Vendor
from .serializers import VendorCreateSerializer,VendorListSerializer,VendorUpdateSerializer,VendorPerformanceSerializer
from config.utils import get_tokens_for_user
from rest_framework.permissions import IsAuthenticated


class VendorViewset(viewsets.ModelViewSet):

    queryset = Vendor.objects.all()
    serializer_class = {
        'list':VendorListSerializer,
        'retrieve':VendorListSerializer,
        'create':VendorCreateSerializer,
        'update':VendorUpdateSerializer,
        'partial_update':VendorUpdateSerializer,
        # 'performance':VendorUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializer_class[self.action]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.save()
        print(vendor)
        user = vendor.user
        tokens = get_tokens_for_user(user) 
        data = {
            'refresh_token': tokens['refresh'],
            'access_token' : tokens['access'],
            'vendor'       : serializer.data
        }
        return  Response(data,status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=["get"])
    def performance(self,request,pk=None):
        vendor = Vendor.objects.get(id=pk)
        serializer = VendorPerformanceSerializer(vendor)

        return Response(serializer.data , status=status.HTTP_200_OK)
        





