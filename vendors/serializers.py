from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from .models import Vendor
from django.contrib.auth import get_user_model

User = get_user_model()


class VendorCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source = 'user.email')
    password  = serializers.CharField(source = 'user.password',write_only=True)

    class Meta:
        model = Vendor
        fields = ('id','email','password','name','contact_number','address')

    def create(self, validated_data):
        print(validated_data)
        
        user_data = validated_data.pop('user')
        user = User.objects.create_user(user_data["email"],user_data["password"])
        vendor = Vendor.objects.create(user=user,**validated_data)
        return vendor
    
        

class VendorListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source = 'user.email')
  
    class Meta:
        model = Vendor
        fields = ('id','email','name','vendor_code','contact_number','address')

class VendorUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source = 'user.email')
  
    class Meta:
        model = Vendor
        fields = ('id','email','name','vendor_code','contact_number','address')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user',None)
        if user_data:
            try:
                user = User.objects.filter(id= instance.user.id)
                user.update(**user_data)
            except User.DoesNotExist:
                raise ValidationError('User does not exist')
            except IntegrityError:
                raise ValidationError("Email with this user exists")
            instance.refresh_from_db()
        return super().update(instance, validated_data)


class VendorPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ('name','on_time_delevery_rate','rating','fullfillment_rate')




