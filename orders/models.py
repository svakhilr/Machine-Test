from django.db import models
from django.utils import timezone
from vendors.models import Vendor

class PurchaseOrder(models.Model):
    
    PENDING ='Pending'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'

    STATUS = (
        (PENDING,'Pending'),
        (CANCELLED,'Cancelled'),
        (COMPLETED,'Completed')
    )

    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,related_name='order')
    order_id = models.CharField(max_length = 15,unique=True,null=True,blank=True)
    items = models.JSONField()
    item_quantity = models.IntegerField()
    order_status = models.CharField(choices = STATUS,default=PENDING)
    delivery_date = models.DateField()
    rating_point = models.IntegerField(null=True,blank=True)
    issue_date = models.DateField(blank=True,null=True)
    order_date = models.DateField(auto_now_add=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f"order {self.order_id}"
    
    def save(self,*args,**kwargs):
        super().save()
        if not self.order_id:
            self.order_id = f"{timezone.now().date().strftime('%Y%m%d')}{self.pk}"
            print(self.order_id)
            self.save(*args,**kwargs)



