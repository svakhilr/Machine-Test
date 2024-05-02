from rest_framework import viewsets
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .serializers import  PurchaseOrderSerializer
from .models import PurchaseOrder


class OrderFilter(filters.FilterSet):
    vendor = filters.CharFilter(method='filter_by_vendor')

    def filter_by_vendor(self, queryset, *args, **kwargs):
        vendor_name = self.request.query_params.get("vendor")
        print(queryset)
        print(vendor_name)
        return queryset.filter(vendor__name__icontains = vendor_name)
        

class PurchaseOrderViewset(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = OrderFilter