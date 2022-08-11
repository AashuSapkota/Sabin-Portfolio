from json.encoder import JSONEncoder
from django.db import models
from datetime import date, datetime, time
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.utils.timezone import now
import _pickle as pkl
import json
import numpy
import face_recognition as fr

from department.models import DepartmentListModel
from position.models import PositionListModel
from level.models import LevelListModel


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class EmployeeListModel(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female")
    )
    emp_firstname = models.CharField(max_length=15, null=False, blank=False)
    emp_middlename = models.CharField(max_length=15, null=False, blank=True)
    emp_lastname = models.CharField(max_length=15, null=False, blank=False)
    emp_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False, blank=False)
    emp_DOB = models.DateField(null=False, blank=False)
    emp_contact_number = models.CharField(max_length=15, null=False, blank=False)
    emp_mail = models.EmailField(blank=False, null=False)
    emp_address =models.CharField(max_length=50, null=False, blank=False)
    emp_department = models.ForeignKey(DepartmentListModel, on_delete=models.SET_NULL, null=True, blank=False)
    emp_position = models.ForeignKey(PositionListModel, on_delete=SET_NULL, null=True, blank=False)
    emp_level = models.ForeignKey(LevelListModel, on_delete=SET_NULL, null=True, blank=False)
    emp_image = models.ImageField(upload_to='employee_images', null=True)
    emp_image_binary = models.BinaryField(null=True)
    emp_document = models.FileField(upload_to='documents', null=False, blank=False)
    emp_registered_date = models.DateField(default=date.today())
    emp_joining_date =  models.DateField(null=False, blank=False)
    def save(self, *args, **kwargs):
        read_emp_image = fr.load_image_file(self.emp_image)
        encoded_emp_image = fr.face_encodings(read_emp_image)[0]
        encoded_emp_image = {'encoded_emp_image':encoded_emp_image}
        json_encoded_emp_image = json.dumps(encoded_emp_image, cls=NumpyArrayEncoder)
        picked_encoded_emp_image = pkl.dumps(json_encoded_emp_image)
        self.emp_image_binary=picked_encoded_emp_image

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.emp_firstname
    
    class Meta:
        ordering= ('emp_firstname',)



class EmployeeLogmodel(models.Model):
    LOG_CHOICES = (
        ("I", "Check-in"),
        ("O", "Check-Out"),
    )
    emp_name = models.ForeignKey(EmployeeListModel, on_delete=models.SET_NULL, null=True, blank=False)
    log_type = models.CharField(max_length=1, choices=LOG_CHOICES, null=True, blank=True)
    check_in_datetime = models.DateTimeField()
    check_out_datetime = models.DateTimeField(null=True, blank=True)



# if(emp.check_in_datetime != None and emp.check_out_datetime == None):
#                         in_date = emp.check_in_datetime.strftime('%D')
#                         out_date = emp.check_out_datetime
#                         today = datetime.today().strftime('%D')
#                         if in_date == today and out_date == None and log_type=='O':
#                             print('Today, Checkout')
#                             emp.check_out_datetime = datetime.now()
#                             emp.save()
#                             print('Checked Out')