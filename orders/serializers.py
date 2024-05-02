from rest_framework import serializers
from django.utils import timezone

from .models import PurchaseOrder


class PurchaseOrderSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(read_only=True)
    vendor_name = serializers.CharField(source ='vendor.name',read_only=True)
    order_date = serializers.CharField(read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = ('id','vendor','vendor_name','order_id','items',
            'item_quantity','order_status','order_date','rating_point',
            'delivery_date','issue_date','created_at','updated_at')
        
    def validate_rating_point(self,value):
        if value and value >5:
            raise serializers.ValidationError("Value must be less than eqaual to five")
        return value
    
    def update(self, instance, validated_data):
        print(validated_data)
        if 'order_status' in validated_data :
            if validated_data['order_status'] == PurchaseOrder.COMPLETED:
                current_date = timezone.now().date()
                validated_data["issue_date"] = current_date
        
        return super().update(instance, validated_data)