from django.db import models


class DepartmentListModel(models.Model):
    department_name = models.CharField(max_length=50, null=False, blank=False)
    department_code = models.CharField(max_length=10, null=False, blank=True)
    department_description = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('department_name',)

    def __str__(self):
        return self.department_name
