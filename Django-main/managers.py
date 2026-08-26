from django.db import models


class ItemManager(models.Manager):
    def get_queryset(self):
        ''' Only return items that are not deleted '''
        return super().get_queryset().filter(is_deleted=False)
    def get_deleted_items(self):
        ''' Only return items that are deleted '''
        return super().get_queryset().filter(is_deleted=True)