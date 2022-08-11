from django.db import models


class PositionListModel(models.Model):
    position_name = models.CharField(max_length=50, null=False, blank=False)
    position_description = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('position_name',)
    
    def __str__(self):
        return self.position_name