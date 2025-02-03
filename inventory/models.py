from django.db import models
from django.contrib.auth.models import User



# Create your models here.
 
class inventoryItem(models.Model):
    name=models.CharField(max_length=200)
    quantity = models.IntegerField()
    category = models.ForeignKey('category', on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
  
    issue_out_status = models.ForeignKey('IssueOut', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_items')
    @property
    def is_issued(self):  # More descriptive name for a boolean property
        if self.issue_out:
            return self.issue_out.issue_out_status
        return False 



    def __str__(self):
     return self.name





class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'catergories'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 
   



class Staff(models.Model):
    name = models.CharField(max_length=200)
    #postion = models.CharField(max_length=200)
    department = models.ForeignKey('department', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.name 


class IssueOut(models.Model):
    issue_date = models.DateTimeField(auto_now=True)
    issue_out_status = models.BooleanField(default=False)
    inventoryItem = models.ForeignKey(
        'inventoryItem', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='issueout_inventory'
    ) 
    staff = models.ForeignKey(
        'staff', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )
    quantity = models.PositiveIntegerField(blank=False, null=False, default=0)  