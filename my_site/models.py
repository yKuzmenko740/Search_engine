from django.db import models


# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=100, default='list')

    def __str__(self):
        return f'{self.search, self.city}'

    class Meta:
        verbose_name_plural = 'Searches'