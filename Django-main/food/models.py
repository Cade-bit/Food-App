from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from managers import ItemManager
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    user_name = models.ForeignKey(User, on_delete= models.CASCADE,default= 1)
    item_name = models.CharField(max_length=200, db_index=True)
    item_description = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=10,decimal_places=2, db_index=True)
    item_image = models.CharField(max_length=500, default="https://www.thefuzzyduck.co.uk/wp-content/uploads/2024/05/image-coming-soon-placeholder-01-660x660.png")

    is_deleted = models.BooleanField(default=False) # soft delete flag
    deleted_at = models.DateTimeField(blank=True, null=True)


    objects = ItemManager()
    all_objects = models.Manager()


    class Meta:
        indexes = [
            models.Index(fields=['user_name','item_price']),
        ]

    def __str__(self):
        return self.item_name + ":" + str(self.item_price)


    def get_absolute_url(self):
        return reverse("food:detail", kwargs={"pk": self.pk})

    def delete(self,using=None,keep_parents=False):
        self.is_deleted= True
        self.deleted_at= timezone.now()
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name