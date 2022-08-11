from django.db import models


class LevelListModel(models.Model):
    level_name = models.CharField(max_length=50, null=False, blank=False)
    level_description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('level_name',)
    
    def __str__(self):
        return self.level_name