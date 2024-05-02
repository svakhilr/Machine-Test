from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F,Q,Sum,Avg





class Vendor(models.Model):
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,related_name='vendor')
    name = models.CharField(max_length=100,unique=True)
    contact_number = models.CharField(max_length=10)
    address = models.TextField()
    vendor_code = models.CharField(max_length=15,unique=True,null=True,blank=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        super().save()
        if not self.vendor_code:
            self.vendor_code = f"{timezone.now().date().strftime('%Y%m%d')}{self.pk}"
            print(self.vendor_code)
            self.save(*args,**kwargs)

    @property
    def on_time_delevery_rate(self):
        from orders.models import PurchaseOrder
        on_time_delevery_count = self.order.all().filter(Q(order_status=PurchaseOrder.COMPLETED) &
            Q(issue_date__lte = F('delivery_date'))).count()
                   
        delevery_completed_count = self.order.all().filter(order_status=PurchaseOrder.COMPLETED).count()

        delevery_rate =round((on_time_delevery_count/delevery_completed_count)*100,3)

        return  delevery_rate
    
    @property
    def rating(self):
        
        rating_sum = self.order.aggregate(Sum('rating_point'))['rating_point__sum']
        
        order_count = self.order.all().count()
        
        return round(((rating_sum)/(order_count)),3)
    
    @property
    def fullfillment_rate(self):
        from orders.models import PurchaseOrder
        order_count = self.order.alcompleted_l().count()
        completed_order_count = self.order.filter(order_status=PurchaseOrder.COMPLETED).count()

        return round((completed_order_count/order_count)*100) 



