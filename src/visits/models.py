from django.db import models


# Create your models here.
class PageVisits(models.Model):
    # db -> table
    # id -> Primary key -> autofield --> 1, 2, 3, 4
    path = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

